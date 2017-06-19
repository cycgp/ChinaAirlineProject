from Spiders.NewsSpider import aplSpider, cldSpider, cnaSpider, cntSpider, ltnSpider, ntkSpider, stmSpider, tnlSpider, tpnSpider, udnSpider
from Spiders.NewsSpiderCheck import aplSpiderCheck, cldSpiderCheck, cnaSpiderCheck, cntSpiderCheck, ltnSpiderCheck, ntkSpiderCheck, stmSpiderCheck, tnlSpiderCheck, tpnSpiderCheck, udnSpiderCheck
import logging
import time

logging.basicConfig(level=logging.INFO,
					format='[%(levelname)-4s - %(asctime)-4s] %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S ',
					handlers = [logging.FileHandler('log-'+time.strftime('%Y%m%d%H%M%S', time.localtime())+'.log', 'w', 'utf-8'),])

press = ['Apple', 'CNA', 'China Times', 'Liberty Times', 'New Talks', 'Storm', 'The News Lens', 'Taiwan People News', 'UDN']
pressAbbr = ['apl', 'cna', 'cnt', 'ltn', 'ntk', 'stm', 'tnl', 'tpn', 'udn']
spiders = [aplSpider(), cnaSpider(), cntSpider(), ltnSpider(), ntkSpider(), stmSpider(), tnlSpider(), tpnSpider(), udnSpider()]
spidersCheck = [aplSpiderCheck(), cnaSpiderCheck(), cntSpiderCheck(), ltnSpiderCheck(), ntkSpiderCheck(), stmSpiderCheck(), tnlSpiderCheck(), tpnSpiderCheck(), udnSpiderCheck()]

def getNewsList(state):
	print("Getting News List...")
	NewsLists = []
	for i in range(0,9):
		print('    Loading ' + press[i] + ' List...', end="", flush=True)
		try:
			if state == 'new':
				newsList = spiders[i].getURL()
			elif state == 'check':
				newsList = spidersCheck[i].getURL()
			NewsLists.append(newsList)
			print("  DONE")
		except:
			print('  FAILED')
			logging.exception(press[index]+' List problems : \n')
			pass
	return NewsLists

def getContent(state, NewsLists, record):
	print('\n Getting content from news list...')
	newsContentList = []
	for NewsList in NewsLists:
		index = pressAbbr.index(NewsList['press'])
		print("    Loading " + press[index] + " List...", end="", flush=True)
		try:
			if state == 'new':
				newsContentList.extend(spiders[index].getContent(NewsList['URLList'], record))
			elif state == 'check':
				newsContentList.extend(spidersCheck[index].getContent(NewsList['URLList'], record))
			print("  DONE")
		except:
			print('  FAILED')
			logging.exception(press[index]+' List problems : \n')
			pass
	return  newsContentList
