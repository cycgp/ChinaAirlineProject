from Spiders.NewsSpider import aplSpider, cldSpider, cnaSpider, cntSpider, ltnSpider, ntkSpider, stmSpider, tnlSpider, tpnSpider, udnSpider
from Spiders.NewsSpiderCheck import aplSpiderCheck, cldSpiderCheck, cnaSpiderCheck, cntSpiderCheck, ltnSpiderCheck, ntkSpiderCheck, stmSpiderCheck, tnlSpiderCheck, tpnSpiderCheck, udnSpiderCheck
from Spiders.Threading import getURLThread, getContentThread
import logging
import time

logging.basicConfig(level=logging.INFO,
					format='[%(levelname)-4s - %(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S ',
					handlers = [logging.FileHandler('NewsSpider'+'.log', 'a', 'utf-8'),])

press = ['Apple', 'CNA', 'China Times', 'Liberty Times', 'New Talks', 'Storm', 'The News Lens', 'Taiwan People News', 'UDN']
pressAbbr = ['apl', 'cna', 'cnt', 'ltn', 'ntk', 'stm', 'tnl', 'tpn', 'udn']
spiders = [aplSpider(), cnaSpider(), cntSpider(), ltnSpider(), ntkSpider(), stmSpider(), tnlSpider(), tpnSpider(), udnSpider()]
spidersCheck = [aplSpiderCheck(), cnaSpiderCheck(), cntSpiderCheck(), ltnSpiderCheck(), ntkSpiderCheck(), stmSpiderCheck(), tnlSpiderCheck(), tpnSpiderCheck(), udnSpiderCheck()]
#press = ['Liberty Times']
#pressAbbr = ['ltn']
#spiders = [ltnSpider()]
#spidersCheck = [ltnSpiderCheck()]

def getNewsList(state):
	getNewsListThreads = []
	print("Getting News List...")
	NewsLists = []
	for i in range(0,len(press)):
		try:
			if state == 'new':
				newThread = getURLThread(pressAbbr[i]+'Thread', spiders[i])
				#newsList = spiders[i].getURL()
			elif state == 'check':
				newThread = getURLThread(pressAbbr[i]+'Thread', spidersCheck[i])
			getNewsListThreads.append(newThread)
		except:
			logging.exception(press[i]+' List problems : \n')
			pass

	for  thread in getNewsListThreads:
		thread.start()

	for  thread in getNewsListThreads:
		thread.join()

	for  thread in getNewsListThreads:
		NewsLists.append(thread.newsList)

	print('\n    [--Exiting getNewsList Threads--]\n')
	return NewsLists

def getContent(state, NewsLists, record):
	getContentThreads = []
	print('Getting content from news list...\n')
	newsContentList = []
	for NewsList in NewsLists:
		index = pressAbbr.index(NewsList['press'])
		try:
			if state == 'new':
				newThread = getContentThread(pressAbbr[index]+'Thread', spiders[index], NewsList['URLList'], record)
			elif state == 'check':
				newThread = getContentThread(pressAbbr[index]+'Thread', spidersCheck[index], NewsList['URLList'], record)
			getContentThreads.append(newThread)
		except:
			logging.exception(press[index]+' List problems : \n')
			pass

	for  thread in getContentThreads:
		thread.start()

	for  thread in getContentThreads:
		thread.join()

	for  thread in getContentThreads:
		newsContentList.extend(thread.newsList)

	print('\n    [--Exiting getContent Threads--]\n')
	return  newsContentList
