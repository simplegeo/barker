from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_FILE = '/dev/null'
LOG_LEVEL = WARNING
LOG_MAX_BYTES = 100000000
LOG_COUNT = 5

POD_DIR = '/Users/plathrop/tmp/pod'
POD_TIMEOUT = 15

CONSOLE_LOG = True

try:
    execfile('/etc/clive/config.py')
except IOError:
    pass
