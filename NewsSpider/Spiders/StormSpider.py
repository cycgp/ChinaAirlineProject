#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class StormSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = StormSpider.URLList
		self.ARTICLE_List = StormSpider.ARTICLE_List
		self.NEWS_Lists = StormSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		for page in range(1,2):
			#Real-time news pages
			URL = 'http://www.storm.mg/articles/'+str(page)
			self.URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll(class_ = 'main_content')
			for article in articles:
				articleURL = 'http://www.storm.mg'+ article.find('p').find('a').get('href')
				print(articleURL)
				self.ARTICLE_List.append(articleURL)
		return self.ARTICLE_List

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.ARTICLE_List:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'inner-wrap')
			content = ""
			newsList = []
			title = str(news.find('h1', {'class':'title'}).contents[0])
			time = news.find(class_='date').text.split('風傳媒')[0]
			article = news.article.findAll('p')
			print('新聞標題 : ' + title.strip())
			print('------------------------------')
			print(time)
			print('------------------------------')
			for contents in article:
				content +=  str(contents.text)
			print(content)
			print('------------------------------')
			self.NEWS_Lists.append([title,time,content])
		return self.NEWS_Lists
