#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class AppleSpider:
	RTN_URLList = []
	articleList = []
	newsLists = []
	def __init__(self):
		self.RTN_URLList = AppleSpider.RTN_URLList
		self.articleList = AppleSpider.articleList
		self.newsLists = AppleSpider.newsLists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(1,2):
			#Real-time news pages
			URL = 'http://www.appledaily.com.tw/realtimenews/section/new/'+str(page)
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find_all(class_ = 'rtddt')
			for article in articles:
				articleURL = 'http://www.appledaily.com.tw/'+article.find('a').get('href')
				self.articleList.append(articleURL)
		return self.articleList

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.articleList:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'abdominis')
			content = ""
			newsList = []
			title = str(news.find('h1', {'id':'h1'}).contents[0].encode('utf-8'))
			article = news.find('p', {'id':'summary'}).findAll(text=True)
			print('新聞標題 : ' + title)
			print('------------------------------')
			for contents in article:
				content +=  str(contents.encode('utf-8'))
			print(content)
			print('------------------------------')
			self.newsLists.append([title,content])
		return self.newsLists
