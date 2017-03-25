#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class CLSpider:
	RTN_URLList = []
	articleList = []
	newsLists = []
	def __init__(self):
		self.RTN_URLList = CLSpider.RTN_URLList
		self.articleList = CLSpider.articleList
		self.newsLists = CLSpider.newsLists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(1,2):
			#Real-time news pages
			URL = 'http://www.coolloud.org.tw/story?page='+str(page)
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll(class_ = 'field-content pc-style')
			print(articles)
			for article in articles:
				articleURL = 'http://www.coolloud.org.tw'+ article.find('a').get('href')
				self.articleList.append(articleURL)
		return self.articleList

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.articleList:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'main-container')
			content = ""
			newsList = []
			title = str(news.find('p').contents[0])
			time = news.find(class_ ='date-display-single')
			article = news.find(class_ = 'node node-post node-promoted clearfix').findAll('p')
			print('新聞標題 : ' + title)
			print('------------------------------')
			print(time)
			print('------------------------------')
			for contents in article:
				content +=  str(contents)
			print(content.text)
			print('------------------------------')
			self.newsLists.append([title,time,content])
		return self.newsLists
