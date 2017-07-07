#coding:utf-8
import facebook
import requests
import json

def getLikesSummary(posts):
	for a in posts['data']:
		if 'message' in a:
			global SID
			print(str(SID)+':')
			SID += 1
			r = requests.get('https://graph.facebook.com/'+str(a['id'])+'/?fields=created_time,message&access_token='+token)
			post_dict = json.loads(r.text)
			print(post_dict['created_time'])
			print(post_dict['message'])
			r = requests.get('https://graph.facebook.com/'+str(a['id'])+'/likes?summary=true&access_token='+token)
			likes_dict = json.loads(r.text)
			print(likes_dict['summary'])

def getNextPage(posts):
	if posts['paging']['next'] != None:
		r = requests.get(posts['paging']['next'])
		nextPageDict = json.loads(r.text)
		getLikesSummary(nextPageDict)
	getNextPage(nextPageDict)

if __name__ == '__main__':
	token = 'EAACEdEose0cBAAnIeMwcZAXHSwfwppKThWBHJnzhFjvvtZBDIfj4yFvAqNCpK1H4rO6ZCmt5i9mwVgyFY9hYZAjJRo7rl11a8lVHcblzVLqUZAEuLQT4bFlHRKkJwrqMIQN0qpUKfSVvmTwzmeHo8RWZBflNrY1toaAEBV47X8xH8apaukBZBBbZBRe5LEuDCXoZD'
	#facebook token
	graph = facebook.GraphAPI(access_token = token)
	posts = graph.get_connections(id='119474188105563', connection_name='posts')
	print ("\n--")
	SID = 1
	getLikesSummary(posts)
	#Get summary of all likes in a post
	getNextPage(posts)
	#Get next page
