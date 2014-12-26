def amazon():
	amazon = amazonproduct.API(locale="us")
	items = amazon.item_search("Books", Publisher="O'Reilly")

	for item in items:
		pprint(item)