#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import requests
import json

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
		for page in range(0,2):
			#Real-time news pages
			URL = 'http://www.coolloud.org.tw/story?page='+str(page)
			self.URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll('div', {'class':'field-content pc-style'})
			for article in articles:
				articleURL = 'http://www.coolloud.org.tw'+ article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return self.ARTICLE_List

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
			newsList = []
			title = str(news.find('p').contents[0])
			time = news.find(class_ ='date-display-single')
			article = news.find(class_ = 'node node-post node-promoted clearfix').findAll('p')
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
