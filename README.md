# Sentiment aAnalysis Project (China Airline)
This is a project in China Airline to do text mining and sentiment analysis on [Trip Advisor](https://www.tripadvisor.com.tw/Airline_Review-d8729049-Reviews-Cheap-Flights-China-Airlines) and [Facebook fans page](https://www.facebook.com/chinaairlines.travelchannel/?fref=ts) for further business and advertising decision(Based on Python3).

## News Spiders

#### News List

- [自由時報](http://news.ltn.com.tw/list/BreakingNews)(Liberty Time) 
- [蘋果日報](http://www.appledaily.com.tw/realtimenews/section/new/)(Apple Daily)
- [聯合新聞網](https://udn.com/news/breaknews/1)(UDN)
- [中時電子報](http://www.chinatimes.com/realtimenews)(China Times)
- [中央通訊社](http://www.cna.com.tw/list/aall-1.aspx)(CNA)
- [關鍵評論網](https://www.thenewslens.com/news)(The News Lens)
- [東森新聞雲](http://www.ettoday.net/news/news-list.htm)(ETtoday)
- [民報](http://www.peoplenews.tw/list/%E7%B8%BD%E8%A6%BD)(Taiwan People News) *
- [風傳媒](http://www.storm.mg/articles)(Storm)
- [新頭殼](https://newtalk.tw/news/summary/today)(New Talk) *
- [苦勞網](http://www.coolloud.org.tw/story)(Cool Loud) *

## Trip Advisor
The steps of do text mining and sentiment analysis on Trip Advisor.

1. Web Spider
2. Simplified Chinese to Traditional Chinese
3. Ｗord segmentation
4. Training Word to Vector

#### Web Spider

- BeautifulSoup
- qt -- (must lover then 5.5 `brew install qt@5.5`)
- [dryscrape](http://dryscrape.readthedocs.io/en/latest/installation.html) -- `pip install dryscrape`
- json
- time

#### Simplified Chinese to Traditional Chinese
[OpenCC](https://github.com/BYVoid/OpenCC) -- simple tool to translate simplified Chinese to traditional Chinese or traditional chinese to simplified chinese.

#### Ｗord segmentation
[jieba](https://github.com/fxsjy/jieba)

- load traditional chinese dictionary `jieba.set_dictionary('jieba_dict/dict.txt.big')`
- load custom dictionary `jieba.load_userdict("jieba_dict/userdict.txt")`

#### Training Word to Vector
[gensim](https://radimrehurek.com/gensim/)
## Facebook
#### Get Facebook likes
