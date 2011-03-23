Barker is a hive mind for your clusters. But what the hell does that
mean? Well, barker is intended to be a suite of pluggable tools which
integrate together nicely to help you manage groups of servers.

The first component of barker is the PoD system. A "pod" is simply a
piece of data; specifically metadata about a host or set of
hosts. Pods are scripts written in the language of your choice that
output JSON. Barker loads these pods on the fly to output
(JSON-formatted) information about a given host.

Barker is capable of publishing the collected output of Pods as
messages on an AMQP queue. See ``barker help publish`` for more
information.

For now that is all, but there is definitely more to come! Barker is
under active development and will change very frequently. You probably
don't want to use it yet!

Installation
============
For now, clone the repo, set up a virtualenv, and ``python setup.py
develop``. There will be a real installation some day.

Configuration
=============
Barker loads ``barker/config.py`` in the repo directory, then loads
``/etc/barker/config.py`` if it exists. These are python files and must
be written following python syntax. Configuration parameters are:

``LOG_FILE``
  Path to the file which barker will log to.

``LOG_LEVEL``
  Tune the verbosity of logging. Can be one of ``DEBUG``, ``INFO``,
  ``WARNING``, ``ERROR``, ``CRITICAL``

``POD_DIR``
  The directory containing PoD scripts for barker to load.

``POD_TIMEOUT``
  Amount of time an individual PoD script can run before barker skips
  that PoD.

``CONSOLE_LOG``
  Boolean controlling whether barker outputs logs to the console as
  well as its log file. Can be one of ``True`` or ``False``

``EXCHANGE``
  Name of the exchange that ``barker-publish-pod`` will publish to.

``QUEUE_NAME``
  Name of the queue that ``barker-demo-listener`` will pull messages
  from.

``QUEUE_USER``
  AMQP username to use when connecting to the queue service.

``QUEUE_PASSWORD``
  Password used to authenticate to the queue service.

``QUEUE_VHOST``
  AMQP virtual host to use when connecting to the queue service.

Usage
=====
``barker help [command]``
  Prints out a help message and exits. If a command is specified,
  prints specific usage help for that barker command.

``barker pod [options ...] [-p pod ...]``
  Loads the specified PoD scripts (loads all by default) and outputs a
  JSON hash containing their individual data.

``barker publish [options ...] queue_hostname [-p pod ...]``
  Connects to the specified queue host and publishes the specified
  pod(s) (or all of them if none are specified) to a fanout
  exchange. If no listeners are attached to the associated queues; the
  messages will be dropped.

Examples
========
``examples/demo-listener.py``
  Connects to the specified queue host and waits for a single pod
  message, prints it out, acknowledges it, and exits. This is just a
  demo for how you might listen for pod information on the queue.
