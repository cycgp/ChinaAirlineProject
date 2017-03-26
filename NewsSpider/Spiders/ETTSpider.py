#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import time
import dryscrape

class ETTSpider:
	RTN_URLList = []
	ARTICLE_List = []
	NEWS_Lists = []
	def __init__(self):
		self.RTN_URLList = ETTSpider.RTN_URLList
		self.ARTICLE_List = ETTSpider.ARTICLE_List
		self.NEWS_Lists = ETTSpider.NEWS_Lists

	#Get real-time news url
	def getRTNURL(self):
		response = requests.get('http://www.ettoday.net/news/news-list.htm')
		soup = bs4(response.text, 'html.parser')
		links = soup.find('div', {'class':'part_list_2'}).findAll('h3')
		for link in links:
			title = link.a.text
			date = link.span.text
			href = 'http://www.ettoday.net'+link.a.get('href')
			self.ARTICLE_List.append([title,date,href])

		url = "http://www.ettoday.net/show_roll.php"
		for j in range(1,50):
			payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"offset\"\r\n\r\n"+str(j)+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"tPage\"\r\n\r\n3\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"tFile\"\r\n\r\n20170326.xml\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"tOt\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"tSi\"\r\n\r\n100\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
			headers = {
				'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
				'cache-control': "no-cache",
				'postman-token': "79a5b044-75b7-ceed-8758-37b670dcc18c"
				}
			response = requests.request("POST", url, data=payload, headers=headers)
			soup = bs4(response.text, 'html.parser')
			links = soup.findAll('h3')
			for link in links:
				title = link.a.text
				date = link.span.text
				href = 'http://www.ettoday.net'+link.a.get('href')
				self.ARTICLE_List.append([title,date,href])
		return self.ARTICLE_List

	# def checkUpdate():
	# 	pass

	#Get Content from article
	def getContent(self):
		for articles in self.ARTICLE_List:
			r = requests.get(articles[2])
			soup = bs4(r.text, 'html.parser')
			news = soup.find(class_ = 'story')
			content = ""
			article = news.findAll('p')
			del article[:2]
			print('新聞標題 : ' + articles[0])
			print('------------------------------')
			print(articles[1])
			print('------------------------------')
			for contents in article:
				try:
					[x.extract() for x in contents.findAll('strong')]
				except:
					pass
				content +=  str(contents.text)
			print(content)
			print('------------------------------')
			self.NEWS_Lists.append([articles[0], articles[1], content])
		return self.NEWS_Lists
