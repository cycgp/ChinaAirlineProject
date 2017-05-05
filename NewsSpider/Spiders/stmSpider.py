#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import re
import time as t

class stmSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = stmSpider.URLList
		self.ARTICLE_List = stmSpider.ARTICLE_List
		self.NEWS_Lists = stmSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.storm.mg/articles/'+str(page)
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll(class_ = 'main_date')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.replace('年','/').replace('月','/').replace('日','').split(' ')[0]
			state = t.strftime('%Y/%m/%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.findAll(class_ = 'main_content')
			for article in articles:
				articleURL = 'http://www.storm.mg'+ article.find('p').find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'stn', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		articleIDList = []
		for article in self.ARTICLE_List:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'inner-wrap')
			content = ""
			newsList = []
			title = news.find('h1', {'class':'title'}).text.strip()
			time = re.split('年|月|日| |:|風傳媒',news.find(class_='date').text)
			datetime = '/'.join(time[:3])
			timeInNews = ':'.join(time[4:6])
			article = news.article.findAll('p')

			if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
				continue
			else:
				pass

			articleID = ''.join(time)+'0'
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'stm'+articleID
			for contents in article:
				content +=  str(contents.text.strip())

			content = ''.join(re.split(' |[\n]|[\t]|[\r]', content))
			self.NEWS_Lists.append([articleID, article, title, datetime + ' ' + timeInNews, content])
		return self.NEWS_Lists
