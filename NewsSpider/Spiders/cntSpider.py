#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import time as t
import re

class cntSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = cntSpider.URLList
		self.ARTICLE_List = cntSpider.ARTICLE_List
		self.NEWS_Lists = cntSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		#Real-time news pages
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.chinatimes.com/realtimenews?page='+str(page)
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll('time')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.split()[1]
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
			articles = soup.find(class_ = 'listRight').findAll('h2')
			for article in articles:
				articleURL = 'http://www.chinatimes.com'+ article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'cnt', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		articleIDList = []
		for article in self.ARTICLE_List:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'page_container')
			content = ""
			newsList = []
			title = str(news.find('h1').contents[0])
			time = re.split('年|月|日|:| ', news.find('time').text)#time to list
			timeInNews = ':'.join(time[4:])
			datetime = '/'.join(time[:3])
			article = news.findAll('p')

			if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
				continue
			else:
				pass

			articleID = ''.join(time)+'0'
			print(articleID)
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'cnt'+articleID
			for contents in article:
				content +=  str(contents.text)
			self.NEWS_Lists.append([articleID, title,datetime + ' ' + timeInNews,content])
		return self.NEWS_Lists
