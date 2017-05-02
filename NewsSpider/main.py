from Spiders.AppleSpider import AppleSpider
from Spiders.CNASpider import CNASpider
from Spiders.LTNSpider import LTNSpider
from Spiders.TNLSpider import TNLSpider
from Spiders.CTSpider import CTSpider
from Spiders.StormSpider import StormSpider
from Spiders.CLSpider import CLSpider
from Spiders.NTSpider import NTSpider
from Spiders.TPNSpider import TPNSpider
import pandas as pd

a = TPNSpider()
a.getRTNURL()
newsList = a.getContent()
df = pd.DataFrame(data=newsList, columns=['Title','Time','Content'])
df.to_csv('newsList.csv', sep=',', encoding='utf-8', index=False)
