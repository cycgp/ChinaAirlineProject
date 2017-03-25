#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class UDNSpider:
	RTN_URLList = []
	articleList = []
	newsLists = []
	def __init__(self):
		self.RTN_URLList = UDNSpider.RTN_URLList
		self.articleList = UDNSpider.articleList
		self.newsLists = UDNSpider.newsLists

	#Get real-time news url
	def getRTNURL(self):
		i = 0
		for page in range(1,2):
			#Real-time news pages
			URL = 'https://udn.com/news/breaknews/1/99/'+str(page)+'#breaknews'
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find(id = 'breaknews_body').find_all('dt')
			for article in articles:
				articleURL = 'https://udn.com/'+article.find('a').get('href')
				self.articleList.append(articleURL)
		return self.articleList

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.articleList:
			session = dryscrape.Session()
			session.visit(article)
			response = session.body()
			soup = bs4(response, 'html.parser')
			news = soup.find(id = 'story_body_content')
			content = ""
			newsList = []
			title = str(news.find('h1', {'id':'story_art_title'}).contents[0])
			time = str(news.find('div', {'class':'story_bady_info_author'}))
			timeSoup = bs4(time, 'html.parser')
			timeSoup.span.decompose()
			article = news.findAll('p')
			print('新聞標題 : ' + title)
			print('------------------------------')
			print(timeSoup.div.text)
			print('------------------------------')
			for contents in article:
				try:
					content +=  str(contents.contents[0])
				except:
					pass
			print(content)
			print('------------------------------')
			self.newsLists.append([title,time,content])
		return self.newsLists
