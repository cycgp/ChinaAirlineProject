#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class LTNSpider:
	RTN_URLList = []
	articleList = []
	newsLists = []
	def __init__(self):
		self.RTN_URLList = LTNSpider.RTN_URLList
		self.articleList = LTNSpider.articleList
		self.newsLists = LTNSpider.newsLists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(1,2):
			#Real-time news pages
			URL = 'http://news.ltn.com.tw/list/BreakingNews?page='+str(page)
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find_all('a', {'class' : 'picword'})
			for article in articles:
				articleURL = article.get('href')
				self.articleList.append(articleURL)
		return self.articleList

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.articleList:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'content')
			content = ""
			newsList = []
			try:
				title = str(news.find('h1').contents[0])
			except Exception as e:
				continue
			newsText = news.find('div', {'id':'newstext'})
			try:
				time = newsText.span.text
			except:
				continue
			newsSoup = bs4(str(newsText), 'html.parser')
			newsSoup.ul.decompose()
			try:
				article = newsSoup.findAll('p')
			except:
				pass
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
