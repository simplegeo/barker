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

def load_pod_dir(dirname=config.POD_DIR, timeout=None, filter_fn=None):
    """Concurrently loads the pod files in the given directory and
    returns a dict containing their output."""
    if dirname[-1] != os.sep:
        dirname += os.sep
        LOGGER.info("Appended file separator to specified pod dir %s",
                    dirname)
    pool = eventlet.GreenPool()
    LOGGER.debug("Loading pod files from directory %s with timeout %s",
                 dirname, timeout)
    return dict(ifilter(filter_fn, pool.imap(partial(load_pod, timeout=timeout),
                                             get_pod_files(dirname))))

def get_pod_filter(pods):
    if len(pods) == 0:
        def pod_fn(pod):
            return pod[1] != {} # Filter out empty pods
        return pod_fn
    else:
        def pod_fn(pod):
            # Filter out empty pods and those which were not specified.
            return pod[1] != {} and os.path.basename(pod[0]) in pods
        return pod_fn
