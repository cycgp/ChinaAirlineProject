from Spiders.NewsSpider import aplSpider, cldSpider, cnaSpider, cntSpider, ltnSpider, ntkSpider, stmSpider, tnlSpider, tpnSpider, udnSpider

def getNewsList():
	print("Getting News List...")
	print("    Loading Apple News List...", end="", flush=True)
	aplNewsList = aplSpider().getURL()
	print("  DONE")
	print("    Loading CNA News List...", end="", flush=True)
	cnaNewsList = cnaSpider().getURL()
	print("  DONE")
	print("    Loading China Times News List...", end="", flush=True)
	cntNewsList = cntSpider().getURL()
	print("  DONE")
	print("    Loading Liberty Times News List...", end="", flush=True)
	ltnNewsList = ltnSpider().getURL()
	print("  DONE")
	print("    Loading New Talks News List...", end="", flush=True)
	ntkNewsList = ntkSpider().getURL()
	print("  DONE")
	print("    Loading Storm News List...", end="", flush=True)
	stmNewsList = stmSpider().getURL()
	print("  DONE")
	print("    Loading The News Lens News List...", end="", flush=True)
	tnlNewsList = tnlSpider().getURL()
	print("  DONE")
	print("    Loading Taiwan People News News List...", end="", flush=True)
	tpnNewsList = tpnSpider().getURL()
	print("  DONE")
	print("    Loading UDN News List...", end="", flush=True)
	udnNewsList = udnSpider().getURL()
	print("  DONE")
	NewsList = [aplNewsList, cnaNewsList, cntNewsList, ltnNewsList, ntkNewsList, stmNewsList, tnlNewsList, tpnNewsList, udnNewsList]
	return NewsList

def getContent(NewsLists, record):
	print('\n Getting content from news list...')
	newsContentList = []
	for NewsList in NewsLists:
		if NewsList['press'] == 'apl':
			print("    Loading Apple News List...", end="", flush=True)
			newsContentList.extend(aplSpider.getContent(NewsList['URLList'], record))
			print("  DONE")
		elif NewsList['press'] == 'cna':
			print("    Loading CNA News List...", end="", flush=True)
			newsContentList.extend(cnaSpider.getContent(NewsList['URLList'], record))
			print("  DONE")
		elif NewsList['press'] == 'cnt':
			print("    Loading China Times News List...", end="", flush=True)
			newsContentList.extend(cntSpider.getContent(NewsList['URLList'], record))
			print("  DONE")
		elif NewsList['press'] == 'ltn':
			print("    Loading Liberty Times News List...", end="", flush=True)
			newsContentList.extend(ltnSpider.getContent(NewsList['URLList'], record))
			print("  DONE")
		elif NewsList['press'] == 'ntk':
			print("    Loading New Talks News List...", end="", flush=True)
			newsContentList.extend(ntkSpider.getContent(NewsList['URLList'], record))
			print("  DONE")
		elif NewsList['press'] == 'stm':
			print("    Loading Storm News List...", end="", flush=True)
			newsContentList.extend(stmSpider.getContent(NewsList['URLList'], record))
			print("  DONE")
		elif NewsList['press'] == 'tnl':
			print("    Loading The News Lens News List...", end="", flush=True)
			newsContentList.extend(tnlSpider.getContent(NewsList['URLList'], record))
			print("  DONE")
		elif NewsList['press'] == 'tpn':
			print("    Loading Taiwan People News News List...", end="", flush=True)
			newsContentList.extend(tpnSpider.getContent(NewsList['URLList'], record))
			print("  DONE")
		elif NewsList['press'] == 'udn':
			print("    Loading UDN List...", end="", flush=True)
			newsContentList.extend(udnSpider.getContent(NewsList['URLList'], record))
			print("  DONE")
	return  newsContentList
