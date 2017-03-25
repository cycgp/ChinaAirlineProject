#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class TPNSpider:
	RTN_URLList = []
	articleList = []
	newsLists = []
	def __init__(self):
		self.RTN_URLList = TPNSpider.RTN_URLList
		self.articleList = TPNSpider.articleList
		self.newsLists = TPNSpider.newsLists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(1,2):
			#Real-time news pages
			URL = 'http://www.peoplenews.tw/list/總覽#page-'+str(page)
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll(class_ = 'list_realtime')
			print(articles)
			for article in articles:
				articleURL = 'http://www.peoplenews.tw'+ article.find('a')[1].get('href')
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
			news = soup.find(id = 'news')
			content = ""
			newsList = []
			title = str(news.find('h1').contents[0])
			time = news.find(class_ = 'date').text
			article = news.findAll('p', {'class':'news_font2'})
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
