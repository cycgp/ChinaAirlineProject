#coding:utf-8
from bs4 import BeautifulSoup as bs4
import time as t
import requests
import json
import sys
import re

class aplSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = aplSpider.URLList
		self.ARTICLE_List = aplSpider.ARTICLE_List
		self.NEWS_Lists = aplSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.appledaily.com.tw/realtimenews/section/new/'+str(page)
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			soup = soup.find('time').text.replace(' / ','')
			state = t.strftime('%y%m%d', t.localtime()) in soup
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find_all(class_ = 'rtddt')
			for article in articles:
				inListURL = article.find('a').get('href')
				articleURL = article.find('a').get('href') if 'http://www.appledaily.com.tw' in inListURL else 'http://www.appledaily.com.tw'+article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'apl', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		articleIDList = []
		for article in self.ARTICLE_List:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'abdominis')
			content = ""
			title = news.find('h1', {'id':'h1'}).contents[0]
			time = re.split('年|月|日|:', news.find('time').text)#time to list
			timeInNews = ':'.join(time[3:])
			datetime = '/'.join(time[:3])
			article = news.find('p', {'id':'summary'}).findAll(text=True)

			#filter fault news
			if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
				continue
			else:
				pass

			articleID = ''.join(time)+'0'
			print(articleID)
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'apl'+articleID
			for contents in article:
				content +=  str(contents)
			self.NEWS_Lists.append([articleID, title,datetime + ' ' + timeInNews,content])
		return self.NEWS_Lists
