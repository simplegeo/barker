# Clive is Copyright 2011 SimpleGeo, Inc.
# Written by Paul Lathrop <paul@simplegeo.com>

import logging
from optparse import OptionParser, make_option
try:
    import simplejson as json
except ImportError:
    import json
import sys

from kombu import BrokerConnection, Exchange, Queue, Producer, Consumer

import clive.config as config
import clive.pod as pod

OPTIONS={"directory": make_option("-d", "--directory", help="Path to the "
                                  "directory containing pod scripts. "
                                  "[default: \"%default\"]",
                                  default=getattr(config, 'POD_DIR',
                                                  "/etc/clive/pod/")),
         "exchange": make_option("-e", "--exchange", help="Name of the "
                                 "'exchange' to send messages to (see AMQP "
                                 "for details). [default: \"%default\"]",
                                 default=getattr(config, 'EXCHANGE', "clive")),
         "password": make_option("--password", help="Password to use for the "
                                 "queue connection (see AMQP for details). "
                                 "[default: \"%default\"]",
                                 default=getattr(config, 'QUEUE_PASSWORD', "")),
         "pod": make_option("-p", "--pod", help="Pod script to run. Can be "
                            "specified more than once. If no pods are "
                            "specified, all available pod scripts are run.",
                            action="append", default=[]),
         "queue": make_option("-q", "--queue", help="Name of the 'queue' to "
                              "send messages to (see AMQP for details). "
                              "[default: \"%default\"]",
                              default=getattr(config, 'QUEUE_NAME', "clive")),
         "timeout": make_option("-t", "--timeout", help="Maximum amount of "
                                "time (in seconds) to wait for a pod script to "
                                "return a result. [default: %default]",
                                type="int", default=getattr(config, 'POD_TIMEOUT', None)),
         "userid": make_option("-u", "--userid", help="User ID to use for the "
                               "queue connection (see AMQP for details). "
                               "[default: \"%default\"]",
                               default=getattr(config, 'QUEUE_USER', "clive")),
         "vhost": make_option("-v", "--vhost", help="Virtual host to connect to "
                              "on the queue host (see AMQP for details). "
                                 "[default: \"%default\"]",
                              default=getattr(config, 'QUEUE_VHOST', "clive"))}

COMMANDS={"pod": {"options": ["timeout", "directory", "pod"],
                  "usage": "usage: %prog pod [options] [-p pod ...]",
                  "help": "Execute specified pod scripts and print their output."},
          "publish": {"options": ["timeout", "directory", "pod", "exchange",
                                  "queue", "userid", "password", "vhost"],
                      "usage": "usage: %prog publish [options] queue_host [-p pod ...]",
                      "help": "Execute specified pod scripts and publish their "
                              "output to a queue over AMQP."}}

def get_parser(command):
    parser = OptionParser(usage=COMMANDS[command]["usage"], add_help_option=False)
    for option in COMMANDS[command]["options"]:
        parser.add_option(OPTIONS[option])
    return parser

def print_help(command=None):
    if command == "help":
        print "Usage: clive [general_options] <command> [command_options] command_arguments"
        print
        print "Commands:"
        print "  %s\n    %s" % ("help", "Print this help message and exit.")
        for command, opt in COMMANDS.iteritems():
            print "  %s\n    %s" % (command, opt["help"])
    else:
        parser = get_parser(command)
        parser.print_help()

def help_cmd():
    if len(sys.argv) < 3:
        print_help("help")
    else:
        print_help(sys.argv[2])
    return 0

def pod_cmd():
    parser = get_parser("pod")
    (options, args) = parser.parse_args(sys.argv[2:])
    json.dump(pod.load_pod_dir(dirname=options.directory,
                               timeout=options.timeout,
                               filter_fn=pod.get_pod_filter(options.pod)),
              sys.stdout, sort_keys=True, indent=4)
    return 0

def publish_cmd():
    parser = get_parser("publish")
    (options, args) = parser.parse_args(sys.argv[2:])
    if len(args) < 1:
        parser.error("You must provide a queue hostname to publish to!")
    exchange = Exchange(options.exchange, type="fanout")
    queue = Queue(options.queue, exchange)
    connection = BrokerConnection(hostname=args[0],
                                  userid=options.userid,
                                  password=options.password,
                                  virtual_host=options.vhost)
    channel = connection.channel()
    producer = Producer(channel, exchange)
    producer.publish(pod.load_pod_dir(dirname=options.directory,
                                      timeout=options.timeout,
                                      # The first arg is the queue hostname, the rest
                                      # will be pod names
                                      filter_fn=pod.get_pod_filter(options.pod)),
                     serializer="json", compression="zlib")
    return 0

def main():
    if len(sys.argv) == 1:
        command = "help"
    else:
        command = sys.argv[1]
    return getattr(sys.modules['clive.cli'], "%s_cmd" % command)()
