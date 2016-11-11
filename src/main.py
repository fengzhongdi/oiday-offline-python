#!/usr/bin/python
# -*- coding: utf-8 -*-
# flake8: noqa
"""Program entry point"""

from __future__ import print_function

import argparse
import sys
import os
sys.dont_write_bytecode = True
sys.path.append("%s/" % os.path.dirname(os.path.abspath(__file__)))
import metadata
from logs.oidayLog import initializeDebugLogging
from aws_modules.oiday_aws_workflow import run_oiday_aws_workflow
from qiniu_modules.oiday_qiniu_workflow import run_oiday_qiniu_workflow
global logger

logger = initializeDebugLogging("Main")

def main(argv):
    """Program entry point.

    :param argv: command-line arguments
    :type argv: :class:`list`
    """
    author_strings = []
    for name, email in zip(metadata.authors, metadata.emails):
        author_strings.append('Author: {0} <{1}>'.format(name, email))

    epilog = '''
{project} {version}

{authors}
URL: <{url}>
'''.format(
        project=metadata.project,
        version=metadata.version,
        authors='\n'.join(author_strings),
        url=metadata.url)

    arg_parser = argparse.ArgumentParser(
        prog=argv[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=metadata.description,
        epilog=epilog)
    arg_parser.add_argument(
        '-V', '--version',
        action='version',
        version='{0} {1}'.format(metadata.project, metadata.version))
    arg_parser.add_argument('-s', '--startDate', help="Log start date", required=True)
    arg_parser.add_argument('-e', '--endDate', help="Log end date",required=True, default="common")
    arg_parser.add_argument('-s3l', '--s3Location', help="S3 file lcoation", default="iday")
    arg_parser.add_argument('-qnl', '--quniuLocation', help="Qiniu file lcoation", default="oiday")
    arg_parser.add_argument('-c', '--configurationPath', help="Configuration path", default="/var/conf")
    arg_parser.add_argument('-o', '--option', help="Option", choices=["ibeFullRefresh", "fpFullRefresh", "ibeCookieRefresh", "fpDailyUpdate","liteUser"])
    arg_parser.add_argument('-scl', '--schemaList', help="A list of schemas, use comma delimiter",default="")
    arg_parser.add_argument('-t', '--task', help="Type of task", choices=['aws', 'qiniu'])
    
    inputValues = vars(arg_parser.parse_args(args=argv[1:]))

    startDate = inputValues["startDate"]
    endDate = inputValues["endDate"]
    s3Location = inputValues["s3Location"]
    option = inputValues["option"]
    task = inputValues["task"]
    qiniuLocation = inputValues["quniuLocation"]

    logger.debug('''Start task: startDate = %s, endDate = %s, s3Location = %s, option = %s, task = %s
    '''% (startDate, endDate, s3Location, option, task))

    if task == 'aws':
        logger.debug(">>>start aws workflow")
        run_oiday_aws_workflow(startDate, endDate, s3Location)
        logger.debug(">>>exit aws workflow")
    elif task == 'qiniu':
        logger.debug(">>>start qiniu workflow")
        run_oiday_qiniu_workflow(startDate, endDate, qiniuLocation)
        logger.debug(">>>exit qiniu workflow")
    else :
        logger.debug(">>>Do nothing, task is {task}".format(**locals()))
    logger.debug('<<<<<<<<<<<Finish task!')
    return 0


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()

