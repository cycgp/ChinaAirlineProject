# ChinaAirlineProject
This is a project in China Airline to do text mining and sentiment analysis on [Trip Advisor](https://www.tripadvisor.com.tw/Airline_Review-d8729049-Reviews-Cheap-Flights-China-Airlines) and [Facebook fans page](https://www.facebook.com/chinaairlines.travelchannel/?fref=ts) for further business and advertising decision.(Based on Python3)
##Trip Advisor
The steps of do text mining and sentiment analysis on Trip Advisor.

1. Web Spider
2. Simplified Chinese to Traditional Chinese
3. Ｗord segmentation
4. Training Word to Vector

###Web Spider

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- qt -- (must lover then 5.5 `brew install qt@5.5`)
- [dryscrape](http://dryscrape.readthedocs.io/en/latest/installation.html) -- `pip install dryscrape`
- json
- time

###Simplified Chinese to Traditional Chinese
[OpenCC](https://github.com/BYVoid/OpenCC) -- simple tool to translate simplified Chinese to traditional Chinese or traditional chinese to simplified chinese.
###Ｗord segmentation
[jieba](https://github.com/fxsjy/jieba)

- load traditional chinese dictionary -- `jieba.set_dictionary('jieba_dict/dict.txt.big')`
- load custom dictionary -- `jieba.load_userdict("jieba_dict/userdict.txt")`

###Training Word to Vector
gensim
##Facebook
###Get Facebook likes
