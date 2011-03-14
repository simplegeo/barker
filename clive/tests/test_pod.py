# Clive is Copyright 2011 SimpleGeo, Inc.
# Written by Paul Lathrop <paul@simplegeo.com>

try:
    import simplejson as json
except ImportError:
    import json
import os
import time

from mock import patch, Mock, MagicMock, mocksignature
from nose.tools import assert_equals

import clive

FAKE_POD_OUTPUT = {"test-pod1.sh": {"shfoo": "shbar"},
                   "test-pod2.py": {"pyfoo": "pybar"},
                   "test-pod3.rb": {"rbfoo": "rbbar"}}

FAKE_POD_SUBSET = {"test-pod1.sh": {"shfoo": "shbar"},
                   "test-pod3.rb": {"rbfoo": "rbbar"}}

def test_load_pod_with_errors():
    for klass in [OSError, ValueError, TypeError]:
        yield check_load_pod_with_error, klass

@patch("clive.pod.subprocess.Popen")
def check_load_pod_with_error(klass, mock_popen):
    mock_popen.side_effect = klass('testing load_pod with %s' % klass)
    assert clive.pod.load_pod("/nonexistent_pod") == ()

# I'd test the case where executing the pod exceeds the timeout, but
# as far as I can tell that test is fucking impossible.

@patch("clive.pod.subprocess.Popen")
def test_load_pod(mock_popen):
    mock_popen.return_value = Mock()
    mock_communicate = mock_popen.return_value.communicate
    mock_communicate.return_value = MagicMock()
    mock_communicate.return_value.__getitem__.return_value = json.dumps(FAKE_POD_OUTPUT["test-pod1.sh"])
    assert_equals(clive.pod.load_pod("test-pod1.sh"),
                  ("test-pod1.sh", {u"shfoo": u"shbar"}))

def test_executable_p():
    for truth in [("executable directory", True, True, False),
                  ("executable file", True, False, True),
                  ("non-executable directory", False, True, False),
                  ("non-executable file", False, False, False)]:
        yield check_executable_file_p, truth

def check_executable_file_p(truth):
    mock_os_access = Mock(return_value = truth[1])
    mock_os_path_isdir = Mock(return_value = truth[2])
    with patch.object(clive.pod.os, 'access', mock_os_access):
        with patch.object(clive.pod.os.path, 'isdir', mock_os_path_isdir):
            print "testing with %s" % truth[0]
            assert_equals(clive.pod.executable_file_p("/nonexistent"), truth[3])

def test_get_pod_files():
    mock_os_listdir = Mock(return_value = ['foo', 'bar', 'baz'])
    mock_pod_executable_file_p = mocksignature(clive.pod.executable_file_p)
    mock_pod_executable_file_p.return_value = True
    with patch.object(clive.pod.os, 'listdir', mock_os_listdir):
        with patch.object(clive.pod, "executable_file_p", mock_pod_executable_file_p):
            assert_equals(list(clive.pod.get_pod_files('/clive-tests')),
                          ['/clive-tests/foo', '/clive-tests/bar', '/clive-tests/baz'])

def test_load_pod_dir():
    mock_eventlet_greenpool = Mock()
    mock_imap = mock_eventlet_greenpool.return_value.imap
    mock_imap.return_value = FAKE_POD_OUTPUT.iteritems()
    with patch.object(clive.pod.eventlet, 'GreenPool', mock_eventlet_greenpool):
        assert_equals(clive.pod.load_pod_dir(), FAKE_POD_OUTPUT)

def test_load_pod_subset():
    mock_eventlet_greenpool = Mock()
    mock_imap = mock_eventlet_greenpool.return_value.imap
    mock_imap.return_value = FAKE_POD_SUBSET.iteritems()
    with patch.object(clive.pod.eventlet, 'GreenPool', mock_eventlet_greenpool):
        assert_equals(clive.pod.load_pod_dir(filter_fn=clive.pod.get_pod_filter(["test-pod1.sh", "test-pod3.rb"])),
                      FAKE_POD_SUBSET)
