#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import dryscrape

class TPNSpider:
	RTN_URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.RTN_URLList = TPNSpider.RTN_URLList
		self.ARTICLE_List = TPNSpider.ARTICLE_List
		self.NEWS_Lists = TPNSpider.NEWS_Lists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(1,2):
			#Real-time news pages
			URL = 'http://www.peoplenews.tw/list/%E7%B8%BD%E8%A6%BD#page-'+str(page)
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			session = dryscrape.Session(base_url=URL)
			session.visit('')
			response = session.body()
			soup = bs4(response, 'html.parser')
			articles = soup.findAll('div',{'class':'list_realtime'})
			for article in articles:
				try:
					articleURL = 'http://www.peoplenews.tw'+ article.findAll('a')[0].get('href')
					self.ARTICLE_List.append(articleURL)
				except:
					pass
		return self.ARTICLE_List

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.ARTICLE_List:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(id = 'news')
			content = ""
			newsList = []
			title = str(news.find('h1').contents[0])
			time = news.find(class_ = 'date').text
			article = news.find('div', {'id':'newscontent'}).findAll('p')
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
