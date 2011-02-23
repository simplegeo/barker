# Clive is Copyright 2011 SimpleGeo, Inc.
# Written by Paul Lathrop <paul@simplegeo.com>

import logging
import os
from itertools import imap, ifilter
from functools import partial
try:
    import simplejson as json
except ImportError:
    import json

import eventlet
from eventlet.green import subprocess

import clive.config as config

LOGGER = logging.getLogger('clive.datum')

def get_datum_output(filename):
    """Executes a 'datum' file (an executable file which should output
    JSON to stdout) and returns the output."""
    LOGGER.debug("Executing datum file %s", filename)
    return subprocess.Popen([filename], stdout=subprocess.PIPE).communicate()[0]

def load_datum(filename, timeout=30):
    """Attempts to execute a datum file, possibly with a timeout, and
    parse the output as JSON. If the execution times out or an error
    is encountered during execution, or if the output is not valid
    JSON, this will return an empty dict."""
    datum = ()
    with eventlet.Timeout(timeout, False):
        try:
            LOGGER.debug("Executing and parsing datum %s with timeout %s",
                         filename, timeout)
            datum = (os.path.basename(filename), json.loads(get_datum_output()))
        except OSError, exc:
            LOGGER.warning("OSError while executing datum plugin %s,"
                           "ignoring datum!", filename)
            LOGGER.debug(exc)
        except (ValueError, TypeError), exc:
            LOGGER.warning("Error while parsing output from datum plugin %s, "
                           "ignoring datum!", filename)
            LOGGER.debug(exc)
    if not datum:
        LOGGER.warning("Timed out while executing datum plugin %s,"
                       "ignoring datum!", filename)
    return datum

def executablep(filename):
    """Predicate to check if a given file is executable."""
    LOGGER.debug("Checking if %s is executable", filename)
    return os.access(filename, os.X_OK)

def get_datum_files(dirname):
    """Returns the fully-qualified paths for the list of executable
    files in the specified directory. Does not recurse into
    subdirectories."""
    LOGGER.debug("Locating executable files in datum directory %s", dirname)
    return ifilter(executablep, imap(partial(os.path.join, dirname),
                                    os.listdir(dirname)))

def load_datum_dir(dirname=config.DATUM_DIR, timeout=config.DATUM_TIMEOUT):
    """Concurrently loads the datum files in the given directory and
    returns a dict containing their output."""
    if dirname[-1] != os.sep:
        dirname += os.sep
        LOGGER.info("Appended file separator to specified datum dir %s",
                    dirname)
    pool = eventlet.GreenPool()
    LOGGER.debug("Loading datum files from directory %s with timeout %s",
                 dirname, timeout)
    return dict(ifilter(None, pool.imap(partial(load_datum, timeout=timeout), get_datum_files(dirname))))
