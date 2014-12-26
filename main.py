#! /usr/bin/env python

import random
from pprint import pprint
import django
import json
import amazonproduct
from ebay import ebay

f = open("config.json", "r")
config = json.loads(f.read())
f.close()

def checkEbay():
	e = ebay()
	e.randomItem()

if __name__ == '__main__':
	checkEbay()
