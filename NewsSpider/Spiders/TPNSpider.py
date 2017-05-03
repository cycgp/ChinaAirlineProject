#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import requests
import json
import time as t
import re

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
		page = 1
		state = True
		while state:
			#Real-time news pages
			URL = 'http://www.peoplenews.tw/list/%E7%B8%BD%E8%A6%BD#page-'+str(page)
			driver = webdriver.PhantomJS(executable_path = 'C:\\Users\\Bob\\AppData\\Local\\Programs\\Python\\Python36-32\\Scripts\\phantomjs-2.1.1-windows\\phantomjs.exe')
			r = driver.get(URL)
			pageSource = driver.page_source
			soup = bs4(pageSource, 'html.parser')
			timeList = soup.findAll('div', {'class':'date'})
			for time in timeList:
				timeList[timeList.index(time)] = (time.text).split(' ')[1].replace('-','')
			state = t.strftime('%Y%m%d', t.localtime()) in timeList
			if state:
				page += 1
				self.URLList.append(URL)	
			else:
				page -= 1
			
		#Get articles url from real-time news pages
		for URL in self.URLList:
			driver = webdriver.PhantomJS(executable_path = 'C:\\Users\\Bob\\AppData\\Local\\Programs\\Python\\Python36-32\\Scripts\\phantomjs-2.1.1-windows\\phantomjs.exe')
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
		return {'press':'tpn', 'URLList':self.ARTICLE_List}

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		articleIDList = []
		for article in self.ARTICLE_List:
			r = requests.get(article)
			soup = bs4(r.text, 'html.parser')
			news = soup.find(id = 'news')
			content = ""
			newsList = []
			title = str(news.find('h1').contents[0])
			time = re.split('-| |:', news.find(class_ = 'date').text)
			datetime = '/'.join(time[:3])
			timeInNews = ':'.join(time[3:])
			print(time)
			print(datetime)
			print(timeInNews)
			article = news.find('div', {'id':'newscontent'}).findAll('p')

			if t.strftime('%Y/%m/%d', t.localtime()) not in datetime:
				continue
			else:
				pass

			print('新聞標題 : ' + title)
			print('------------------------------')
			print(datetime + ' ' + timeInNews)
			print('------------------------------')
			for contents in article:
			    content +=  str(contents.text)
			print(content)
			print('------------------------------')

			articleID = ''.join(time)+'0'
			print(articleID)
			while articleID in articleIDList:
				articleID = str(int(articleID)+1)
			articleIDList.append(articleID)
			articleID = 'tpn'+articleID
			for contents in article:
				content +=  str(contents)
			self.NEWS_Lists.append([articleID, title,datetime + ' ' + timeInNews,content])
		return self.NEWS_Lists
