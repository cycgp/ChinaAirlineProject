#coding:utf-8
from bs4 import BeautifulSoup as bs4
import json
import re
import requests
from selenium import webdriver
import sys
import time as t
from datetime import date, timedelta

import json

def getURL(self):
	page = 1
	state = True
	while state:
		EID_LIST = []
		timeList = []
		url = 'http://www.peoplenews.tw/resource/lists/ALL'
		payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"page\"\r\n\r\n" + str(page) + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"status\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
		headers = {
		    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
		    'cache-control': "no-cache",
		    'postman-token': "d5674e31-12ad-7724-03e3-c41687271841"
		    }
		r = requests.request("POST", url, data=payload, headers=headers)
		jsonResponse = json.loads(r.text)
		data_list = jsonResponse['data_list']
		for data in data_list:
			EID_LIST.append(data['EID'])
			timeList.append(data['PUBTIME'].split(' ')[0])
		if t.strftime('%Y%m%d', today) not in timeList and t.strftime('%Y%m%d', yesterday) not in timeList:
			state = False
		if state:
			page += 1
			self.URLList.append(URL)
		else:
			page -= 1
	#Get articles url from real-time news pages
	driver = webdriver.PhantomJS()
	for URL in self.URLList:
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

def getContent(ARTICLE_List, record):
	newsList = []
	articleIDList = []
	for articleURL in ARTICLE_List:
		t.sleep(0.5)
		if articleURL in record:
			continue
		r = requests.get(articleURL)
		soup = bs4(r.text, 'html.parser')
		news = soup.find(id = 'news')
		content = ""
		title = str(news.find('h1').contents[0])
		time = re.split('-| |:', news.find(class_ = 'date').text)
		datetime = '/'.join(time[:3])
		timeInNews = ':'.join(time[3:])
		article = news.find('div', {'id':'newscontent'}).findAll('p')

		if t.strftime('%Y/%m/%d', yesterday) not in datetime:
			continue
		else:
			pass

		articleID = ''.join(time)+'000'
		while articleID in articleIDList:
			articleID = str(int(articleID)+1)
		articleIDList.append(articleID)
		articleID = 'tpn'+articleID
		for contents in article:
			content +=  str(contents.text)
		newsList.append([articleID, articleURL, title, datetime + ' ' + timeInNews, content])
	return newsList

def test():
	EID_LIST = []
	timeList = []
	url = 'http://www.peoplenews.tw/resource/lists/ALL'

	page = 1
	payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"page\"\r\n\r\n" + str(page) + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"status\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
	headers = {
	    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
	    'cache-control': "no-cache",
	    'postman-token': "d5674e31-12ad-7724-03e3-c41687271841"
	    }

	r = requests.request("POST", url, data=payload, headers=headers)
	jsonResponse = json.loads(r.text)
	data_list = jsonResponse['data_list']
	for data in data_list:
		EID_LIST.append(data['EID'])
		timeList.append(data['PUBTIME'].split(' ')[0])
	print(EID_LIST)
	print(timeList)
test()
