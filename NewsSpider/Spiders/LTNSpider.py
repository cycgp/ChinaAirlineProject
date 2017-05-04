#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import time as t
import re

class LTNSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = LTNSpider.URLList
		self.ARTICLE_List = LTNSpider.ARTICLE_List
		self.NEWS_Lists = LTNSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		#Real-time news pages
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://news.ltn.com.tw/list/BreakingNews?page='+str(page)
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll('li', {'class':'lipic'})
			for time in timeList:
				timeList[timeList.index(time)] = time.span.text.split()[0]
			state = t.strftime('%Y-%m-%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find_all('a', {'class' : 'picword'})
			for article in articles:
				articleURL = article.get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'ltn', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		articleIDList = []
		for article in self.ARTICLE_List:
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
			if t.strftime('%Y-%m-%d', t.localtime()) not in time.split()[0]:
				continue
			else:
				pass

			for contents in article:
				content +=  str(contents.text)

			time = re.split('-|\xa0\xa0|:', time)
			datetime = '/'.join(time[:3])
			timeInNews = ':'.join(time[3:])
			articleID = ''.join(time)+'0'
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'ltn'+articleID
			self.NEWS_Lists.append([articleID, title,datetime + ' ' + timeInNews,content])
		return self.NEWS_Lists
