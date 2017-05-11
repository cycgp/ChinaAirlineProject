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
	print('\n' + time.strftime('%Y/%m/%d %H:%M', time.localtime()) + '\n')
	fileName = 'NewsList_' + time.strftime('%Y%m%d', time.localtime())
	try:
		df = pd.read_csv('' + fileName + '.csv')
		df = df.append(writePandas(), ignore_index=True)
		df = df.drop_duplicates(subset=['url'], keep='last')
		df.to_csv(fileName+'.csv', sep=',', encoding='utf-8', index=False)
	except:
		df = writePandas()
		df.to_csv(fileName+'.csv', sep=',', encoding='utf-8', index=False)

if __name__ == '__main__':
	writeFile()
	scheduler = BlockingScheduler()
	scheduler.add_job(writeFile, 'interval', hours=1)
	scheduler.start()
