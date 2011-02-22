# Clive is Copyright 2011 SimpleGeo, Inc.
# Written by Paul Lathrop <paul@simplegeo.com>

import logging
import logging.handlers
import clive.config as config

LOG_FILE = config.LOG_FILE
logger = logging.getLogger('clive')
LOG.setLevel(config.LOG_LEVEL)
LOG.addHandler(logging.handlers.RotatingFileHandler(LOG_FILE,
                                                    maxBytes=config.LOG_MAX_BYTES,
                                                    backupCount=config.LOG_COUNT))
