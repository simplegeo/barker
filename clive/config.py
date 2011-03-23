from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_FILE = '/dev/null'
LOG_LEVEL = WARNING

POD_DIR = '/usr/share/barker/pods'
POD_TIMEOUT = 15

CONSOLE_LOG = True

EXCHANGE = "barker"
QUEUE_NAME = "barker"
QUEUE_USER = "barker"
QUEUE_PASSWORD = "barker_secret"
QUEUE_VHOST = "/barker"

try:
    execfile('/etc/barker/config.py')
except IOError:
    pass
