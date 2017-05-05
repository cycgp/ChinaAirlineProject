from Spiders.aplSpider import aplSpider
from Spiders.cnaSpider import cnaSpider
from Spiders.ltnSpider import ltnSpider
from Spiders.tnlSpider import tnlSpider
from Spiders.cntSpider import cntSpider
from Spiders.stmSpider import stmSpider
from Spiders.cldSpider import cldSpider
from Spiders.ntkSpider import ntkSpider
from Spiders.tpnSpider import tpnSpider
from Spiders.udnSpider import udnSpider
import pandas as pd

a = udnSpider()
a.getURL()
newsList = a.getContent()
df = pd.DataFrame(data=newsList, columns=['News ID', 'Title','Time','Content'])
df.to_csv('newsList.csv', sep=',', encoding='utf-8', index=False)
