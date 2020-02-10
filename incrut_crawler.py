#!/usr/bin/python
#encoding:u8

import os
import datetime, time
import errno
from time import localtime, strftime
import sys
from htmlFunc import *
import socket
from datetime import datetime as dt, timedelta
import psycopg2
import config
import pickle

def setAbsPathFolder() :
	"""

	데이터 저장 위치까지의 폴더 생성

	"""
	AbsPath = config.abs_path()
	if os.path.exists(AbsPath) == False :
		os.system('mkdir -p %s' % AbsPath)

def setLogDataFile() :

	"""
	
	로그 파일을 설정하는 모듈

	"""

	AbslogPath = config.abs_path() + 'log.csv'
	if os.path.exists(AbslogPath) == False :
		f = open(AbslogPath, 'w')
		f.write('크롤링 사이트\t시작시간\t종료시간\t시작인덱스\t종료인덱스\t홈페이지수\t인덱스리스트\r\n')
		f.close()

def setDataSaveFolder(folderPath) :
	"""

	데이터 저장 폴더를 설정하는 모듈

	Args::

		folderNmae (str) ::
			
			20200204

	Usages ::
		
		/home/owlnest-01/20200204

	"""

	AbsPath = config.abs_path()+ folderPath
	if os.path.exists(AbsPath) == False :
		os.system('mkdir -p %s' % AbsPath)

def setDataSaveFile(folderPath, fileName) :
	"""

	데이터 저장 파일을 설정하고 반환해주는 모듈

	Args::
		
		folderName (str) ::
			
			20200204

		fileName (str) ::

			2020.02.04.csv
	
	Usages::
		
		/home/owlnest-01/20200204/2020.02.04.csv
	
	returns::
		
		파일의 절대경로 ''Returns'' (str)

	"""
	AbsFilePath = config.abs_path() + folderPath +'/' + fileName
	if os.path.exists(AbsFilePath) == False:
		f = open(AbsFilePath, 'w')
		f.write('url\t시작일\t마감일\t회사명\t제목\t조회수\t경력\t우대사항\t근무형태\t학력\t급여\t근무일시\t근무지역\t복리후생\t기업정보\t태그\t본문\r\n')
		f.close()
	return AbsFilePath


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

#형식을 수정해야 한다.
def insertDataToDB(TableName, DataFormat, DataTuple):
	"""
	
	DB에 데이터를 넣는 모듈

	Args::
		
		DataTuple (tuple)::

			(20200103,20200104,395,400,"395,396,397,398,399,400")	


	"""

	params = config.db_config()
	conn = psycopg2.connect(**params)
	conn.autocommit = True
	cur = conn.cursor()

	query = 'INSERT INTO ' + TableName + ' VALUES' + DataFormat
	#(%s,%s,%s,%s,%s,%s)'
	#cur.execute(query,(DataTuple[0],DataTuple[1],DataTuple[2],DataTuple[3],DataTuple[4],DataTuple[5]))
	cur.execute(query,DataTuple)	
	cur.close()
	conn.commit()
	conn.close()
	

def main():

	baseUrl = 'https://job.incruit.com/jobdb_info/jobpost.asp?job='
	baseMainUrl = 'https://job.incruit.com/s_common/jobpost/jobpostcont.asp?job='
	#print wiredSpaceRemover(getHtmlContent(baseUrl + '2002050004510'))
	#htmlContent = wiredSpaceRemover(getHtmlContent(baseUrl))
	#htmlContent = getHtmlContent(baseUrl)
	#if htmlContent == ' ':
	#	print 'error'
	#print htmlContent
	
	#시작시간 저장
	setAbsPathFolder()
	crawlerName = 'incrut'
	LatestIdxDic = setLatestIdxFile()
	#LatestIdxDic ={'incrut':2002060002990}
	startTime = localtime()
	logStartDate = strftime("%Y-%m-%d %I:%M:%S",startTime)
	startIdx = 0
	endDate = ''
	startDate = ''
	hompageCnt = 0
	IdxList = []
	
	print LatestIdxDic
	print 'Crawling.........'

	# 이전에 검색한 데이터가 있을 때
	if crawlerName in LatestIdxDic.keys() :
		startIdx = LatestIdxDic[crawlerName] + 1
		if startIdx == int(strftime("%y%m%d",startTime) + '0005001'):
			return

		if startIdx%10000000 > 5000 :
			startIdx = int(str(startIdx/10000000) + '0000001')
	else :
		startIdx = 1801010000001

	print startIdx
	endtime = int(datetime.datetime.now().strftime("%y%m%d"))
	curIdx = startIdx
	while True:
		DataList = []
		for i in range(0,17):
			DataList.append('')
		
		print curIdx
		#if curIdx % 5002 == 5001 :
		if curIdx - (curIdx/10000000)*10000000 == 5001 :
			curIdx = int(str((curIdx/10000000) + 1).zfill(6) + '0000001')

		try :
			HtmlContent = getHtmlContent(baseUrl + str(curIdx).zfill(13))
		
			if curIdx/10000000 > endtime:
				curIdx = int(str(endtime) + '0005000')
				break

			if HtmlContent == ' ':
				curIdx += 1
				continue
		except socket.error :
			print 'socket error'
			curIdx -= 1
			break;

		hompageCnt += 1
		
		print 'hompageCnt %d'%hompageCnt
		
		HtmlMainContent = getHtmlContent(baseMainUrl + str(curIdx).zfill(13))
		HtmlContent = wiredSpaceRemover(HtmlContent)
		DataList[0] = baseUrl + str(curIdx).zfill(13)
		
		if '<em>시작</em>' in HtmlContent :
			DataList[1] = HtmlContent.split('<em>시작</em>')[1].split('<strong>')[1].split(' ')[0].strip()

		if '<em>마감</em></span>' in HtmlContent :
			DataList[2] = HtmlContent.split('<em>마감</em></span>')[1].split('<strong>')[1].split(' ')[0].strip()
			

		if 'jobview_top_title' in HtmlContent:
			DataList[3] = HtmlContent.split('jobview_top_title')[1].split('<span>')[1].split('</span>')[0].strip()
			DataList[4] = HtmlContent.split('jobview_top_title')[1].split('<strong>')[1].split('</strong>')[0].strip()

		TempDic = {'경력': '', '학력': '', '우대사항':'', '고용형태':'', '지역':'', '급여':''}
		tempHtmlContent = HtmlContent.split('jobpost_sider_jbinfo_inlay_last')[0].split('jobpost_sider_cpinfo')[-1] + HtmlContent.split('jobpost_sider_jbinfo_inlay_last')[1].split('jobview_top_btn jobview_top_btn_empty')[0]

		for key in TempDic.keys() :
			if key in tempHtmlContent :
				TempDic[key] =  wiredSpaceRemover(remove_html_tags(tempHtmlContent.split('<dt>%s</dt>'%key)[1].split('<dd>')[1].split('</div>')[0])).strip()

		DataList[6]= TempDic['경력'].strip()
		DataList[7]= TempDic['우대사항'].strip()
		DataList[9]= TempDic['학력'].strip()
		DataList[10]= TempDic['급여'].strip()
		DataList[11]= TempDic['고용형태'].strip()
		
		if '<ul class="AreaList">' in HtmlContent :
			DataList[12] += remove_html_tags(HtmlContent.split('<ul class="AreaList">')[1].split('</ul>')[0].strip())			
		if 'welfare_receipt' in HtmlContent:
			DataList[13] = wiredSpaceRemover(remove_html_tags(HtmlContent.split('welfare_receipt')[1].split('<ul>')[1].split('</ul>')[0])).strip()
		if 'brand_detail_table' in HtmlContent:
			DataList[14]= wiredSpaceRemover(remove_html_tags(HtmlContent.split('brand_detail_table')[1].split('</div>')[0])).split('>')[1].strip()
		
		try:
			if 'content_job' in HtmlMainContent:
				if 'BODY' in HtmlMainContent :
					HtmlMainContent = HtmlMainContent.split('BODY')[1]
			else :
					HtmlMainContent = HtmlMainContent.split('jobview_top_btn jobview_top_btn_empty')[1].split('jobview_h2')[1].split('</div')[0]

			DataList[16]= wiredSpaceRemover(remove_html_tags(HtmlMainContent)).replace('>',' ').strip() + '\r\n'

		except IndexError:
			DataList[16] =''
	
		dataStr = ''
		for data in DataList:
			dataStr += data + '\t'

		folderName = strftime("%Y%m%d",startTime)
		setDataSaveFolder('IncrutCrawler/%s' % folderName)
		
		fileName = DataList[2]
		if fileName == '':
			fileName = 'noDate'

		filePath = setDataSaveFile('IncrutCrawler/%s'% folderName, '%s.csv' % fileName)		
		f = open(filePath,'a')
		f.write(dataStr.strip()+'\r\n')
		f.close()
		IdxList.append(str(curIdx))
		curIdx += 1

					
	logEndDate = strftime("%Y-%m-%d %I:%M:%S",localtime())
	print 'Crawler End......'
	#idxListStr = '{' + ','.join(IdxList) + '}'

#	insertDataToDB('crawler_log','(%s,%s,%s,%s,%s,%s,%s)', ('incrut',logStartDate,logEndDate, str(startIdx),str(curIdx),hompageCnt,IdxList))
	
	setLogDataFile()
	with open(config.abs_path() + 'log.csv', 'a') as fa:
		fa.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t'.format(crawlerName,logStartDate, logEndDate, str(startIdx), str(curIdx),str(hompageCnt)))
		fa.write(','.join(IdxList))
		fa.close()
	
	LatestIdxDic[crawlerName] = curIdx
	with open(config.abs_path() + 'latestIdx.txt','w') as fa:
		pickle.dump(LatestIdxDic, fa)
		fa.close()
	#insertDataToDB((logStartDate,logEndDate,preLatestIdx+1,preLatestIdx+cnt,htmlCnt,indexListStr))


if __name__ == '__main__' :
	sys.exit(main())

#❚
