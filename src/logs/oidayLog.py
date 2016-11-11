#!/user/bin/python

import logging
from configs.constants import LOG_FILE_GENERAL

def initializeDebugLogging(className):
    logger = logging.getLogger(className)
    logger.setLevel(logging.DEBUG)
    hdlr = logging.FileHandler(LOG_FILE_GENERAL())
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(lineno)d : %(message)s')
    hdlr.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.addHandler(ch)
    return logger