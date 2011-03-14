# Clive is Copyright 2011 SimpleGeo, Inc.
# Written by Paul Lathrop <paul@simplegeo.com>

import logging
from optparse import OptionParser
import sys

from kombu import BrokerConnection, Exchange, Queue, Producer, Consumer

import clive.config as config
from clive.pod import load_pod_dir, get_pod_filter

LOGGER = logging.getLogger('clive.publish')

def clive_publish_pod_cmd():
    try:
        default_timeout = config.POD_TIMEOUT
    except AttributeError:
        default_timeout = None
    try:
        default_pod_dir = config.POD_DIR
    except AttributeError:
        default_pod_dir = "/etc/clive/pod/"
    parser = OptionParser(usage="usage: %prog [options] queue_host [pod...]")
    parser.add_option("-t", "--timeout", help="Maximum amount of time to wait "
                      "for a pod script to return a result.", type="int")
    parser.add_option("-d", "--directory",
                      help="Path to the directory containing pod scripts.")
    parser.add_option("-e", "--exchange", help="Name of the 'exchange' to "
                      "send messages to (see AMQP for details). Defaults to "
                      "\"%s\"" % config.EXCHANGE)
    parser.add_option("-q", "--queue", help="Name of the 'queue' to "
                      "send messages to (see AMQP for details). Defaults to "
                      "\"%s\"" % config.QUEUE_NAME)
    parser.add_option("-u", "--userid", help="User ID to use for the queue "
                      "connection (see AMQP for details). Defaults to "
                      "\"%s\"" % config.QUEUE_USER)
    parser.add_option("-p", "--password", help="Password to use for the "
                      "queue connection (see AMQP for details). Defaults to "
                      "\"%s\"" % config.QUEUE_PASSWORD)
    parser.add_option("-v", "--vhost", help="Virtual host to connect to "
                      "on the queue host (see AMQP for details). Defaults to "
                      "\"%s\"" % config.QUEUE_VHOST)
    parser.set_defaults(timeout=default_timeout,
                        directory=default_pod_dir,
                        exchange=config.EXCHANGE,
                        queue=config.QUEUE_NAME,
                        userid=config.QUEUE_USER,
                        password=config.QUEUE_PASSWORD,
                        vhost=config.QUEUE_VHOST)
    (options, args) = parser.parse_args()
    if len(args) < 1:
        sys.stderr.write("Must provide a queue host!\n")
        sys.exit(1)
    exchange = Exchange(options.exchange, type="fanout")
    queue = Queue(options.queue, exchange)
    connection = BrokerConnection(hostname=args[0],
                                  userid=options.userid,
                                  password=options.password,
                                  virtual_host=options.vhost)
    channel = connection.channel()
    producer = Producer(channel, exchange)
    producer.publish(load_pod_dir(dirname=default_pod_dir,
                                  timeout=options.timeout,
                                  # The first arg is the queue hostname, the rest
                                  # will be pod names
                                  filter_fn=get_pod_filter(args[1:])),
                     serializer="json", compression="zlib")

# Callback function for the demo listener.
def demo_listen_and_print(body, message):
    print("Received message: \n%r" % (body, ))
    message.ack()

def clive_demo_listener_cmd():
    try:
        default_timeout = config.POD_TIMEOUT
    except AttributeError:
        default_timeout = None
    try:
        default_pod_dir = config.POD_DIR
    except AttributeError:
        default_pod_dir = "/etc/clive/pod/"
    parser = OptionParser(usage="usage: %prog [options] queue_host")
    parser.add_option("-e", "--exchange", help="Name of the 'exchange' to "
                      "send messages to (see AMQP for details). Defaults to "
                      "\"%s\"" % config.EXCHANGE)
    parser.add_option("-q", "--queue", help="Name of the 'queue' to "
                      "send messages to (see AMQP for details). Defaults to "
                      "\"%s\"" % config.QUEUE_NAME)
    parser.add_option("-u", "--userid", help="User ID to use for the queue "
                      "connection (see AMQP for details). Defaults to "
                      "\"%s\"" % config.QUEUE_USER)
    parser.add_option("-p", "--password", help="Password to use for the "
                      "queue connection (see AMQP for details). Defaults to "
                      "\"%s\"" % config.QUEUE_PASSWORD)
    parser.add_option("-v", "--vhost", help="Virtual host to connect to "
                      "on the queue host (see AMQP for details). Defaults to "
                      "\"%s\"" % config.QUEUE_VHOST)
    parser.set_defaults(exchange=config.EXCHANGE,
                        queue=config.QUEUE_NAME,
                        userid=config.QUEUE_USER,
                        password=config.QUEUE_PASSWORD,
                        vhost=config.QUEUE_VHOST)
    (options, args) = parser.parse_args()
    if len(args) < 1:
        sys.stderr.write("Must provide a queue host!\n")
        sys.exit(1)
    exchange = Exchange(options.exchange, type="fanout")
    queue = Queue(options.queue, exchange)
    connection = BrokerConnection(hostname=args[0],
                                  userid=options.userid,
                                  password=options.password,
                                  virtual_host=options.vhost)
    channel = connection.channel()
    consumer = Consumer(channel, queue, callbacks=[demo_listen_and_print])
    consumer.consume()
    connection.drain_events()
