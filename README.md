Zeromq Demos
============

A simple zeromq processing pipeline. The pipeline transforms JSON messages
from this:

    {"data": "aweseme"}

to this:

    {"data": "AWESOME!!!"}

The number of consumers doing the transformation is configurable and a single
collector combines results and keeps simple statistics about the performance
of each consumer.

Tested on Python 2.7.6 and Ubuntu 14.04

Setup
-----

Install dependencies:

    python2.7 bootstrap.py
    ./bin/buildout

Run
---

Once installed, the following scripts are available under ./bin:

    bin
    ├── collector
    ├── consumer
    ├── producer
    └── zeromqdemos-main

You can run --help on each one to see available options. Alternatively,
just run

    ./bin/zeromqdemos-main

Which will set up a producer, 3 consumers and a collector, each running in
a separate process with the collected results printed to stdout.
