#coding:utf-8
from bs4 import BeautifulSoup as bs4
import json
import re
import requests
import random
import sys
from selenium import webdriver
import time as t

class aplSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = aplSpider.URLList
		self.ARTICLE_List = aplSpider.ARTICLE_List

	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.appledaily.com.tw/realtimenews/section/new/'+str(page)
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			soup = soup.find('time').text.replace(' / ','')
			state = t.strftime('%y%m%d', t.localtime()) in soup
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find_all(class_ = 'rtddt')
			for article in articles:
				inListURL = article.find('a').get('href')
				articleURL = article.find('a').get('href') if 'http://www.appledaily.com.tw' in inListURL else 'http://www.appledaily.com.tw'+article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'apl', 'URLList':self.ARTICLE_List}

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsList = []
		articleIDList = []
		for articleURL in ARTICLE_List:
			try:
				if articleURL in record:
					continue
				t.sleep(random.randint(5,8))
				sys.stdout.write('\r             ' + ' '*65)
				sys.stdout.write('\r    URL: ' + articleURL[:69])
				#get news from url
				r = requests.get(articleURL)
				soup = bs4(r.text, 'html.parser')
				news = soup.find(class_ = 'abdominis')
				#get title, date, time
				title = news.find('h1', {'id':'h1'}).text
				time = re.split('年|月|日|:', news.find('time').text)#time to list
				timeInNews = ':'.join(time[3:])
				datetime = '/'.join(time[:3])
				#filter news from yesterday
				if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
					continue
				else:
					pass
				#get content
				article = news.find('p', {'id':'summary'}).findAll(text=True)
				content = ''
				for contents in article:
					content +=  str(contents)
				#assign news ID
				articleID = ''.join(time)+'000'
				while articleID in articleIDList:
					articleID = str(int(articleID)+1)
				articleIDList.append(articleID)
				articleID = 'apl'+articleID
				newsList.append([articleID, articleURL, title, datetime + ' ' + timeInNews, content])
			except:
				continue
		return newsList

class cldSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = cldSpider.URLList
		self.ARTICLE_List = cldSpider.ARTICLE_List

	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		page = 0
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.coolloud.org.tw/story?page='+str(page)
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll('span', {'class':'date-display-single'})
			for time in timeList:
				timeList[timeList.index(time)] = time.text
			timeList = timeList[:-5]#filter hot news
			state = t.strftime('%Y/%m/%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1

		#Get articles url from real-time news pages
		for URL in self.URLList:
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll('div', {'class':'field-content pc-style'})
			for article in articles:
				articleURL = 'http://www.coolloud.org.tw'+ article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'cld', 'URLList':self.ARTICLE_List}

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsLists = []
		articleIDList = []
		driver = webdriver.PhantomJS()
		for articleURL in ARTICLE_List:
			if articleURL in record:
				continue
			sys.stdout.write('\r             ' + ' '*65)
			sys.stdout.write('\r    URL: ' + articleURL[:69])
			t.sleep(random.randint(5,8))
			r = driver.get(articleURL)
			pageSource = driver.page_source
			soup = bs4(pageSource, 'html.parser')
			news = soup.find(class_ = 'main-container')
			content = ""
			title = str(news.find('p').text)
			time = re.split('/', news.find(class_ ='date-display-single').text)
			datetime = '/'.join(time[:3])+' 00:00'
			article = news.find(class_ = 'node node-post node-promoted clearfix').findAll('p')

			#filter fault news
			if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
				continue
			else:
				pass

			for contents in article:
				content +=  contents.text

			articleID = ''.join(time)+'0000000'
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'cld'+articleID
			newsLists.append([articleID, articleURL, title, datetime, content])
		return newsLists

class cnaSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = cnaSpider.URLList
		self.ARTICLE_List = cnaSpider.ARTICLE_List
	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.cna.com.tw/list/aall-'+str(page)+'.aspx'
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			if  soup.find('div', {'class':'article_list'}) is None:
				break
			timeList = soup.find('div', {'class':'article_list'}).findAll('span')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.split(' ')[0]
			state = t.strftime('%Y/%m/%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find(class_ = 'article_list').findAll('li')
			for article in articles:

				articleURL = 'http://www.cna.com.tw'+article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'cna', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsList = []
		articleIDList = []
		for articleURL in ARTICLE_List:
			try:
				if articleURL in record:
					continue
				t.sleep(random.randint(5,8))
				sys.stdout.write('\r             ' + ' '*65)
				sys.stdout.write('\r    URL: ' + articleURL[:69])
				r = requests.get(articleURL)
				soup = bs4(r.text, 'html.parser')
				news = soup.find(class_ = 'news_article')
				content = ""
				title = news.find('h1').text.replace('\r\n        ','')
				time = re.split('發稿時間：| |/|:', news.find('div', {'class':'update_times'}).find('p').text)
				datetime = '/'.join(time[1:4])
				timeInNews = ':'.join(time[4:])
				article = news.find('div', {'class':'article_box'}).p.text

				if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
					continue
				else:
					pass

				articleID = ''.join(time[1:])+'000'
				while articleID in articleIDList:
					articleID = str(int(articleID)+1)
				articleIDList.append(articleID)
				articleID = 'cna'+articleID
				for contents in article:
					content +=  str(contents)
				newsList.append([articleID, articleURL, title, datetime + ' ' + timeInNews, content])
			except:
				continue
		return newsList

class cntSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = cntSpider.URLList
		self.ARTICLE_List = cntSpider.ARTICLE_List

	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		#Real-time news pages
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.chinatimes.com/realtimenews?page='+str(page)
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll('time')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.split()[1]
			state = t.strftime('%Y/%m/%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find(class_ = 'listRight').findAll('h2')
			for article in articles:
				articleURL = 'http://www.chinatimes.com'+ article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'cnt', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsList = []
		articleIDList = []
		for articleURL in ARTICLE_List:
			if articleURL in record:
				continue
			t.sleep(random.randint(5,8))
			sys.stdout.write('\r             ' + ' '*65)
			sys.stdout.write('\r    URL: ' + articleURL[:69])
			try:
				r = requests.get(articleURL)
				soup = bs4(r.text, 'html.parser')
				news = soup.find(class_ = 'page_container')
				content = ""
				title = str(news.find('h1').text)
				time = re.split('年|月|日|:| ', news.find('time').text)#time to list
				timeInNews = ':'.join(time[4:])
				datetime = '/'.join(time[:3])
				article = news.findAll('p')

				if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
					continue
				else:
					pass

				articleID = ''.join(time)+'000'
				while articleID in articleIDList:
					articleID = str(int(articleID)+1)
				articleIDList.append(articleID)
				articleID = 'cnt'+articleID
				for contents in article:
					content +=  str(contents.text)
				newsList.append([articleID, articleURL, title, datetime + ' ' + timeInNews, content])
			except:
				continue
		return newsList

class ltnSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = ltnSpider.URLList
		self.ARTICLE_List = ltnSpider.ARTICLE_List

	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		#Real-time news pages
		page = 0
		state = True
		TimeList= []
		while state:
			#Real-time news pages
			URL = 'http://news.ltn.com.tw/list/breakingnews/all/'+str(page)
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.find('ul', {'class':'list imm'}).findAll('span')
			for time in timeList:
				state = '-' not in time.text
			page += 1
			self.URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.URLList:
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find_all('a', {'class' : 'ph'})
			for article in articles:
				articleURL = article.get('href')
				if 'sports' in articleURL or 'talk' in articleURL or '3c' in articleURL or 'auto' in articleURL:
					continue
				else:
					pass
				self.ARTICLE_List.append(articleURL)
		return {'press':'ltn', 'URLList':self.ARTICLE_List}

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsList = []
		articleIDList = []
		for articleURL in ARTICLE_List:
			try:
				if articleURL in record:
					continue
				t.sleep(random.randint(5,8))
				sys.stdout.write('\r             ' + ' '*65)
				sys.stdout.write('\r    URL: ' + articleURL[:69])
				r = requests.get(articleURL)
				soup = bs4(r.text, 'html.parser')
				if soup.find(class_ = 'whitecon articlebody') is not None:
					news = soup.find(class_ = 'whitecon articlebody')
				elif soup.find(class_ = 'news_content') is not None:
					news = soup.find(class_ = 'news_content')
				elif soup.find(class_ = 'main-content') is not None:
					news = soup.find(class_ = 'main-content')
				elif soup.find(class_ = 'conbox') is not None:
					news = soup.find(class_ = 'conbox')
				elif soup.find(class_ = 'content') is not None:
					news = soup.find(class_ = 'content')
				content = ""

				if news.find('h1') is not None:
					title = ''.join(re.split(' |[\n]|[\t]|[\r]', str(news.find('h1').text)))
				else:
					title = ''.join(re.split(' |[\n]|[\t]|[\r]', str(news.find('h2').text)))

				if 'TAIPEITIMES' in title or 'TAIPEI TIMES' in title:
					continue

				if news.find('div',{'class':'text'}) is not None:
					time = news.find('div',{'class':'text'}).span.text
				elif news.find(class_ = 'c_time') is not None:
					time = news.find(class_ = 'c_time').text
				elif news.find(class_ = 'date') is not None:
					time = news.find(class_ = 'date').text
				elif news.find(class_ = 'pic750') is not None:
					time = news.find(class_ = 'pic750').text
				elif news.find(class_ = 'label-date') is not None:
					if t.strftime('%b. %d %Y', t.localtime()) in news.find(class_ = 'label-date').text:
						time = t.strftime('%Y-%m-%d 00:00', t.localtime())
				elif news.find(class_ = 'writer_date') is not None:
					time = news.find(class_ = 'writer_date').text
				elif news.find(class_ = 'writer') is not None:
					time = news.findAll('span',{'class':'writer'})[2].replace(' 2','2')
				elif news.find(class_ = 'h1dt') is not None:
					time = news.find('span',{'class':'h1dt'}).text
				elif news.find(class_ = 'mobile_none') is not None:
					time = news.find(class_ = 'mobile_none').text
				elif news.find(class_ = 'writer_date') is not None:
					time = news.find(class_ = 'writer_date').text

				if news.find('div',{'class':'text'}) is not None:
					article = news.find('div',{'class':'text'}).findAll('p')
				elif news.find('div',{'class':'new_p'}) is not None:
					article = news.find('div',{'class':'new_p'}).findAll('p')
				elif news.find('div',{'class':'content'}) is not None:
					article = news.find('div',{'class':'content'}).findAll('p')
				elif news.find('div',{'class':'boxTitle'}) is not None:
					article = news.find('div',{'class':'boxTitle'}).findAll('p')
				elif news.find('div',{'class':'cont'}) is not None:
					article = news.find('div',{'class':'cont'}).findAll('p')
				elif news.find('div',{'class':'cont boxTitle'}) is not None:
					article = news.find('div',{'class':'cont boxTitle'}).findAll('p')
				elif news.find('div',{'class':'cin'}) is not None:
					article = news.find('div',{'class':'con'}).findAll('p')

				if t.strftime('%Y-%m-%d', t.localtime()) not in time.split()[0]:
					continue
				else:
					pass

				for contents in article:
					content +=  str(contents.text.strip())
				content = ''.join(re.split(' |[\n]|[\t]|[\r]', content))

				time = re.split('-| |:',time)
				datetime = '/'.join(time[:3])
				timeInNews = ':'.join(time[3:])
				articleID = ''.join(time)+'000'
				while articleID in articleIDList:
					articleID = str(int(articleID)+1)
				articleIDList.append(articleID)
				articleID = 'ltn'+articleID

				newsList.append([articleID, articleURL, title, datetime + ' ' + timeInNews, content])
			except Exception as e:
				continue
		return newsList

class ntkSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = ntkSpider.URLList
		self.ARTICLE_List = ntkSpider.ARTICLE_List

	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		a = t.strftime('%Y-%m-%d', t.localtime())
		#Real-time news pages
		URL = 'https://newtalk.tw/news/summary/'+str(a)
		self.URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.URLList:
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll(class_ = 'news_title')
			for article in articles:
				articleURL = article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'ntk', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsList = []
		articleIDList = []
		driver = webdriver.PhantomJS()
		for articleURL in ARTICLE_List:
			try:
				if articleURL in record:
					continue
				t.sleep(random.randint(5,8))
				if t.strftime('%Y-%m-%d', t.localtime()) not in articleURL.split('/')[5]:
					continue
				else:
					pass
				sys.stdout.write('\r             ' + ' '*65)
				sys.stdout.write('\r    URL: ' + articleURL[:69])
				r = driver.get(articleURL)
				pageSource = driver.page_source
				soup = bs4(pageSource, 'html.parser')
				news = soup.find(id = 'left_column')
				content = ""
				title = news.find(class_ = 'content_title').text
				time = '/'.join(re.split('發布 |[.]| [|] |[:]|   [\n]', news.find(class_='content_date').text)[1:-1])
				datetime ='/'.join(re.split('/', time))[:10]
				timeInNews = ':'.join(re.split('/', time))[11:16]
				article = news.findAll('p')
				articleID = ''.join(re.split('/', time))[:12]+'000'
				while articleID in articleIDList:
					articleID = str(int(articleID)+1)
				articleIDList.append(articleID)
				articleID = 'ntk'+articleID
				for contents in article:
					content +=  str(contents.text)
				newsList.append([articleID, articleURL, title, datetime + ' ' + timeInNews, content])
			except:
				continue
		return newsList

class stmSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = stmSpider.URLList
		self.ARTICLE_List = stmSpider.ARTICLE_List

	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.storm.mg/articles/'+str(page)
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll(class_ = 'main_date')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.replace('年','/').replace('月','/').replace('日','').split(' ')[0]
			state = t.strftime('%Y/%m/%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll(class_ = 'main_content')
			for article in articles:
				articleURL = 'http://www.storm.mg'+ article.find('p').find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'stm', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsList = []
		articleIDList = []
		for articleURL in ARTICLE_List:
			if articleURL in record:
				continue
			t.sleep(random.randint(5,8))
			sys.stdout.write('\r             ' + ' '*65)
			sys.stdout.write('\r    URL: ' + articleURL[:69])
			try:
				r = requests.get(articleURL)
				soup = bs4(r.text, 'html.parser')
				news = soup.find(class_ = 'inner-wrap')
				content = ""
				title = news.find('h1', {'class':'title'}).text.strip()
				time = re.split('年|月|日| |:|風傳媒',news.find(class_='date').text)
				datetime = '/'.join(time[:3])
				timeInNews = ':'.join(time[4:6])
				article = news.article.findAll('p')
			except:
				pass
			if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
				continue
			else:
				pass

			articleID = ''.join(time)+'000'
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'stm'+articleID
			for contents in article:
				content +=  str(contents.text.strip())

			content = ''.join(re.split(' |[\n]|[\t]|[\r]', content))
			newsList.append([articleID, articleURL, title, datetime + ' ' + timeInNews, content])
		return newsList

class tnlSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = tnlSpider.URLList
		self.ARTICLE_List = tnlSpider.ARTICLE_List

	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'https://www.thenewslens.com/news?page='+str(page)
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll(class_ = 'time')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.split(' ')[1]
			state = t.strftime('%Y/%m/%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1

		#Get articles url from real-time news pages
		for URL in self.URLList:
			t.sleep(random.randint(3,5))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find_all(class_ = 'info-box')
			for article in articles:
				articleURL = article.findAll('a')[1].get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'tnl', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsList = []
		articleIDList = []
		for articleURL in ARTICLE_List:
			try:
				if articleURL in record:
					continue
				t.sleep(random.randint(5,8))
				sys.stdout.write('\r             ' + ' '*65)
				sys.stdout.write('\r    URL: ' + articleURL[:69])
				r = requests.get(articleURL)
				soup = bs4(r.text, 'html.parser')
				news = soup.find(class_ = 'article-title-box')
				content = ""
				title = str(news.find('h1', {'class':'article-title'}).header.text)
				time = news.find(class_ = 'article-info').text.split(',')[0].replace(' ','')
				article = soup.find(class_ = 'article-content').findAll('p')

				if t.strftime('%Y/%m/%d', t.localtime()) not in time:
					continue
				else:
					pass

				articleID = ''.join(re.split('/', time))[:8]+'0000000'
				while articleID in articleIDList:
					articleID = str(int(articleID)+1)
				articleIDList.append(articleID)
				articleID = 'tnl'+articleID
				for contents in article:
					content +=  str(contents.text.strip())
				content = content.strip()
				newsList.append([articleID, articleURL, title, time + ' 00:00', content])
			except:
				continue
		return newsList

class tpnSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = tpnSpider.URLList
		self.ARTICLE_List = tpnSpider.ARTICLE_List

	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		page = 1
		state = True
		while state:
			EID_LIST = []
			timeList = []
			url = 'http://www.peoplenews.tw/resource/lists/ALL'
			payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"page\"\r\n\r\n" + str(page) + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"status\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
			headers = {
			    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
			    'cache-control': "no-cache",
			    'postman-token': "d5674e31-12ad-7724-03e3-c41687271841"
			    }
			r = requests.request("POST", url, data=payload, headers=headers)
			jsonResponse = json.loads(r.text)
			data_list = jsonResponse['data_list']
			for data in data_list:
				EID_LIST.append(data['EID'])
				timeList.append(data['PUBTIME'].split(' ')[0])
			state = t.strftime('%Y-%m-%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(EID_LIST)
			else:
				page -= 1
			#Get articles url from real-time news pages
		for EID_LIST in self.URLList:
			for EID in EID_LIST:
				try:
					articleURL = 'http://www.peoplenews.tw/news/'+ EID
					self.ARTICLE_List.append(articleURL)
				except:
					continue
		return {'press':'tpn', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsList = []
		articleIDList = []
		for articleURL in ARTICLE_List:
			try:
				if articleURL in record:
					continue
				t.sleep(random.randint(5,8))
				sys.stdout.write('\r             ' + ' '*65)
				sys.stdout.write('\r    URL: ' + articleURL[:69])
				r = requests.get(articleURL)
				soup = bs4(r.text, 'html.parser')
				news = soup.find(id = 'news')
				content = ""
				title = str(news.find('h1').contents[0])
				time = re.split('-| |:', news.find(class_ = 'date').text)
				datetime = '/'.join(time[:3])
				timeInNews = ':'.join(time[3:])
				article = news.find('div', {'id':'newscontent'}).findAll('p')

				if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
					continue
				else:
					pass

				articleID = ''.join(time)+'000'
				while articleID in articleIDList:
					articleID = str(int(articleID)+1)
				articleIDList.append(articleID)
				articleID = 'tpn'+articleID
				for contents in article:
					content +=  str(contents.text)
				newsList.append([articleID, articleURL, title, datetime + ' ' + timeInNews, content])
			except:
				continue
		return newsList

class udnSpider:
	URLList = []
	ARTICLE_List = []
	def __init__(self):
		self.URLList = udnSpider.URLList
		self.ARTICLE_List = udnSpider.ARTICLE_List

	#Get real-time news url
	def getURL(self):
		self.URLList = []
		self.ARTICLE_List = []
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'https://udn.com/news/breaknews/1/99/'+str(page)+'#breaknews'
			t.sleep(random.randint(1,3))
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll(class_ = 'dt')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.split(' ')[0]
			state = t.strftime('%m-%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			t.sleep(1)
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find(id = 'breaknews_body').find_all('dt')
			for article in articles:
				articleURL = 'https://udn.com'+article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'udn', 'URLList':self.ARTICLE_List}

	#Get Content from article
	def getContent(self, ARTICLE_List, record):
		newsList = []
		articleIDList = []
		driver = webdriver.PhantomJS()
		for articleURL in ARTICLE_List:
			if articleURL in record:
				continue
			t.sleep(random.randint(1,2))
			sys.stdout.write('\r             ' + ' '*65)
			sys.stdout.write('\r    URL: ' + articleURL[:69])
			try:
				r = driver.get(articleURL)
				pageSource = driver.page_source
				soup = bs4(pageSource, 'html.parser')
				news = soup.find(id = 'story_body_content')
				content = ""
				title = str(news.find('h1', {'id':'story_art_title'}).text)
				time = news.find('div', {'class':'story_bady_info_author'})
				span = time.find('span')
				if span is not None:
					span.extract()
				time = re.split('-| |:', time.text)
				datetime = '/'.join(time[:3])
				timeInNews = ':'.join(time[3:])
				article = news.findAll('p')

				if '今日星座運勢' in title:
					break

				if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
					continue
				else:
					pass

				for contents in article:
					try:
						content +=  str(contents.text)
					except:
						pass

				articleID = ''.join(time)+'000'
				if articleID.isdigit():
					pass
				else:
					continue
				while articleID in articleIDList:
					articleID = str(int(articleID)+1)
				articleIDList.append(articleID)
				articleID = 'udn'+articleID
				for contents in article:
					content +=  str(contents.text)
				newsList.append([articleID, articleURL, title, datetime + ' ' + timeInNews, content])
			except:
				continue
		return newsList
