#!/usr/bin/python
import time

def LOG_FILE_GENERAL():
    return '/var/tmp/OidayPython_%s.log' % time.strftime("%y%m%d")

def MYSQL_DSN():
    return 'MySQLDSN'

def VERTICA_DSN():
    return 'VerticaDSN'

def ACCOUNT_PATH_MYSQL_NODE():
    return '/mnt/src_data/code/mysql'

def ACCOUNT_PATH_VERTICA_NODE():
    return '/mnt/src_data/code'

def LOCK_FILE_UPDATE_PIVOT(schema):
    return '/var/tmp/updateMySQLPivotlock_'+schema+'.lock'

def DISTRIBUTION_COLUMN_VALUE():
    return 'distribution_column_value'

def DISTRIBUTION_COLUMN_BIT_VALUE():
    return 'distribution_column_bit_value'

def GET_DISTRIBUTION_ROOT_NAME():
    return 'distribution_root_name'

def EXTERNAL_COLUMN_VALUE():
    return 'external_column_value'

def EXTERNAL_COLUMN_BIT_VALUE():
    return 'external_column_bit_value'

def QINIU_PUBLIC_DOMAIN_NAME():
    return '7xompi.com1.z0.glb.clouddn.com'

def QINIU_AK():
    return '7yNbTp0tCH0MbstARiiT8p8wxKYBzpx5Y1suQnU8'

def QINIU_SK():
    return 'yuUcaWFtB9B_U-mRzW1i3pLAd0jGaAdIe2Jtova7'

def LOAD_DATA_CHARACTER_SET():
    return ' CHARACTER SET UTF8 '