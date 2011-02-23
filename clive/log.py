# Clive is Copyright 2011 SimpleGeo, Inc.
# Written by Paul Lathrop <paul@simplegeo.com>

import logging
import logging.handlers
import clive.config as config

logger = logging.getLogger('clive')
logger.setLevel(config.LOG_LEVEL)
logger.addHandler(logging.handlers.RotatingFileHandler(config.LOG_FILE,
                                                    maxBytes=config.LOG_MAX_BYTES,
                                                    backupCount=config.LOG_COUNT))
