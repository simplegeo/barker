from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_FILE = '/tmp/clive.log'
LOG_LEVEL = DEBUG
LOG_MAX_BYTES = 100000000
LOG_COUNT = 5

DATUM_DIR = '/tmp/datum'
DATUM_TIMEOUT = '15'

try:
    execfile('/etc/clive/config.py')
except IOError:
    pass
