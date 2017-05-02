#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import requests
import json

class CLSpider:
	RTN_URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.RTN_URLList = CLSpider.RTN_URLList
		self.ARTICLE_List = CLSpider.ARTICLE_List
		self.NEWS_Lists = CLSpider.NEWS_Lists

	#Get real-time news url
	def getRTNURL(self):
		for page in range(0,2):
			#Real-time news pages
			URL = 'http://www.coolloud.org.tw/story?page='+str(page)
			self.RTN_URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.RTN_URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll('div', {'class':'field-content pc-style'})
			for article in articles:
				articleURL = 'http://www.coolloud.org.tw'+ article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return self.ARTICLE_List

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.ARTICLE_List:
			driver = webdriver.PhantomJS(executable_path = 'C:\\Users\\Bob\\AppData\\Local\\Programs\\Python\\Python36-32\\Scripts\\phantomjs-2.1.1-windows\\phantomjs.exe')
			r = driver.get(article)
			pageSource = driver.page_source
			soup = bs4(pageSource, 'html.parser')
			news = soup.find(class_ = 'main-container')
			content = ""
			newsList = []
			title = str(news.find('p').contents[0])
			time = news.find(class_ ='date-display-single')
			article = news.find(class_ = 'node node-post node-promoted clearfix').findAll('p')
			print('新聞標題 : ' + title)
			print('------------------------------')
			print(time.text)
			print('------------------------------')
			for contents in article:
				content +=  str(contents.text)
			print(content)
			print('------------------------------')
			self.NEWS_Lists.append([title,time,content])
		return self.NEWS_Lists
