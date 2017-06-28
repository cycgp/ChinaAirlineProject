from Spiders.NewsSpider import aplSpider, cldSpider, cnaSpider, cntSpider, ltnSpider, ntkSpider, stmSpider, tnlSpider, tpnSpider, udnSpider
from Spiders.NewsSpiderCheck import aplSpiderCheck, cldSpiderCheck, cnaSpiderCheck, cntSpiderCheck, ltnSpiderCheck, ntkSpiderCheck, stmSpiderCheck, tnlSpiderCheck, tpnSpiderCheck, udnSpiderCheck
import logging
import time

logging.basicConfig(level=logging.INFO,
					format='[%(levelname)-4s - %(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S ',
					handlers = [logging.FileHandler('newsSpider'+'.log', 'a', 'utf-8'),])

press = ['Apple', 'CNA', 'China Times', 'Liberty Times', 'New Talks', 'Storm', 'The News Lens', 'Taiwan People News', 'UDN']
pressAbbr = ['apl', 'cna', 'cnt', 'ltn', 'ntk', 'stm', 'tnl', 'tpn', 'udn']
spiders = [aplSpider(), cnaSpider(), cntSpider(), ltnSpider(), ntkSpider(), stmSpider(), tnlSpider(), tpnSpider(), udnSpider()]
spidersCheck = [aplSpiderCheck(), cnaSpiderCheck(), cntSpiderCheck(), ltnSpiderCheck(), ntkSpiderCheck(), stmSpiderCheck(), tnlSpiderCheck(), tpnSpiderCheck(), udnSpiderCheck()]
#press = ['Liberty Times']
#pressAbbr = ['ltn']
#spiders = [ltnSpider()]
#spidersCheck = [ltnSpiderCheck()]

def getNewsList(state):
	print("Getting News List...")
	NewsLists = []
	for i in range(0,len(press)):
		print('\n    Loading ' + press[i] + ' List...', end="", flush=True)
		try:
			if state == 'new':
				newsList = spiders[i].getURL()
			elif state == 'check':
				newsList = spidersCheck[i].getURL()
			NewsLists.append(newsList)
			print("  DONE")
		except:
			print('  FAILED')
			logging.exception(press[i]+' List problems : \n')
			pass

	print('\n')
	return NewsLists

def getContent(state, NewsLists, record):
	print('Getting content from news list...\n')
	newsContentList = []
	for NewsList in NewsLists:
		index = pressAbbr.index(NewsList['press'])
		print("    Loading " + press[index] + " List...")
		try:
			if state == 'new':
				newsContentList.extend(spiders[index].getContent(NewsList['URLList'], record))
			elif state == 'check':
				newsContentList.extend(spidersCheck[index].getContent(NewsList['URLList'], record))
			print('\r        [---DONE---]  '+time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())+'                                         ')
		except:
			print('\r        [--FAILED--]  '+time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())+'                                         ')
			logging.exception(press[index]+' List problems : \n')
			pass
	return  newsContentList
