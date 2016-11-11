#!/usr/bin/python
# -*- coding: utf-8 -*-
# flake8: noqa

from logs.oidayLog import initializeDebugLogging
from datetime import datetime, timedelta, date
from utilities.mySqlUtilities import createDailyTable, createDailyTable_runtime, query_update,deleteCurrentDs, insertCurrentDs
from utilities.fileUtilities import remove_file, create_file
from configs import constants
import qiniu
import requests
import json
import sys 


logger = initializeDebugLogging("QiniuUtilities")


def mergeAllDayDataIntoLocalDailyFile(qiniuLocation, qiniuDate, localFile):
    '''
    Get all the files from one day folder and merge them into one file
    '''
    try:
        logger.debug('''>>> Enter mergeAllDayDataIntoOneFile, check location
             {qiniuLocation}, and save to {localFile}'''.format(**locals()))
        logger.debug('Start get auth')
        q = qiniu.Auth(constants.QINIU_AK(), constants.QINIU_SK())
        logger.debug('finish get auth')
        count = 0 
        fileCount = 0       
        create_file(localFile)
        marker = None
        eof = False
        while not eof:
            ret, eof, info = qiniu.BucketManager(q).list(qiniuLocation,qiniuDate,marker=marker)
            marker = ret.get('marker', None)
            allDayTexts = json.loads(info.text_body).get('items')
            logger.debug('find %s files' % str(len(allDayTexts)))
            fileCount += len(allDayTexts)
            with open(localFile, "a") as myfile:
                finished = 0
                for dayText in allDayTexts:
                    key = dayText.get('key')
                    url = 'http://{domain}/{key}'.format(domain=constants.QINIU_PUBLIC_DOMAIN_NAME(), key=key)
                    logger.debug('----------finised :' + str(finished))
                    finished += 1
                    if url.endswith('txt'):
                        userid = url.split('_')[0].split('-')[-1]
                        private_url = q.private_download_url(url, expires=3600)
                        r = requests.get(private_url) 
                        r.encoding='utf-8'
                        for row in r.text.split('\n')[1:]:
                    	   if len(row) > 3:
                                count += 1
                        	   #only focus on the last 24 columns
                                newRow = ','.join(row.split(',')[-24:]).decode('utf-8')
                                #folder.split('/')[0] is the ds
                                myfile.write(qiniuDate + ',' + userid + ',' + 
                            	   newRow + '\n')
            logger.debug('done one iteration')
        logger.debug('''<<< Exit mergeAllDayDataIntoLocalDailyFile, 
        	find %s item in the folder''' % count)
    except Exception, e:
        logger.error('!!!!!! Error in checkFolderExistInQiniu'+str(e)) 
        raise e 
