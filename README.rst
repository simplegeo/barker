Clive is a hive mind for your clusters. But what the hell does that
mean? Well, clive is intended to be a suite of pluggable tools which
integrate together nicely to help you manage groups of servers.

The first component of clive is the PoD system. A "pod" is simply a
piece of data; specifically metadata about a host or set of
hosts. Pods are scripts written in the language of your choice that
output JSON. Clive loads these pods on the fly to output
(JSON-formatted) information about a given host.

For now that is all, but there is definitely more to come!

Installation
============
For now, clone the repo, set up a virtualenv, and ``python setup.py
develop``. There will be a real installation some day.

Configuration
=============
Clive loads ``clive/config.py`` in the repo directory, then loads
``/etc/clive/config.py`` if it exists. These are python files and must
be written following python syntax. Configuration parameters are:

``LOG_FILE``
  Path to the file which clive will log to.

``LOG_LEVEL``
  Tune the verbosity of logging. Can be one of ``DEBUG``, ``INFO``,
  ``WARNING``, ``ERROR``, ``CRITICAL``

``POD_DIR``
  The directory containing PoD scripts for clive to load.

``POD_TIMEOUT``
  Amount of time an individual PoD script can run before clive skips
  that PoD.

``CONSOLE_LOG``
  Boolean controlling whether clive outputs logs to the console as
  well as its log file. Can be one of ``True`` or ``False``

Usage
=====
``clive-pod [pod ...]``
  Loads the specified PoD scripts (loads all by default) and outputs a
  JSON hash containing their individual data.
