"""
Runs a zmq message processing demo with a configurable number of consumer
processes.

Usage:
    main.py [options]

Options:
    -h, --help                        Show this screen and exit.
    --num-consumers=<num_consumers>   The number of consumers [default: 3]
"""

import multiprocessing

import docopt

import zeromqdemos.producer as producer
import zeromqdemos.consumer as consumer
import zeromqdemos.collector as collector


def main():
    options = docopt.docopt(__doc__)

    num_consumers = int(options['--num-consumers'])

    processes = []

    producer_proc = multiprocessing.Process(
        target=producer.run,
        args=('tcp://127.0.0.1:5554',)
    )

    processes.append(producer_proc)

    for x in range(num_consumers):
        processes.append(multiprocessing.Process(
            target=consumer.run,
            args=(
                'consumer-{}'.format(x),
                'tcp://127.0.0.1:5554',
                'tcp://127.0.0.1:5555',
            )
        ))

    processes.append(multiprocessing.Process(
        target=collector.run,
        args=('tcp://127.0.0.1:5555',)
    ))

    for p in processes:
        p.daemon = True  # All child processes killed on exit
        p.start()

    producer_proc.join()  # Doesn't matter which we join - none terminate
