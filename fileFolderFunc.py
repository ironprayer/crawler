#!/usr/bin/python
#encoding:u8

import os
import sys
import config
import pickle


def setDataSaveFolder(folderPath) :
	"""

	데이터 저장 폴더를 설정하는 모듈

	Args::

		folderPath (str) ::
			
			/home/owlnest-01/20200204

	"""

	if os.path.exists(folderPath) == False :
		os.system('mkdir -p %s' % folderPath)


def setDataFile(filePath, fileName, FieldNameList, fieldSpr) :

	"""
	
	저장 파일 설정 해주는 모듈

	Args::
	
		filePath (str)::
		
			/home/userName

		fileName (str)::

			log.csv

		FieldNameList (list)::
			
			[Url, StartDate, EndDate, ...]

		fieldSpr::
		
			'\t' 

	"""
	if os.path.exists(filePath) == False :
		os.system('mkdir -p %s' % filePath)

	if os.path.exists('{0}/{1}'.format(filePath, fileName)) == False:
		f = open('{0}/{1}'.format(filePath, fileName) , 'w')
		f.write(fieldSpr.join(FieldNameList))
		f.close()


def setLatestIdxFile() :

	if os.path.exists('%slatestIdx.txt'%config.abs_path()) == False:
		f = open('%slatestIdx.txt'%config.abs_path(), 'w')
		pickle.dump({},f)
		f.close()
		return {}

	f = open('%slatestIdx.txt'%config.abs_path())
	
	LatestIdxDic = pickle.load(f)
	f.close()
	return LatestIdxDic 


#❚
