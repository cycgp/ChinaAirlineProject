from datetime import date, timedelta
from Spiders.SpiderFunctions import getNewsList, getContent
import pandas as pd
import schedule
import time

def writePandas(record):
	newsList = getNewsList('new')
	newsContentList = getContent('new', newsList, record)
	df = pd.DataFrame(data=newsContentList, columns=['news ID', 'url', 'title','time','content'])
	return df

def writeFile():
	print('\nstart: ' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()) + '\n')
	fileName = 'NewsList_' + time.strftime('%Y%m%d', time.localtime())
	try:
		df = pd.read_csv('data_csv/' + fileName + '.csv')
		record = df['url'].values.tolist()
		df = df.append(writePandas(record), ignore_index=True)
		df = df.drop_duplicates(subset=['url'], keep='last')
		df.to_csv('data_csv/'+fileName+'.csv', sep=',', encoding='utf-8', index=False)
	except:
		record = []
		df = writePandas(record)
		df.to_csv('data_csv/'+fileName+'.csv', sep=',', encoding='utf-8', index=False)

	print('\n'+fileName+'.csv updated')
	print('End: ' + time.strftime('%Y/%m/%d %H:%M', time.localtime()) + '\n')

def checkPandas(record):
	newsList = getNewsList('check')
	newsContentList = getContent('check', newsList, record)
	df = pd.DataFrame(data=newsContentList, columns=['news ID', 'url', 'title','time','content'])
	return df


def checkFile():
	print('start: ' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
	yesterday = (date.today() - timedelta(1)).timetuple()
	fileName = 'NewsList_' + time.strftime('%Y%m%d', yesterday)
	df = pd.read_csv('data_csv/' + fileName + '.csv')
	record = df['url'].values.tolist()
	df = df.append(checkPandas(record), ignore_index=True)
	df = df.drop_duplicates(subset=['url'], keep='last')
	df.to_csv('data_csv/' + fileName+'.csv', sep=',', encoding='utf-8', index=False)
	print('\n'+fileName+'.csv updated')
	print('End: ' + time.strftime('%Y/%m/%d %H:%M', time.localtime()))

if __name__ == '__main__':
	writeFile()
	schedule.every().day.at("06:30").do(writeFile)
	schedule.every().day.at("10:00").do(writeFile)
	schedule.every().day.at("13:30").do(writeFile)
	schedule.every().day.at("15:30").do(writeFile)
	schedule.every().day.at("18:00").do(writeFile)
	schedule.every().day.at("21:00").do(writeFile)
	schedule.every().day.at("22:00").do(writeFile)
	schedule.every().day.at("00:00").do(checkFile)
	print('Next Run: ' + time.strftime('%Y/%m/%d %H:%M:%S', schedule.next_run().timetuple()) + '\n')
	while True:
		schedule.run_pending()
