#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import time as t

class CNASpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = CNASpider.URLList
		self.ARTICLE_List = CNASpider.ARTICLE_List
		self.NEWS_Lists = CNASpider.NEWS_Lists
	#Get real-time news url
	def getURL(self):
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.cna.com.tw/list/aall-'+str(page)+'.aspx'
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.find('div', {'class':'article_list'}).findAll('span')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.split(' ')[0]
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
			articles = soup.find(class_ = 'article_list').findAll('li')
			for article in articles:
				articleURL = 'http://www.cna.com.tw'+article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'cna', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for article in self.ARTICLE_List:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'news_article')
			content = ""
			newsList = []
			title = str(news.find('h1', {'itemprop':'headline'}).contents[0])
			time = news.find('div', {'class':'update_times'}).find('p', {'class':'blue'}).text.split('：')[1]
			article = news.find('div', {'class':'article_box'}).p.text
			if t.strftime('%Y/%m/%d', t.localtime()) not in time:
				continue
			else:
				pass
			print('新聞標題 : ' + title.strip())
			print('------------------------------')
			print(time)
			print('------------------------------')
			for contents in article:
				content +=  str(contents)
			print(content)
			print('------------------------------')
			self.NEWS_Lists.append([title,time,content])
		return self.NEWS_Lists
