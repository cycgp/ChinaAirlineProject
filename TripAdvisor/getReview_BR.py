#coding:utf-8
from bs4 import BeautifulSoup as bs4
import json
import time
from selenium import webdriver

#generate url of Trip Advisor
def generateURL():
	global URL_List
	for page in range(0,62):
		URL = 'https://www.tripadvisor.com.tw/Airline_Review-d8729076-Reviews-Cheap-Flights-or'+str(page)+'0-EVA-Air#REVIEWS'

		URL_List.append(URL)

#get review detail
def getReviewInfo(review):
	#print(review.prettify())
	innerBubble = review.find("div", { "class" : "innerBubble" })
	quote = innerBubble.find("div", { "class" : "quote" }).span
	try:
		rating = innerBubble.find("div", { "class" : "rating" }).span['alt'].split('.')[0]
	except KeyError:
		rating = innerBubble.find("div", { "class" : "rating" }).img['alt'].split(' ')[0]
	ratingDate = getDate(innerBubble.find("span", { "class" : "ratingDate" })).decode('utf-8')
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
	return tag.contents[0]

def main():
	generateURL()
	global URL_List
	for URL in URL_List:
		time.sleep(1)
		#use dryscrape instead of request to run javascript
		driver = webdriver.PhantomJS(executable_path = 'C:\\Users\\Bob\\AppData\\Local\\Programs\\Python\\Python36-32\\Scripts\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
		r = driver.get(URL)
		pageSource = driver.page_source
		soup = bs4(pageSource, 'html.parser')
		reviews = soup.findAll("div", { "class" : "reviewSelector" })
		for review in reviews:
			getReviewInfo(review)

if __name__ == '__main__':
	subjectCount = 0
	list2json = []
	URL_List= []
	main()
	#Pagination
	with open('data_BR.json', 'w', encoding='utf-8') as outfile:
	    json.dump(list2json, outfile, indent=4, sort_keys=True, ensure_ascii=False)
