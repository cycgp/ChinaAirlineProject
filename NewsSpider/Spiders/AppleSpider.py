#coding:utf-8
from bs4 import BeautifulSoup as bs4
import time
import requests
import json
import sys
import timeout_decorator

class AppleSpider:
	RTN_URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.RTN_URLList = AppleSpider.RTN_URLList
		self.ARTICLE_List = AppleSpider.ARTICLE_List
		self.NEWS_Lists = AppleSpider.NEWS_Lists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(0,10):
			#Real-time news pages
			URL = 'http://www.appledaily.com.tw/realtimenews/section/new/'+str(page)
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find_all(class_ = 'rtddt')
			for article in articles:
				inListURL = article.find('a').get('href')
				articleURL = article.find('a').get('href') if 'http://www.appledaily.com.tw' in inListURL else 'http://www.appledaily.com.tw'+article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return self.ARTICLE_List

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.ARTICLE_List:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'abdominis')
			content = ""
			newsList = []
			title = news.find('h1', {'id':'h1'}).contents[0]
			Time = news.find('time').text
			datetime = news.find('time')['datetime'].strip('/')
			article = news.find('p', {'id':'summary'}).findAll(text=True)
			if time.strftime('%Y/%m/%d', time.localtime()) not in datetime:
				continue
			else:
				pass
			print('新聞標題 : ' + title)
			print('------------------------------')
			print(Time)
			print('------------------------------')
			for contents in article:
				content +=  str(contents)
			print(content)
			print('------------------------------')

			self.NEWS_Lists.append([title,time,content])
		return self.NEWS_Lists
