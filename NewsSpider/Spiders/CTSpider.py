#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class CTSpider:
	RTN_URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.RTN_URLList = CTSpider.RTN_URLList
		self.ARTICLE_List = CTSpider.ARTICLE_List
		self.NEWS_Lists = CTSpider.NEWS_Lists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(1,2):
			#Real-time news pages
			URL = 'http://www.chinatimes.com/realtimenews?page='+str(page)
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find(class_ = 'listRight').findAll('h2')
			for article in articles:
				articleURL = 'http://www.chinatimes.com'+ article.find('a').get('href')
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
			news = soup.find(class_ = 'page_container')
			content = ""
			newsList = []
			title = str(news.find('h1').contents[0])
			time = news.find('time').text
			article = news.findAll('p')
			print('新聞標題 : ' + title)
			print('------------------------------')
			print(time)
			print('------------------------------')
			for contents in article:
				content +=  str(contents.text)
			print(content)
			print('------------------------------')
			self.NEWS_Lists.append([title,time,content])
		return self.NEWS_Lists
