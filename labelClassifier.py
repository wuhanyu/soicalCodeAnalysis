#!/usr/bin/env python

#encoding=utf-8

import sys

import re
import os
import sys
import shutil  
from pyquery import PyQuery
from dateutil.parser import parse
from dateutil.relativedelta import *

gfilepath = ''
	
def getDifTime(starttime, endtime):
	dif = relativedelta(endtime, starttime)
	if (dif.years > 0): return None
	elif (dif.months > 5): return None
	elif (dif.months > 2): return None
	elif (dif.months > 0): return None
	elif (dif.days > 14): return None
	elif (dif.days > 6): return 'gt1Week'
	elif (dif.days > 2): return 'gt2Day'
	else: return 'lte2Day'
	
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
				return timestr
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

def processFile(file, root):
	#print filepath
	html = open(root + '/' + file, 'r').read()
	page = PyQuery(html)
	title = page('title').text()
	#remove invalid page
	if (cmp(title, 'Project hosting on Google Code') != 0 and cmp(title, '500 Server Error') != 0):
		#print page('title').text()
		bug_status = page('span[@title]').eq(0).text()
		# if (bug_status and (cmp(bug_status.lower(),'verified') == 0 or cmp(bug_status.lower(),'fixed') == 0)):
		if (bug_status and (cmp(bug_status.lower(),'fixed') == 0)):
			tmp = getTime(page)
			print tmp
			if (tmp != None):
				if (not os.path.exists(root + '/' + tmp + '/')):
					os.makedirs(root+ '/' + tmp + '/')
				shutil.copyfile(root + '/' + file, root + '/' + tmp + '/' + file)  


# list_dirs = os.walk("./test")
list_dirs = os.walk("D:/tom/bugs-html")
for root, dirs, files in list_dirs:
	for f in files: 
		processFile(f, root)

#processFile('D:/tom/test/1.html')
