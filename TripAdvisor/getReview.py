#coding:utf-8
from bs4 import BeautifulSoup as bs4
import requests
import json
import io

def getReviewInfo(review):
	innerBubble = review.find("div", { "class" : "innerBubble" })
	quote = innerBubble.find("div", { "class" : "quote" }).span
	rating = innerBubble.find("div", { "class" : "rating" }).img['alt'].encode('utf-8').split(' ')[0]
	ratingDate = innerBubble.find("span", { "class" : "ratingDate" })['title'].encode('utf-8')
	comment = getTextFromTag(innerBubble.find("p", { "class" : "partial_entry" }))
	labels = innerBubble.findAll("span", { "class" : "categoryLabel" }) #set of labels
	area = getTextFromTag(labels[0])
	seatClass = getTextFromTag(labels[1])
	route = getTextFromTag(labels[2])
	routeDetail = getRouteDetail(route)
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
	# reviewDict = {
	# 	'id': subjectCount,
	# 	'title': str(getTextFromTag(quote)),
	# 	'rating':str(rating),
	# 	'date':str(ratingDate),
	# 	'comment':str(comment),
	# 	'area':str(area),
	# 	'class':str(seatClass),
	# 	'orgin':str(routeDetail[0]),
	# 	'orgin' : str(routeDetail[1])
	# }
	global list2json
	list2json.append(reviewDict)
	subjectCount += 1

def getRouteDetail(route):
	routeInfo = str(route).split(' - ')
	origin = routeInfo[0]
	destination = routeInfo[1]
	return [origin,destination]

def getTextFromTag(tag):
	return tag.contents[0].encode('utf-8')

page = 0
subjectCount = 0
list2json = []
#Pagination
URL = 'https://www.tripadvisor.com.tw/Airline_Review-d8729049-Reviews-Cheap-Flights-or'+str(page)+'0-China-Airlines#Reviews'
#Url of China Airline in Trip Advisor

r = requests.get(URL)
soup = bs4(r.text, 'html.parser')
reviews = soup.findAll("div", { "class" : "reviewSelector" })

for review in reviews:
	getReviewInfo(review)

with open('data.json', 'w') as outfile:
    json.dump(list2json, outfile, indent=4, sort_keys=True, ensure_ascii=False)

# for review in reviews:
# 	subjectCount += 1
# 	print(review)
# 	print("--\n")
# 	print(subjectCount)
