#!/usr/bin/python
import  os.path
from logs.oidayLog import initializeDebugLogging

global logger

logger = initializeDebugLogging("fileUtility")

def file_exist(filePath):
    return os.path.isfile(filePath)

def create_file(filePath):
	if file_exist(filePath):
		remove_file(filePath)
	open(filePath, 'a').close()
    
def remove_file(filePath):
    os.remove(filePath)
    
def folder_exist(folderPath):
    return os.path.isdir(folderPath)
    
def create_folder(folderPath):
    os.makedirs(folderPath)
    
def remove_folder(folderPath):
    os.rmdir(folderPath)