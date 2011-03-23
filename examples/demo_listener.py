#!/usr/bin/env python
# Barker is Copyright 2011 SimpleGeo, Inc.
# Written by Paul Lathrop <paul@simplegeo.com>

from optparse import OptionParser
import sys

from kombu import BrokerConnection, Exchange, Queue, Producer, Consumer

import barker.config as config
from barker.pod import load_pod_dir, get_pod_filter

# Callback function for the demo listener.
def demo_listen_and_print(body, message):
    print("Received message: \n%r" % (body, ))
    message.ack()

if __name__ == '__main__':
    # TODO: Clean this craziness up!
    default_timeout = getattr(config, POD_TIMEOUT, None)
    default_pod_dir = getattr(config, POD_DIR, "/etc/barker/pod/")
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
