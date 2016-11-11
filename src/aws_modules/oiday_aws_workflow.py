from logs.oidayLog import initializeDebugLogging
from datetime import datetime, timedelta, date
from aws_modules.awsUtilities.s3Utilities import mergeAllDayDataIntoLocalDailyFile
from utilities.mySqlUtilities import createDailyTable, createDailyTable_runtime, query_update,deleteCurrentDs, insertCurrentDs
from utilities.fileUtilities import remove_file

global logger



logger = initializeDebugLogging("AWS_WF")

def daterange(d1, d2):
	return (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))

def run_oiday_aws_workflow(startDate, endDate, s3Location):
	logger.debug('''start checking variables: startDate = {startDate}, endDate={endDate},s3Location={s3Location}'''.format(**locals()))
	sDate = datetime.strptime(startDate, '%Y-%m-%d')
	eDate = datetime.strptime(endDate, '%Y-%m-%d')
	allS3Folders = []	

	for d in daterange(sDate, eDate):
		currentDate = d.strftime('%d-%m-%Y')
		logger.debug(currentDate)
		s3Folder = 's3://' + s3Location + '/' + currentDate + '/'
		logger.debug('s3Folder is: ' + s3Folder)
		allS3Folders.append(s3Folder)
	
	logger.debug('start processing :' + ','.join(allS3Folders))

	for dailyFolder in allS3Folders:
		logger.debug('>>> Start the date: ' + dailyFolder)
		processDate = dailyFolder.split('/')[-2]
		localFile = '/var/tmp/' + processDate + '.txt'
		filedList = mergeAllDayDataIntoLocalDailyFile(dailyFolder,localFile)
		logger.debug('exported to file ' + localFile)
		createStatement = createDailyTable("_".join(processDate.split('-')[1:]), 'aws')
		query_update(createStatement)
		deleteStatement = deleteCurrentDs("_".join(processDate.split('-')[1:]), processDate,'aws')
		query_update(deleteStatement)
		insertStatement = insertCurrentDs("_".join(processDate.split('-')[1:]), localFile, 'aws')
		query_update(insertStatement)
        remove_file(localFile)
        logger.debug('<<< Finish the date: ' + processDate)
