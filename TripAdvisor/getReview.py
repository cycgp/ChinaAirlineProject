#coding:utf-8
from bs4 import BeautifulSoup as bs4
import json
import time
from selenium import webdriver
import re

#get review detail
def getReviewInfo(review):
	#print(review.prettify())
	innerBubble = review.find("div", { "class" : "innerBubble" })
	quote = innerBubble.find("div", { "class" : "quote" }).span
	rating = innerBubble.find("div", { "class" : "rating reviewItemInline" }).span['class'][1].split('bubble_')[1].replace('0','')
	ratingDate = getDate(innerBubble.find("span", { "class" : "ratingDate" })).decode('utf-8')
	try:
		comment = getTextFromTag(review.findAll("div", { "class" : "entry" })[1]).replace(' ','').replace('\n','')
	except:
		comment = getTextFromTag(innerBubble.find("p", { "class" : "partial_entry" })).replace(' ','').replace('\n','')

	try:
		labels = innerBubble.findAll("span", { "class" : "categoryLabel" }) #set of labels
		area = getTextFromTag(labels[0])
		seatClass = getTextFromTag(labels[1])
		route = getTextFromTag(labels[2])
		routeDetail = getRouteDetail(route)
	except:
		#avoid no label review
		area = ''
		seatClass = ''
		routeDetail = ['','']
	global subjectCount
	reviewDict = {
		'id': subjectCount,
		'title': getTextFromTag(quote),
		'rating':rating,
		'date':ratingDate,
		'comment':comment,
		'area':area,
		'class':seatClass,
		'origin':routeDetail[0],
		'destination' : routeDetail[1]
	}
	print(subjectCount)
	print(str(getTextFromTag(quote)))
	print(str(rating))
	print(str(ratingDate))
	print(str(comment))
	print(str(area))
	print(str(seatClass))
	print(str(routeDetail[0]))
	print(str(routeDetail[1]))
	print('\n---\n')
	global list2json
	#add review detail to dictionary
	list2json.append(reviewDict)
	subjectCount += 1

def getDate(ratingDate):
	try:
		ratingDate = ratingDate['title'].encode('utf-8')
	except:
		ratingDate = getTextFromTag(ratingDate).split('的')[0].encode('utf-8')
	return ratingDate

#get origin and destination
def getRouteDetail(route):
	routeInfo = str(route).split(' - ')
	origin = routeInfo[0]
	destination = routeInfo[1]
	return [origin,destination]

def getTextFromTag(tag):
	return tag.text

def main():
	page = 0
	state = True
	while  state:
		URL = 'https://www.tripadvisor.com.tw/Airline_Review-d8729049-Reviews-Cheap-Flights-or'+str(page)+'0-China-Airlines#Reviews'
		driver = webdriver.PhantomJS(executable_path = 'C:\\Users\\Bob\\AppData\\Local\\Programs\\Python\\Python36-32\\Scripts\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
		driver.get(URL)
		pageSource = driver.page_source
		soup = bs4(pageSource, 'html.parser')
		state = 'next' not in soup.find('div',{'class':'unified pagination '}).span['class'][:3]
		time.sleep(1)
		moreLinkID = soup.findAll("div", { 'class' : 'reviewSelector'})
		articleID =  moreLinkID[0]['id']
		script = "      ta.util.cookie.setPIDCookie(4444); ta.call('ta.servlet.Reviews.expandReviews', {type: 'dummy'}, ta.id('" + articleID + "'), '" + articleID + "', '1', 4444);"
		driver.execute_script(script)
		script = "return document.getElementsByTagName('html')[0].innerHTML;"
		time.sleep(3)
		html = driver.execute_script(script)
		pageSource = driver.page_source
		soup = bs4(pageSource, 'html.parser')
		reviews = soup.findAll("div", { "class" : "reviewSelector" })
		for review in reviews:
			getReviewInfo(review)
		page += 1

if __name__ == '__main__':
	subjectCount = 0
	list2json = []
	URL_List= []
	main()
	#Pagination
	with open('data_CI.json', 'w', encoding='utf-8') as outfile:
	    json.dump(list2json, outfile, indent=4, sort_keys=True, ensure_ascii=False)
