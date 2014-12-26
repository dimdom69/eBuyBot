from ebaysdk.exception import *
from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
import random

class ebay:
	def __init__(self):
		self.finding = Finding()
		self.categories = self.getCategories()

	def getItems(self, minPrice = "0.0", maxPrice = "2.0", listingType = "FixedPrice",
		freeShippingOnly = "true", keywords = "(or,and,of,is,i,if,at,where,when,you,why,how,new,used)",
		sortOrder = "StartTimeNewest", categoryID = "-1", pageNumber = "1"):
		request = {
			"itemFilter": [
				{"name": "MinPrice", "value": minPrice},
				{"name": "MaxPrice", "value": maxPrice},
				{"name": "ListingType", "value": listingType},
				{"name": "FreeShippingOnly", "value": freeShippingOnly}
			],
			"keywords": keywords,
			"sortOrder": sortOrder,
			#"descriptionSearch": "true", #Doesn't work for some reason?
			"CategoryID": categoryID,
			"pageNumber": pageNumber
		}
		try:
			response = self.finding.execute("findItemsAdvanced", request).dict()
			return response
		except ConnectionError as e:
			print(e)
			print(e.response.dict())
			return {}

	def buyItem(self):
		pass

	def getCategories(self):
		catList = Shopping().execute("GetCategoryInfo", {"CategoryID": "-1", "IncludeSelector": "ChildCategories"}).dict()["CategoryArray"]["Category"]
		for cat in catList: #meow
			if cat["CategoryID"] != "-1": #perhaps not, would give randomly selecting from all categories
				catList.remove(cat)
		return catList

	def getRandomCategory(self):
		return self.categories[random.randint(0, len(self.categories) - 1)]

	def randomItem(self):
		try:
			randomCategory = self.getRandomCategory()
			response = self.getItems(categoryID = randomCategory)

			count = int(response["searchResult"]["_count"])
			totalCount = int(response["paginationOutput"]["totalEntries"])

			if totalCount >= 10000: #eBay has a dumb 100 page, 100 entries/page limit, so
				totalCount = 999 #a total limit of 10000

			if count < 1:#TODO: error handling
				print("No results :(")
				return

			elif totalCount <= 100:
				print(str(count) + " results from category: " + randomCategory["CategoryName"])
				results = response["searchResult"]["item"]
				print(results[random.randint(0, count - 1)]["viewItemURL"])

			else:
				pageNumber = int(totalCount/100) + 1
				response = self.getItems(categoryID = randomCategory, pageNumber = str(pageNumber))

				results = response["searchResult"]["item"]
				count = int(response["searchResult"]["_count"])

				print(str(totalCount) + " results from category: " + randomCategory["CategoryName"])
				results = response["searchResult"]["item"]
				print(results[random.randint(0, count - 1)]["viewItemURL"])

		except ConnectionError as e:
			print(e)
			print(e.response.dict())
