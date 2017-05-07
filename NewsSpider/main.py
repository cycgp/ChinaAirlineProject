from apscheduler.schedulers.blocking import BlockingScheduler
from Spiders.SpiderFunction import getNewsList, getContent
import pandas as pd
import time

def writePandas():
	newsList = getNewsList()
	newsContentList = getContent(newsList)
	df = pd.DataFrame(data=newsContentList, columns=['news ID', 'url', 'title','time','content'])
	return df


def writeFile():
	fileName = 'NewsList_' + time.strftime('%Y%m%d', time.localtime())
	try:
		df = pd.read_csv('' + fileName + '.csv')
		df.append(writePandas(), ignore_index=True)
		df = df.drop_duplicates(keep='last')
		df.to_csv(fileName+'.csv', sep=',', encoding='utf-8', index=False)
	except:
		df = writePandas()
		df.to_csv(fileName+'.csv', sep=',', encoding='utf-8', index=False)

if __name__ == '__main__':
	scheduler = BlockingScheduler()
	scheduler.add_job(writeFile, 'interval', hours=4)
	scheduler.start()
