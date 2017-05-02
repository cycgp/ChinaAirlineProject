from Spiders.AppleSpider import AppleSpider
from Spiders.CNASpider import CNASpider
from Spiders.LTNSpider import LTNSpider
from Spiders.TNLSpider import TNLSpider
from Spiders.CTSpider import CTSpider
from Spiders.StormSpider import StormSpider
from Spiders.CLSpider import CLSpider
from Spiders.NTSpider import NTSpider
from Spiders.TPNSpider import TPNSpider
from Spiders.UDNSpider import UDNSpider
import pandas as pd

a = StormSpider()
a.getURL()
a.getContent()