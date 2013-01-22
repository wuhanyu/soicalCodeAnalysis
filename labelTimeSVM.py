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
	dif = (endtime - starttime)
	if (dif.days > 14): return None
	elif (dif.days > 6): return '-1'
	elif (dif.days > 2): return '0'
	else: return '1'
	
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
				
				#to filter the time
				timestr = getDifTime(starttime, time)
				if (timestr != None):
					return timestr, count, len(devSet.keys())
	return None
	
def getDevNum(page):
	items = page('tr.cursor_off')

def processFile(filepath):
	#print filepath
	html = open(filepath, 'r').read()
	page = PyQuery(html)
	title = page('title').text()
	#remove invalid page
	if (cmp(title, 'Project hosting on Google Code') != 0 and cmp(title, '500 Server Error') != 0):
		#print page('title').text()
		bug_status = page('span[@title]').eq(0).text()
		# if (bug_status and (cmp(bug_status.lower(),'verified') == 0 or cmp(bug_status.lower(),'fixed') == 0)):
		if (bug_status and (cmp(bug_status.lower(),'fixed') == 0)):
			tmp = getTime(page)
			if (tmp):
				reporter = page("div.author").eq(0).find('a').eq(0).text()
				result = tmp[0]
				result = result + ' ' + '1:' + str(tmp[1])
				result = result + ' ' + '2:' + str(tmp[2])
				featureFlag = False
				areaFlag = False
				osFlag = False
				for item in page('a.label'):
					labeltext = page(item).text()
					labeltext = labeltext.lower().replace(' ', '')
					if (labeltext.find('pri-')>= 0):
						result = result + ' ' + '3:' +labeltext[4:len(labeltext)]
					elif (labeltext.find('feature-') >= 0):
						featureFlag = True
					elif (labeltext.find('area-') >= 0):
						areaFlag = True
					elif (labeltext.find('os-') >= 0):
						osFlag = True
				if (featureFlag):
					result = result +  ' '  + '4:' + '1'
				if (areaFlag):
					result = result +  ' '  + '5:' + '1'
				if (osFlag):
					result = result +  ' '  + '6:' + '1'
				print result


#list_dirs = os.walk("./test")
list_dirs = os.walk("D:/tom/bugs-html")
for root, dirs, files in list_dirs:
	for f in files: 
		processFile(root + "/" + f)

#processFile('D:/tom/test/1.html')
