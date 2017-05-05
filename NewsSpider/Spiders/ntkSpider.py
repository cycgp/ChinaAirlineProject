#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import time as t
import requests
import json
import re

class ntkSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = ntkSpider.URLList
		self.ARTICLE_List = ntkSpider.ARTICLE_List
		self.NEWS_Lists = ntkSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		a = t.strftime('%Y-%m-%d', t.localtime())
		#Real-time news pages
		URL = 'https://newtalk.tw/news/summary/'+str(a)
		self.URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.URLList:
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
	def getContent(self):
		articleIDList = []
		for article in self.ARTICLE_List:
			if t.strftime('%Y-%m-%d', t.localtime()) not in article.split('/')[5]:
				continue
			else:
				pass
			driver = webdriver.PhantomJS()
			r = driver.get(article)
			pageSource = driver.page_source
			soup = bs4(pageSource, 'html.parser')
			news = soup.find(id = 'left_column')
			content = ""
			newsList = []
			title = news.find(class_ = 'content_title').text
			time = '/'.join(re.split('發布 |[.]| [|] |[:]|   [\n]', news.find(class_='content_date').text)[1:-1])
			datetime ='/'.join(re.split('/', time))[:10]
			timeInNews = ':'.join(re.split('/', time))[11:16]
			article = news.findAll('p')
			articleID = ''.join(re.split('/', time))[:12]+'0'
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'ntk'+articleID
			for contents in article:
				content +=  str(contents.text)
			self.NEWS_Lists.append([articleID, article, title, datetime + ' ' + timeInNews, content])
		return self.NEWS_Lists
