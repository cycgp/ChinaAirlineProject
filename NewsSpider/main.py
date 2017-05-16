from datetime import date, timedelta
from Spiders.SpiderFunctions import getNewsList, getContent
from Spiders.SpiderCheckFunctions import checkNewsList, checkContent
import pandas as pd
import schedule
import time

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
		record = []
		df = writePandas(record)
		df.to_csv(fileName+'.csv', sep=',', encoding='utf-8', index=False)

	print('\nEnd: ' + time.strftime('%Y/%m/%d %H:%M', time.localtime()) + '\n')

def checkPandas(record):
	newsList = checkNewsList()
	newsContentList = checkContent(newsList, record)
	df = pd.DataFrame(data=newsContentList, columns=['news ID', 'url', 'title','time','content'])
	return df


def checkFile():
	print('\nstart: ' + time.strftime('%Y/%m/%d %H:%M', time.localtime()) + '\n')
	yesterday = (date.today() - timedelta(1)).timetuple()
	fileName = 'NewsList_' + time.strftime('%Y%m%d', yesterday)
	df = pd.read_csv('' + fileName + '.csv')
	record = df['url'].values.tolist()
	df = df.append(checkPandas(record), ignore_index=True)
	df = df.drop_duplicates(subset=['url'], keep='last')
	df.to_csv(fileName+'.csv', sep=',', encoding='utf-8', index=False)

	print('\nEnd: ' + time.strftime('%Y/%m/%d %H:%M', time.localtime()) + '\n')

if __name__ == '__main__':
	schedule.every().day.at("07:30").do(writeFile)
	schedule.every().day.at("11:30").do(writeFile)
	schedule.every().day.at("17:00").do(writeFile)
	schedule.every().day.at("21:00").do(writeFile)
	schedule.every().day.at("00:30").do(checkFile)

	while True:
		schedule.run_pending()
