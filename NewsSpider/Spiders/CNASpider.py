#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class CNASpider:
	RTN_URLList = []
	articleList = []
	newsLists = []
	def __init__(self):
		self.RTN_URLList = CNASpider.RTN_URLList
		self.articleList = CNASpider.articleList
		self.newsLists = CNASpider.newsLists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(1,2):
			#Real-time news pages
			URL = 'http://www.cna.com.tw/list/aall-'+str(page)+'.aspx'
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find(class_ = 'article_list').findAll('li')
			for article in articles:
				articleURL = 'http://www.cna.com.tw'+article.find('a').get('href')
				self.articleList.append(articleURL)
		return self.articleList

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.articleList:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'news_article')
			content = ""
			newsList = []
			title = str(news.find('h1', {'itemprop':'headline'}).contents[0])
			time = news.find('div', {'class':'update_times'}).find('p', {'class':'blue'}).text.split('：')[1]
			article = news.find('div', {'class':'article_box'}).p.text
			print('新聞標題 : ' + title)
			print('------------------------------')
			print(time)
			print('------------------------------')
			for contents in article:
				content +=  str(contents)
			print(content)
			print('------------------------------')
			self.newsLists.append([title,time,content])
		return self.newsLists
