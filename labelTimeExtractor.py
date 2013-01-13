#!/usr/bin/env python

#encoding=utf-8

import sys

import re
import os
import sys
from pyquery import PyQuery
from dateutil.parser import parse
from dateutil.relativedelta import *
	
def getDifTime(starttime, endtime):
	dif = relativedelta(endtime, starttime)
	if (dif.years > 0): return '>1Year'
	elif (dif.months > 5): return '>HalfYear'
	elif (dif.months > 2): return '>QuarterYear'
	elif (dif.months > 0): return '>1Month'
	elif (dif.days > 14): return '>2Week'
	elif (dif.days > 6): return '>1Week'
	elif (dif.days > 3): return '>3Day'
	elif (dif.days > 0): return '>1Day'
	else: return '1Day'
	
def getTime(page):
	items = page('tr.cursor_off')
	authordiv = page("div.author")
	starttime = parse(page(authordiv).find('span.date').attr('title'))
	for item in items:
		status = page(item).find('div.box-inner')
		if (len(status) > 0):
			tmp = status.text().lower().split('status: ')
			if (len(tmp) > 1 and (cmp(tmp[1], 'fixed') == 0 or cmp(tmp[1], 'verified') == 0)):
				timestr = page(item).find('span.date').attr('title')
				time = parse(timestr)
				return getDifTime(starttime, time)
	return None

def processFile(filepath):
	#print filepath
	html = open(filepath, 'r').read()
	page = PyQuery(html)
	title = page('title').text()
	#remove invalid page
	if (cmp(title, 'Project hosting on Google Code') != 0 and cmp(title, '500 Server Error') != 0):
		#print page('title').text()
		bug_status = page('span[@title]').eq(0).text()
		if (bug_status and (cmp(bug_status.lower(),'verified') == 0 or cmp(bug_status.lower(),'fixed') == 0)):
			result = getTime(page)
			if (result):
				for item in page('a.label'):
					labeltext = page(item).text()
					labeltext = labeltext.lower().replace(' ', '')
					result = result + ' ' + labeltext
				print result

#list_dirs = os.walk("./test")
list_dirs = os.walk("D:/tom/bugs-html")
for root, dirs, files in list_dirs:
	for f in files: 
		processFile(root + "/" + f)

#processFile('D:/tom/test/1.html')
