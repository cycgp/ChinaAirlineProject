#!/usr/bin/python3
import sys
import threading
import time

class getURLThread(threading.Thread):
	def __init__(self, name, spider):
		threading.Thread.__init__(self)
		self.name = name
		self.spider = spider
		self.newsList = []

	def run(self):
		print ('    Starting ' + self.name + time.strftime('  %Y/%m/%d %H:%M:%S', time.localtime()))
		self.newsList = self.spider.getURL()
		time.sleep(1)
		print ('    Exiting ' + self.name + time.strftime('   %Y/%m/%d %H:%M:%S', time.localtime()))

class getContentThread(threading.Thread):
	def __init__(self, name, spider, URLList, record):
		threading.Thread.__init__(self)
		self.name = name
		self.spider = spider
		self.newsList = []
		self.URLList = URLList
		self.record = record

	def run(self):
		print ('    Starting ' + self.name + time.strftime('  %Y/%m/%d %H:%M:%S', time.localtime()))
		self.newsList = self.spider.getContent(self.URLList, self.record)
		time.sleep(1)
		sys.stdout.write('\r             ' + ' '*65)
		sys.stdout.write('\r    Exiting ' + self.name + time.strftime('   %Y/%m/%d %H:%M:%S', time.localtime()) + '\n')
