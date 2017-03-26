#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import time
import dryscrape

class NTSpider:
	RTN_URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.RTN_URLList = NTSpider.RTN_URLList
		self.ARTICLE_List = NTSpider.ARTICLE_List
		self.NEWS_Lists = NTSpider.NEWS_Lists

	#Get real-time news url
	def getRTNURL(self):
		a = time.strftime('%Y-%m-%d', time.localtime())
		#Real-time news pages
		URL = 'https://newtalk.tw/news/summary/'+str(a)
		self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll(class_ = 'news_title')
			for article in articles:
				articleURL = article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return self.ARTICLE_List

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.ARTICLE_List:
			session = dryscrape.Session()
			session.visit(article)
			response = session.body()
			soup = bs4(response, 'html.parser')
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
			content = content.split('（喜歡這條新聞，給新頭殼按個讚！）')[0]
			print(content)
			print('------------------------------')
			self.NEWS_Lists.append([title,time,content])
		return self.NEWS_Lists
