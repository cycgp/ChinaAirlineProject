#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import requests
import json

class TPNSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = TPNSpider.URLList
		self.ARTICLE_List = TPNSpider.ARTICLE_List
		self.NEWS_Lists = TPNSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		i = 0
		for page in range(1,2):
			#Real-time news pages
			URL = 'http://www.peoplenews.tw/list/%E7%B8%BD%E8%A6%BD#page-'+str(page)
			self.URLList.append(URL)
		#Get articles url from real-time news pages
		for URL in self.URLList:
			driver = webdriver.PhantomJS()
			r = driver.get(URL)
			pageSource = driver.page_source
			soup = bs4(pageSource, 'html.parser')
			articles = soup.find('div', {'id':'area_list'}).findAll('a')
			for article in articles:
				try:
					articleURL = 'http://www.peoplenews.tw'+ article.get('href')
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
