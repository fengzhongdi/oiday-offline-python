#!/usr/bin/python
import  os.path
from logs.oidayLog import initializeDebugLogging
from subprocess import Popen, PIPE, sys
import traceback

global logger

logger = initializeDebugLogging("systemCommand")

def run_command(cmd):
    try:
        if '-u' not in cmd and '-p' not in cmd:
            logger.debug('execute command: %s' % cmd)
        else:
            logger.debug('execute command: hide command for sensitive data')
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        p.wait()
        if (p.returncode != None) and (p.returncode != 0):
            message = 'cmd = %s, p.returncode=%s, p.stdout.read() is %s' % (cmd, p.returncode, p.stdout.read())
            logger.error('The following command did not run successfully:\n\t%s' % message)
            raise SyntaxError('The following command did not run successfully:\n\t%s' % cmd)
        return p.stdout.read()
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e