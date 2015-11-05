"""
Runs a process which pushes JSON messages into a zmq PUSH socket.

Example output:

    {"data": "a message"}

Usage:
    producer PUSH_ADDR

Options:
    -h, --help  Show this screen and exit.
"""
import random
import time

import zmq
import docopt


class Producer(object):

    def __init__(self, push_addr):
        self.PUSH_ADDR = push_addr

    def run(self):
        context = zmq.Context()
        push_sock = context.socket(zmq.PUSH)
        push_sock.bind(self.PUSH_ADDR)
        while True:
            push_sock.send_json(self.get_message())
            time.sleep(0.25)

    def get_message(self):
        words = ['wow', 'amazing', 'omg', 'fantastic']
        return {'data': random.choice(words)}


def run(push_addr):
    """Run from python"""
    producer = Producer(push_addr)
    producer.run()


def main():
    """Run from command-line"""
    options = docopt.docopt(__doc__)
    run(options['PUSH_ADDR'])
