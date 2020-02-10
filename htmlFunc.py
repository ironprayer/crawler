#!/usr/bin/python
#encoding:u8

import os
os.environ['http_proxy']=''
import urllib2,cookielib
import urllib as ul
import urllib
from socket import error as SocketError
import errno
import httplib

def wiredSpaceRemover(content):
	"""

	내용에서 필요없는 공간을 제거해주는 모듈

	Args::

		content (str)::
			
			구인구직	일 열심히 할 사람 찾습니다.

	Usage::

		필요없는 공간 제거한 데이터 결과::

			구인구직 일 열심히 할 사람 찾습니다.

	returns::

		필요없는 공간이 제거된 문자열 ''Return'' (str)

	"""
	import re
	content = content.replace('\t', ' ')
	content = content.replace('\v', ' ')
	content = content.replace('\a', ' ')
	content = content.replace('\r\n', '\n')
	content = content.replace('\r', ' ')
	content = content.replace('\n', ' ')
	content = content.replace('\xef\xbb\xbf', '')
	content = re.sub('( )+', ' ', content)
	content = content.strip()
	return content

def remove_html_tags(data):
	"""
	html 문서에서 태그를 없애주는 모듈

	Args::
		
		data (str)::

			<h1> 구인구직 </h1>

	Usage::

		태그 제거 결과::

			구인구직

	returns::

		태그가 제거된 문자열 ''Returns'' (str)

	"""
    
	import re    
	data = wiredSpaceRemover(data) 
	p = re.compile(r'<[( )\.:;/=~|"-_!}{@#$%^&*가-힣a-zA-Z0-9]*?>') 
	data = p.sub(' ', data)	
	data = re.sub("\&\#[0-9]+\;", " ", data)    
	data = data.replace('&nbsp;', ' ').replace('&amp;', '').replace('&quot;', '').replace('&nbsp', ' ').replace('&gt;', '').replace('&raquo;', '').replace('&nbsp;', '').replace('&rarr;', '').replace('&middot;', '').replace('&lsquo;', '').replace('', '').replace('&rsquo;', '').replace('&ldquo;', '').replace('&rdquo;', '')
	data = re.sub(r'<(script).*?</\1>(?s)', '', data)
	data = re.sub('\---+', ' ', data)
	data = re.sub('body\{[a-zA-Z0-9\;\:\-\,\# ]+\}', ' ', data)
	data = re.sub('p\{[a-zA-Z0-9\;\:\-\,\# ]+\}', ' ', data)
	data = re.sub('td\{[a-zA-Z0-9\;\:\-\,\# ]+\}', ' ', data)
	data = re.sub('[a-zA-z0-9\;\:\-\,\#\=\~\"\_\!\(\)\\\.]+>','',data)
	data = re.sub('<[a-zA-z0-9\;\:\-\,\#\=\~\"\_\!\(\)\\\.]+','',data)
	data = re.sub('"','',data)
	data = re.sub('\s*\,\s*',',',data)
	data = re.sub('\s\s*',' ',data)
	data = re.sub('{[a-zA-Z0-9\;\:\-\,\# ]+;}', ' ', data)
	data = data.replace('( )+', ' ')
	return data


class bypassGuardian():
	"""

	Html 문서 접속 헤더 설정해주는 모듈

	"""

	import string
	import random
	hdr = {'User-Agent': 'M%szi%sl%s/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11' % (random.choice(string.uppercase+string.lowercase+string.digits), random.choice(string.uppercase+string.lowercase+string.digits), random.choice(string.uppercase+string.lowercase+string.digits)),
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def unicodeDecoder(htmlContent):
	"""
	
	html 문서 인코딩을 cp949에서 utf-8로 바꿔주는 모듈

	Args::
		
		htmlContent (str) ::
			
			<body> ... \r\n </body>
	Usages::

		인코딩 변환 결과::	

			<body> ... \n <body>
	
	return::

		인코딩이 바뀐 html 문서 ''Returns'' (str)
    
	"""
	
	try:
		htmlContent = htmlContent.decode('cp949').encode('u8').replace('\r\n', '\n').strip()
		return htmlContent
	except UnicodeDecodeError:
		htmlContent = htmlContent.replace('\r\n', '\n').strip()
	
	return htmlContent


def getHtmlContent(bURL) :
	"""

	해당 사이트의 Html문서를 가져오는 모듈

	Args::
		
		bURL (str) ::
			
			https://www.saramin.co.kr/zf_user/jobs/relay/pop_view?isMypage=no&rec_idx=67000000'

	Usages ::
		
		<http> ... </http>

	returns::

		해당 사이트와 연결이 되면 Html 내용 ''Returs'' (str)
		해당 사이트와 연결이 안 되면 \Space 'Returs' (str)

	"""		

	try :
		req = urllib2.Request(bURL, headers=bypassGuardian.hdr)
		page = urllib2.urlopen(req)
	except urllib2.HTTPError :
		return ' '
	
	htmlContent = page.read()
	htmlContent = unicodeDecoder(htmlContent)
	return htmlContent





if __name__ == '__main__' :
	sys.exit(main())

#❚
