#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import re
import time as t

class tnlSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = tnlSpider.URLList
		self.ARTICLE_List = tnlSpider.ARTICLE_List
		self.NEWS_Lists = tnlSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'https://www.thenewslens.com/news?page='+str(page)
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll(class_ = 'time')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.split(' ')[1]
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
			articles = soup.find_all(class_ = 'info-box')
			for article in articles:
				articleURL = article.findAll('a')[1].get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'tnl', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		articleIDList = []
		for article in self.ARTICLE_List:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'article-title-box')
			content = ""
			newsList = []
			title = str(news.find('h1', {'class':'article-title'}).header.contents[0])
			time = news.find(class_ = 'article-info').text.split(',')[0].replace(' ','')
			article = soup.find(class_ = 'article-content').findAll('p')

			if t.strftime('%Y/%m/%d', t.localtime()) not in time:
				continue
			else:
				pass

			articleID = ''.join(re.split('/', time))[:8]+'0'
			print(articleID)
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'tnl'+articleID
			for contents in article:
				content +=  str(contents.text)
			self.NEWS_Lists.append([articleID, title,time,content])
		return self.NEWS_Lists
