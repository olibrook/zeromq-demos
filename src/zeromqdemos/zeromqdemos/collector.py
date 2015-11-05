"""
Runs a process which collects JSON messages from (potentially) many consumers,
prints them and maintains statistics about the performance of consumers.

Usage:
    collector PULL_ADDR

Options:
    -h, --help  Show this screen and exit.
"""
import time
import collections

import zmq
import docopt


class Collector(object):

    def __init__(self, pull_addr):
        self.PULL_ADDR = pull_addr
        self.SAMPLE_SIZE = 100

        # Time the last message was received from each consumer
        self.last_received_times = {}

        # Processing for the last 100 messages for each consumer
        self.processing_times = {}

        # Average processing times for each consumer over the sample size
        self.avg_processing_times = {}

        # Received message counts from each consumer
        self.message_counts = {}

    def run(self):
        context = zmq.Context()

        pull_sock = context.socket(zmq.PULL)
        pull_sock.bind(self.PULL_ADDR)

        while True:
            message = pull_sock.recv_json()

            self.update_stats(message)
            self.process_message(message)

    def update_stats(self, message):
        received_time = time.time()

        consumer_id = message['consumer_id']

        if consumer_id not in self.processing_times:
            self.processing_times[consumer_id] = collections.deque([], self.SAMPLE_SIZE)

        if consumer_id not in self.message_counts:
            self.message_counts[consumer_id] = 0

        # Update processing times from this consumer
        self.processing_times[consumer_id].append(message['processing_time'])

        # Update last time message was received from this consumer
        self.last_received_times[consumer_id] = received_time

        # Update message counts for this consumer
        self.message_counts[consumer_id] += 1

        # Update average response time for this consumer
        self.avg_processing_times[consumer_id] = (
            sum(self.processing_times[consumer_id]) / len(self.processing_times[consumer_id]))

    def process_message(self, message):
        output = ("""
{}
    Received from: {}
    Processing time (this msg): {}
    Processing time (average): {}
    Num processed by consumer: {}
""")
        output = output.format(
            message['result']['data'],
            message['consumer_id'],
            message['processing_time'],
            self.avg_processing_times[message['consumer_id']],
            self.message_counts[message['consumer_id']],
        )
        print(output)


def run(pull_addr):
    """Run from python"""
    collector = Collector(pull_addr)
    collector.run()


def main():
    """Run from command-line"""
    options = docopt.docopt(__doc__)
    run(options['PULL_ADDR'])
