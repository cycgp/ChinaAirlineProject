#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import requests
import json
import time as t
import re

class udnSpider:
	URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.URLList = udnSpider.URLList
		self.ARTICLE_List = udnSpider.ARTICLE_List
		self.NEWS_Lists = udnSpider.NEWS_Lists

	#Get real-time news url
	def getURL(self):
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'https://udn.com/news/breaknews/1/99/'+str(page)+'#breaknews'
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			timeList = soup.findAll(class_ = 'dt')
			for time in timeList:
				timeList[timeList.index(time)] = time.text.split(' ')[0]
			state = t.strftime('%m-%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)
			else:
				page -= 1
		#Get articles url from real-time news pages
		for URL in self.URLList:
			r = requests.get(URL)
			soup = bs4(r.text, 'html.parser')
			articles = soup.find(id = 'breaknews_body').find_all('dt')
			for article in articles:
				articleURL = 'https://udn.com/'+article.find('a').get('href')
				self.ARTICLE_List.append(articleURL)
		return {'press':'udn', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		articleIDList = []
		for article in self.ARTICLE_List:
			driver = webdriver.PhantomJS()
			r = driver.get(article)
			pageSource = driver.page_source
			soup = bs4(pageSource, 'html.parser')
			news = soup.find(id = 'story_body_content')
			content = ""
			newsList = []
			title = str(news.find('h1', {'id':'story_art_title'}).contents[0])
			time = news.find('div', {'class':'story_bady_info_author'})
			span = time.find('span')
			if span is not None:
				span.extract()
			time = re.split('-| |:', time.text)
			datetime = '/'.join(time[:3])
			timeInNews = ':'.join(time[3:])
			article = news.findAll('p')

			if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
				continue
			else:
				pass

			print('新聞標題 : ' + title)
			print('------------------------------')
			print(datetime + ' ' + timeInNews)
			print('------------------------------')
			for contents in article:
				try:
					content +=  str(contents.text)
				except:
					pass
			print(content)
			print('------------------------------')

			articleID = ''.join(time)+'0'
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'udn'+articleID
			for contents in article:
				content +=  str(contents.text)
			self.NEWS_Lists.append([articleID, title, datetime + ' ' + timeInNews, content])
		return self.NEWS_Lists
