#!/usr/bin/python
# -*- coding: utf-8 -*-
# flake8: noqa
from logs.oidayLog import initializeDebugLogging
from datetime import datetime, timedelta, date
from utilities.mySqlUtilities import createDailyTable, createDailyTable_runtime, query_update,deleteCurrentDs, insertCurrentDs
from utilities.fileUtilities import remove_file
from configs import constants
from qiniu_modules.qiniuUtilities.qiniuUtilities import mergeAllDayDataIntoLocalDailyFile
from utilities.mySqlUtilities import createDailyTable, createDailyTable_runtime, query_update,deleteCurrentDs, insertCurrentDs
from utilities.fileUtilities import remove_file

global logger

logger = initializeDebugLogging("QN_WF")

def daterange(d1, d2):
	return (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))

def run_oiday_qiniu_workflow(startDate, endDate, qiniuLocation):
	logger.debug('''start checking variables: startDate = {startDate},
		endDate={endDate},qiniuLocation={qiniuLocation}'''.format(**locals()))
	sDate = datetime.strptime(startDate, '%Y-%m-%d')
	eDate = datetime.strptime(endDate, '%Y-%m-%d')
	allDateFolders = []	

	for d in daterange(sDate, eDate):
		currentDate = d.strftime('%d-%m-%Y')
		logger.debug(currentDate)
		allDateFolders.append(currentDate)

	logger.debug('start processing :' + ','.join(allDateFolders))
		
	for dailyFolder in allDateFolders:
		logger.debug('>>> Start the date: ' + dailyFolder)
		processDate = dailyFolder
		localFile = '/var/tmp/' + processDate + '.txt'
		mergeAllDayDataIntoLocalDailyFile(qiniuLocation, 
			dailyFolder,localFile)
		logger.debug('exported to file ' + localFile)
		createStatement = createDailyTable("_".join(dailyFolder.split('-')[1:]), 'qiniu')
		query_update(createStatement)
		deleteStatement = deleteCurrentDs("_".join(processDate.split('-')[1:]), processDate, 'qiniu')
		query_update(deleteStatement)
		insertStatement = insertCurrentDs("_".join(processDate.split('-')[1:]), localFile, 'qiniu', constants.LOAD_DATA_CHARACTER_SET())
		query_update(insertStatement)
        #remove_file(localFile)
        #logger.debug('<<< Finish the date: ' + processDate)
