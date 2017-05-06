from Spiders.SpiderFunction import getNewsList, getContent
import pandas as pd

if __name__ == '__main__':
	newsList = getNewsList()
	newsContentList = getContent(newsList)
	df = pd.DataFrame(data=newsContentList, columns=['news ID', 'url', 'title','time','content'])
	df.to_csv('NewsList.csv', sep=',', encoding='utf-8', index=False)
