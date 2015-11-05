"""
Runs a worker which consumes JSON messages on a zmq PULL socket, transforms
those messages and forwards the result on to a zmq PUSH socket.

Output messages are wrapped to show which consumer produced the result.

Usage:
    consumer.py CONSUMER_ID PULL_ADDR PUSH_ADDR

Options:
    -h, --help  Show this screen and exit.
"""
import time

import zmq
import docopt


class Consumer(object):

    def __init__(self, consumer_id, pull_addr, push_addr):
        self.CONSUMER_ID = consumer_id  # Get from OS.environ or sys.argv
        self.PULL_ADDR = pull_addr
        self.PUSH_ADDR = push_addr

    def run(self):
        context = zmq.Context()

        pull_sock = context.socket(zmq.PULL)
        pull_sock.connect(self.PULL_ADDR)

        push_sock = context.socket(zmq.PUSH)
        push_sock.connect(self.PUSH_ADDR)

        while True:
            message = pull_sock.recv_json()

            start = time.time()
            result = self.process_message(message)
            end = time.time()

            result = self.wrap_result(result, start, end)
            push_sock.send_json(result)

    def wrap_result(self, result, start, end):
        return {
            'consumer_id': self.CONSUMER_ID,
            'processing_time': end - start,
            'result': result
        }

    def process_message(self, message):
        """Transforms a message to add a bit of drama"""
        time.sleep(0.25)
        return {
            'data': message['data'].upper() + '!!!'
        }


def run(consumer_id, pull_addr, push_addr):
    """Run from python"""
    consumer = Consumer(
        consumer_id,
        pull_addr,
        push_addr,
    )
    consumer.run()


def main():
    """Run from command-line"""
    options = docopt.docopt(__doc__)
    run(
        options['CONSUMER_ID'],
        options['PULL_ADDR'],
        options['PUSH_ADDR'],
    )
