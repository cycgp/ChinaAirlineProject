#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class TNLSpider:
	RTN_URLList = []
	articleList = []
	newsLists = []
	def __init__(self):
		self.RTN_URLList = TNLSpider.RTN_URLList
		self.articleList = TNLSpider.articleList
		self.newsLists = TNLSpider.newsLists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(1,2):
			#Real-time news pages
			URL = 'https://www.thenewslens.com/news?page='+str(page)
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find_all(class_ = 'info-box')
			for article in articles:
				articleURL = article.findAll('a')[1].get('href')
				print(articleURL)
				self.articleList.append(articleURL)
		return self.articleList

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.articleList:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'article-title-box')
			content = ""
			newsList = []
			title = str(news.find('h1', {'class':'article-title'}).header.contents[0])
			time = news.find(class_ = 'article-info').text.split(',')[0]
			article = soup.find(class_ = 'article-content').findAll('p')
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
