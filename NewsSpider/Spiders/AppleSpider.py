#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json

class Task:
	def __init__(self, name, number, balance):
		self.name = name
		self.number = number
		self.balance = balance

#Get real-time news url
def getRTNURL():
	RTN_URLList = []
	articleList = []
	for page in range(1,2):
		#Real-time news pages
		URL = 'http://www.appledaily.com.tw/realtimenews/section/new/'+str(page)
		RTN_URLList.append(URL)
	#Get articles url from real-time news pages
	for URL in RTN_URLList:
		r = requests.get(URL)
		soup = bs4(r.text, 'html.parser')
		articles = soup.find_all(class_ = 'rtddt')
		for article in articles:
			articleURL = 'http://www.appledaily.com.tw/'+article.find('a').get('href')
			articleList.append(articleURL)
	return articleList

# def checkUpdate():
# 	pass

#Get Content from article
def getContent(articleList):
	newsList_HTML = []
	newsLists = []
	for article in articleList:
		r = requests.get(article)
		soup = bs4(r.text, 'html.parser')
		news = soup.find(class_ = 'abdominis')
		newsList_HTML.append(news)

	for news_HTML in newsList_HTML:
		content = ""
		newsList = []
		title = str(news_HTML.find('h1', {'id':'h1'}).contents[0])
		article = news_HTML.find('p', {'id':'summary'}).findAll(text=True)

		print('新聞標題 : ' + title)
		print('------------------------------')
		for contents in article:
			content +=  str(contents)
		print(content)
		print('------------------------------')
		newsList.append([title,content])

def main():
	getContent(getRTNURL())

if __name__ == '__main__':
	main()
