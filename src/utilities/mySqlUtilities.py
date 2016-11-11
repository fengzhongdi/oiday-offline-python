#!/usr/bin/python
import  os.path
from logs.oidayLog import initializeDebugLogging
from sysUtilities import run_command

global logger

logger = initializeDebugLogging("mySqlUtility")

def loadFileToTable(filePath):
    return os.path.isfile(filePath)
	
def createDailyTable(currentMonth,product_type):
	return '''create table IF NOT EXISTS oiday.oiday_offline_daily_{product_type}_{currentMonth} like oiday.oiday_offline_daily_template;'''.format(**locals())

def createDailyTable_runtime(currentDate, fields):
	colStr = ''' ''';
	for field in fields:
		colStr += '''
		{field} varchar(64),'''.format(**locals())
	colStr = colStr[:-1]
	print(colStr)
	sql = '''create table IF NOT EXISTS oiday.oiday_offline_daily_{currentDate} ({colStr})'''.format(**locals())
	return sql

def deleteCurrentDs(currentMonth, currentDate, product_type):
	return '''delete from oiday.oiday_offline_daily_{product_type}_{currentMonth} where ds = '{currentDate}' ; commit; '''.format(**locals())

def insertCurrentDs(currentMonth, localfile, product_type, characterSet='', delimiter=','):
	table = 'oiday.oiday_offline_daily_{product_type}_{currentMonth}'.format(**locals())
	return '''load data infile '{localfile}' into table {table}  {characterSet} FIELDS TERMINATED BY '{delimiter}' ; commit;'''.format(**locals())

def query_update(query):
	logger.debug('query is: ' + query)
	run_query = 'mysql -u root -pTangibleDatabase -e "{query}" '.format(**locals())
	run_command(run_query)
