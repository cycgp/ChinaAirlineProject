#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import time

class NTSpider:
	RTN_URLList = []
	articleList = []
	newsLists = []
	def __init__(self):
		self.RTN_URLList = NTSpider.RTN_URLList
		self.articleList = NTSpider.articleList
		self.newsLists = NTSpider.newsLists

	#Get real-time news url
	def getRTNURL(self):
		a = time.strftime('%Y-%m-%d', time.localtime())
		#Real-time news pages
		URL = 'https://newtalk.tw/news/summary/'+str(a)+'#cal'
		self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll(class_ = 'news_title')
			for article in articles:
				articleURL = article.find('a').get('href')
				self.articleList.append(articleURL)
		return self.articleList

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.articleList:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(id = 'left_column')
			content = ""
			newsList = []
			title = str(news.find(class_ = 'content_title').contents[0])
			time = news.find(class_='content_date').text.split()[1]
			article = news.findAll('p')
			print('新聞標題 : ' + title)
			print('------------------------------')
			print(time)
			print('------------------------------')
			for contents in article:
				content +=  str(contents.text)
			print(content)
			print('------------------------------')
			self.newsLists.append([title,time,content])
		return self.newsLists
