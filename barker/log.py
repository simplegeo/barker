# Barker is Copyright 2011 SimpleGeo, Inc.
# Written by Paul Lathrop <paul@simplegeo.com>

import logging
import logging.handlers
import barker.config as config

logger = logging.getLogger('barker')
logger.setLevel(config.LOG_LEVEL)

logfile_handler = logging.handlers.WatchedFileHandler(config.LOG_FILE)
logfile_handler.setLevel(config.LOG_LEVEL)
logfile_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logfile_handler.setFormatter(logfile_formatter)
logger.addHandler(logfile_handler)

if config.CONSOLE_LOG:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.LOG_LEVEL)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
