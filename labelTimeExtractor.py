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
	count = 0
	devSet = {}
	for item in items:
		count = count + 1
		#dev-count
		authorspan = page("span.author")
		author = authorspan.eq(count).find('a').eq(1).text()
		
		if (author): devSet[author] = True
		#fix-time
		status = page(item).find('div.box-inner')
		if (len(status) > 0):
			tmp = status.text().lower().split('status: ')
			if (len(tmp) > 1 and (cmp(tmp[1], 'fixed') == 0 or cmp(tmp[1], 'verified') == 0)):
				timestr = page(item).find('span.date').attr('title')
				time = parse(timestr)
				return getDifTime(starttime, time), count, len(devSet.keys())
	return None
	
def getDevNum(page):
	items = page('tr.cursor_off')
	
def getCommentNum(num):
	if (num > 100): return 'Com>100'
	elif (num > 50): return 'Com>50'
	elif (num > 25): return 'Com>25'
	elif (num > 10): return 'Com>10'
	elif (num > 5): return 'Com>5'
	else: return 'Com=' + str(num)
	
def getDevNum(num):
	if (num > 10): return 'Dev>10'
	elif (num > 5): return 'Dev>5'
	else: return 'Dev=' + str(num)

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
			tmp = getTime(page)
			if (tmp):
				reporter = page("div.author").eq(0).find('a').eq(0).text()
				result = tmp[0]
				result = result + ' ' + reporter
				result = result + ' ' + getCommentNum(tmp[1])
				result = result + ' ' + getDevNum(tmp[2])
				for item in page('a.label'):
					labeltext = page(item).text()
					labeltext = labeltext.lower().replace(' ', '')
					if (labeltext.find('pri-') >= 0):
						result = result + ' ' + labeltext
					elif (labeltext.find('feature-') >= 0):
						result = result + ' ' + labeltext
					elif (labeltext.find('area-') >= 0):
						result = result + ' ' + labeltext
					elif (labeltext.find('os-') >= 0):
						result = result + ' ' + labeltext
					elif (labeltext.find('mstone-') >= 0):
						result = result + ' ' + labeltext
					elif (labeltext.find('size-') >= 0):
						result = result + ' ' + labeltext
				print result


# list_dirs = os.walk("./test")
list_dirs = os.walk("D:/tom/bugs-html")
for root, dirs, files in list_dirs:
	for f in files: 
		processFile(root + "/" + f)

#processFile('D:/tom/test/1.html')
