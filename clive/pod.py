# Clive is Copyright 2011 SimpleGeo, Inc.
# Written by Paul Lathrop <paul@simplegeo.com>

import logging
import os
from itertools import imap, ifilter
from functools import partial
from optparse import OptionParser
try:
    import simplejson as json
except ImportError:
    import json

import eventlet
from eventlet.green import subprocess

import clive.config as config

LOGGER = logging.getLogger('clive.pod')

def load_pod(filename, timeout=None):
    """Attempts to execute a pod file, possibly with a timeout, and
    parse the output as JSON. If the execution times out or an error
    is encountered during execution, or if the output is not valid
    JSON, this will return an empty tuple. Otherwise, it will return
    a tuple: (filename, parsed_output)"""
    pod = ()
    with eventlet.Timeout(timeout, None):
        try:
            LOGGER.debug("Executing and parsing pod %s with timeout %s",
                         filename, timeout)
            proc = subprocess.Popen([filename], stdout=subprocess.PIPE)
            pod = (os.path.basename(filename), json.loads(proc.communicate()[0]))
        except (OSError, ValueError, TypeError), ex:
            LOGGER.warning("Error executing pod plugin %s, ignoring pod!",
                           filename)
            LOGGER.debug(ex)
        except eventlet.Timeout:
            LOGGER.warning("Timed out while executing pod plugin %s,"
                           "ignoring pod!", filename)
            proc.kill()
    return pod

def executable_file_p(filename):
    """Predicate to check if a given file is executable."""
    result =  os.access(filename, os.X_OK) and not os.path.isdir(filename)
    if result:
        LOGGER.debug("%s is an executable file", filename)
    else:
        LOGGER.debug("%s is not an executable file", filename)
    return result

def get_pod_files(dirname):
    """Returns the fully-qualified paths for the list of executable
    files in the specified directory. Does not recurse into
    subdirectories."""
    LOGGER.debug("Locating executable files in pod directory %s", dirname)
    return ifilter(executable_file_p, imap(partial(os.path.join, dirname),
                                           os.listdir(dirname)))

def load_pod_dir(dirname=config.POD_DIR, timeout=None):
    """Concurrently loads the pod files in the given directory and
    returns a dict containing their output."""
    if dirname[-1] != os.sep:
        dirname += os.sep
        LOGGER.info("Appended file separator to specified pod dir %s",
                    dirname)
    pool = eventlet.GreenPool()
    LOGGER.debug("Loading pod files from directory %s with timeout %s",
                 dirname, timeout)
    return dict(ifilter(None, pool.imap(partial(load_pod, timeout=timeout), get_pod_files(dirname))))

def load_pod_subset(pods, dirname=config.POD_DIR, timeout=None):
    """Concurrently loads only the specified pod files in the given
    directory and returns a dict containing their output."""
    if dirname[-1] != os.sep:
        dirname += os.sep
        LOGGER.info("Appended file separator to specified pod dir %s",
                    dirname)
    pool = eventlet.GreenPool()
    LOGGER.debug("Loading specified pod files from directory %s with"
                 "timeout %s", dirname, timeout)
    return dict(ifilter(None, pool.imap(partial(load_pod, timeout=timeout),
                                        ifilter(lambda p: os.path.basename(p) in pods,
                                                get_pod_files(dirname)))))

def clive_pod_cmd():
    try:
        default_timeout = config.POD_TIMEOUT
    except AttributeError:
        default_timeout = None
    try:
        default_pod_dir = config.POD_DIR
    except AttributeError:
        default_pod_dir = "/etc/clive/pod/"
    parser = OptionParser(usage="usage: %prog [options] [pod...]")
    parser.add_option("-t", "--timeout", help="Maximum amount of time to wait "
                      "for a pod script to return a result.", type="int")
    parser.add_option("-d", "--directory",
                      help="Path to the directory containing pod scripts.")
    parser.set_defaults(timeout=default_timeout,
                        directory=default_pod_dir)
    (options, args) = parser.parse_args()
    if len(args) > 0:
        print json.dumps(load_pod_subset(args, dirname=default_pod_dir, timeout=options.timeout), sort_keys=True, indent=4)
    else:
        print json.dumps(load_pod_dir(dirname=default_pod_dir, timeout=options.timeout), sort_keys=True, indent=4)
