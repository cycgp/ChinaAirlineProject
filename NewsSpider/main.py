from apscheduler.schedulers.blocking import BlockingScheduler
from Spiders.SpiderFunction import getNewsList, getContent
import pandas as pd
import time
from datetime import date, timedelta

yesterday = (date.today() - timedelta(1)).timetuple()

def writePandas(record):
	newsList = getNewsList()
	newsContentList = getContent(newsList, record)
	df = pd.DataFrame(data=newsContentList, columns=['news ID', 'url', 'title','time','content'])
	return df


def writeFile():
	print('\nstart: ' + time.strftime('%Y/%m/%d %H:%M', time.localtime()) + '\n')
	fileName = 'NewsList_' + time.strftime('%Y%m%d', time.localtime())
	try:
		df = pd.read_csv('' + fileName + '.csv')
		record = df['url'].values.tolist()
		df = df.append(writePandas(record), ignore_index=True)
		df = df.drop_duplicates(subset=['url'], keep='last')
		df.to_csv(fileName+'.csv', sep=',', encoding='utf-8', index=False)
	except:
		df = writePandas(record)
		df.to_csv(fileName+'.csv', sep=',', encoding='utf-8', index=False)

	print('\nEnd: ' + time.strftime('%Y/%m/%d %H:%M', time.localtime()) + '\n')

def checkPandas(record):
	newsList = getNewsList()
	newsContentList = getContent(newsList, record)
	df = pd.DataFrame(data=newsContentList, columns=['news ID', 'url', 'title','time','content'])
	return df


def checkFile():
	print('\nstart: ' + time.strftime('%Y/%m/%d %H:%M', time.localtime()) + '\n')
	fileName = 'NewsList_' + time.strftime('%Y%m%d', yesterday)
	df = pd.read_csv('' + fileName + '.csv')
	record = df['url'].values.tolist()
	df = df.append(writePandas(record), ignore_index=True)
	df = df.drop_duplicates(subset=['url'], keep='last')
	df.to_csv(fileName+'.csv', sep=',', encoding='utf-8', index=False)

	print('\nEnd: ' + time.strftime('%Y/%m/%d %H:%M', time.localtime()) + '\n')

if __name__ == '__main__':
	writeFile()
	scheduler = BlockingScheduler()
	scheduler.add_job(writeFile, 'interval', hours=1)
	scheduler.start()
