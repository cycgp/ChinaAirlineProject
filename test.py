#coding:utf-8
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import requests
import json
import time as t

t.strftime('%Y/%m/%d', t.localtime())

URL = 'http://www.coolloud.org.tw/story?page=0'
r = requests.get(URL)
soup = bs4(r.text, 'html.parser')
timeList = soup.findAll('span', {'class':'date-display-single'})
state = True
for time in timeList:
	timeList[timeList.index(time)] = time.text
print(timeList)
