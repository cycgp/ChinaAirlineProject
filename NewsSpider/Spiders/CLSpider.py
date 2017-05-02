#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import requests
import json
import time as t

class CLSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = CLSpider.URLList
		self.ARTICLE_List = CLSpider.ARTICLE_List
		self.NEWS_Lists = CLSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		page = 0
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.coolloud.org.tw/story?page='+str(page)
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll('span', {'class':'date-display-single'})
			for time in timeList:
				timeList[timeList.index(time)] = time.text
			state = t.strftime('%y%m%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll('div', {'class':'field-content pc-style'})
			for article in articles:
				articleURL = 'http://www.coolloud.org.tw'+ article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'cld', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.ARTICLE_List:
			driver = webdriver.PhantomJS()
			r = driver.get(article)
			pageSource = driver.page_source
			soup = bs4(pageSource, 'html.parser')
			news = soup.find(class_ = 'main-container')
			content = ""
			title = str(news.find('p').contents[0])
			time = news.find(class_ ='date-display-single')
			article = news.find(class_ = 'node node-post node-promoted clearfix').findAll('p')

			#filter fault news
			if t.strftime('%Y/%m/%d', t.localtime()) not in time:
				continue
			else:
				pass

			print('新聞標題 : ' + title)
			print('------------------------------')
			print(time.text)
			print('------------------------------')
			for contents in article:
				content +=  str(contents.text)
			print(content)
			print('------------------------------')
			self.NEWS_Lists.append([title,time,content])
		return self.NEWS_Lists
