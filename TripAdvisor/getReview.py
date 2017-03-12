#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import time
import dryscrape

def generateURL():
	global URL_List
	for page in range(0,40):
		URL = 'https://www.tripadvisor.com.tw/Airline_Review-d8729049-Reviews-Cheap-Flights-or'+str(page)+'0-China-Airlines#Reviews'
		#Url of China Airline in Trip Advisor
		URL_List.append(URL)

def getReviewInfo(review):
	print(review.prettify())
	innerBubble = review.find("div", { "class" : "innerBubble" })
	quote = innerBubble.find("div", { "class" : "quote" }).span
	rating = innerBubble.find("div", { "class" : "rating" }).img['alt'].encode('utf-8').split(' ')[0]
	ratingDate = getDate(innerBubble.find("span", { "class" : "ratingDate" }))
	comment = getTextFromTag(innerBubble.find("p", { "class" : "partial_entry" }))
	try:
		labels = innerBubble.findAll("span", { "class" : "categoryLabel" }) #set of labels
		area = getTextFromTag(labels[0])
		seatClass = getTextFromTag(labels[1])
		route = getTextFromTag(labels[2])
		routeDetail = getRouteDetail(route)
	except:
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
		'orgin':routeDetail[0],
		'destination' : routeDetail[1]
	}
	# print(subjectCount)
	# print(str(getTextFromTag(quote)))
	# print(str(rating))
	# print(str(ratingDate))
	# print(str(comment))
	# print(str(area))
	# print(str(seatClass))
	# print(str(routeDetail[0]))
	# print(str(routeDetail[1]))
	# print('\n---\n')
	global list2json
	list2json.append(reviewDict)
	subjectCount += 1

def getDate(ratingDate):
	try:
		ratingDate = ratingDate['title'].encode('utf-8')
	except:
		ratingDate = getTextFromTag(ratingDate).split('的')[0]
	return ratingDate

def getRouteDetail(route):
	routeInfo = str(route).split(' - ')
	origin = routeInfo[0]
	destination = routeInfo[1]
	return [origin,destination]

def getTextFromTag(tag):
	return tag.contents[0].encode('utf-8')

def main():
	generateURL()
	global URL_List
	for URL in URL_List:
		time.sleep(1)
		session = dryscrape.Session()
		session.visit(URL)
		response = session.body()
		soup = bs4(response, 'html.parser')
		reviews = soup.findAll("div", { "class" : "reviewSelector" })
		for review in reviews:
			getReviewInfo(review)

if __name__ == '__main__':
	subjectCount = 0
	list2json = []
	URL_List= []
	main()
	#Pagination
	with open('data.json', 'w') as outfile:
	    json.dump(list2json, outfile, indent=4, sort_keys=True, ensure_ascii=False)
