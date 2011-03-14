from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_FILE = '/dev/null'
LOG_LEVEL = WARNING

POD_DIR = '/Users/plathrop/tmp/pod'
POD_TIMEOUT = 15

CONSOLE_LOG = True

EXCHANGE = "clive"
QUEUE_NAME = "clive"
QUEUE_USER = "clive"
QUEUE_PASSWORD = "clive_secret"
QUEUE_VHOST = "/clive"

try:
    execfile('/etc/clive/config.py')
except IOError:
    pass
