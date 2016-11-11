'''
Created on Feb 16, 2016

@author: dilin
'''

import os
import sys
import shutil,tarfile
from datetime import datetime
import json,boto
import uuid
import gzip
from logs.oidayLog import initializeDebugLogging
global logger
from utilities.fileUtilities import create_file
reload(sys)
sys.setdefaultencoding("utf-8")

logger = initializeDebugLogging("S3Utilities")

def mergeAllDayDataIntoLocalDailyFile(s3Location, localFile):
    '''
    Get all the files from one day folder and merge them into one file
    '''
    try:
        logger.debug('''>>> Enter mergeAllDayDataIntoOneFile, check location
             {s3Location}, and save to {localFile}'''.format(**locals()))  
        if (not s3Location.endswith('/')):
            raise  ValueError('the input URL %s is not a folder url ' % s3Location)
        filedList = ''
        s3Conn = boto.connect_s3()
        bucket = s3Location.split('//')[1].split('/')[0]
        folder = s3Location.split('//')[1].split('/',1)[1]
        logger.debug('bucket = %s, folder = %s' % (bucket,folder))
        buckets = s3Conn.get_bucket(bucket)
        keys = buckets.list(prefix=folder)
        count = 0
        create_file(localFile)
        with open(localFile, "a") as myfile:
            for item in keys:
                count += 1
                if item.name.endswith('txt'):
                    userid = item.name.split('_')[0].split('-')[-1]
                    value = item.get_contents_as_string()
                    if len(filedList) == 0:
                        filedList =  value.split('\n')[0]
                    for row in value.split('\n')[1:]:
                        if len(row) > 3:
                            #only focus on the last 24 columns
                            newRow = ','.join(row.split(',')[-24:])
                            #folder.split('/')[0] is the ds
                            myfile.write(folder.split('/')[0]+','+userid+ ','+newRow + '\n')
        logger.debug('<<< Exit checkFolderExistInS3, find %s item in the folder' % count) 
        return filedList
    except Exception, e:
        logger.error('!!!!!! Error in checkFolderExistInS3'+str(e)) 
        raise e 
