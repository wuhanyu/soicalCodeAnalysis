#!/usr/bin/env python

#encoding=utf-8

import sys

import re
import os
import sys
from pyquery import PyQuery
from dateutil.parser import parse
from dateutil.relativedelta import *

featureSet = {}
featureSum = {}
featureCount = {}
cateSet = {}
BASE = 4
INDEX = 0
CUTOFF = 1
WINDOW = 10

def getDifTime(starttime, endtime):
	result = None
	dif = (endtime - starttime)
	difdays = dif.days
	return str(difdays), difdays
	if (difdays > 2 and starttime.isoweekday() > endtime.isoweekday()): difdays = difdays - 2
	if (difdays > 14): result = None
	elif (difdays > 6): result = '3'
	elif (difdays > 2): result = '2'
	else: result = '1'
	# elif (difdays > 6): result = '[1Week..2Week)'
	# elif (difdays > 2): result = '(2days..6days]'
	# else: result = '<2days'
	return result, difdays
	
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
				timestr, difdays = getDifTime(starttime, time)
				if (timestr != None):
					return timestr, count, len(devSet.keys()), difdays
	return None
	
def getFeatureAvgTime(feature, c_difdays):
	global INDEX, BASE, featureSet, featureSum, featureCount
	result = -1
	if (feature.find('-') >= 0):
		cate = feature[0:feature.find('-')]
	else:
		cate = feature
	# tmp = feature
	# feature = cate
	if (featureSet.has_key(feature)):
		result = featureSum[feature] / featureCount[feature]
		featureSum[feature] = featureSum[feature] + c_difdays
		featureCount[feature] = featureCount[feature] + 1
		
	else:
		if (not featureSet.has_key(cate)):
			featureSet[cate] = BASE + INDEX
			cateSet[BASE + INDEX] = cate
			INDEX = INDEX + 1
		featureSet[feature] = featureSet[cate]
		# featureSet[feature] = BASE + INDEX	
		# INDEX = INDEX + 1	
		featureSum[feature] = c_difdays
		featureCount[feature] = 1

			
	# featureSet[tmp] = featureSet[cate]
	if (featureCount[feature] >= CUTOFF):
		return result
	else:
		return -1
		
def getDevNum(page):
	items = page('tr.cursor_off')

def processFile(filepath):
	global featureSet
	html = open(filepath, 'r').read()
	page = PyQuery(html)
	title = page('title').text()
	#remove invalid page
	resultset = {}
	if (cmp(title, 'Project hosting on Google Code') != 0 and cmp(title, '500 Server Error') != 0):
		#print page('title').text()
		bug_status = page('span[@title]').eq(0).text()
		if (bug_status and (cmp(bug_status.lower(),'verified') == 0 or cmp(bug_status.lower(),'fixed') == 0)):
		# if (bug_status and (cmp(bug_status.lower(),'fixed') == 0)):
			tmp = getTime(page)
			if (tmp):
				reporter = page("div.author").eq(0).find('a').eq(0).text()
				reporter = 'reporter-' + reporter
				result = tmp[0]
				resultset[1] = tmp[1]
				resultset[2] = tmp[2]
				difdays = tmp[3]
				resultset[featureSet[reporter]] = getFeatureAvgTime(reporter, difdays)
				for item in page('a.label'):
					labeltext = page(item).text()
	
					labeltext = labeltext.lower().replace(' ', '')
					if (labeltext.find('pri-')>= 0):
						resultset[3] = labeltext[4:len(labeltext)]
						resultset[featureSet[labeltext]] = getFeatureAvgTime(labeltext, difdays)
					elif (labeltext.find('feature-') >= 0):
						resultset[featureSet[labeltext]] = getFeatureAvgTime(labeltext, difdays)
					elif (labeltext.find('area-') >= 0):
						resultset[featureSet[labeltext]] = getFeatureAvgTime(labeltext, difdays)
					elif (labeltext.find('os-') >= 0):
						resultset[featureSet[labeltext]] = getFeatureAvgTime(labeltext, difdays)
					elif (labeltext.find('mstone-') >= 0):
						resultset[featureSet[labeltext]] = getFeatureAvgTime(labeltext, difdays)
				for i in range(BASE, BASE + INDEX):
					if (not resultset.has_key(i)):
						resultset[i] = getFeatureAvgTime(cateSet[i] + '-NONE', difdays)			
				for i in range(0, BASE + INDEX):
					if (resultset.has_key(i) and resultset[i] >= 0):
						result = result + ' ' + str(i) + ':' + str(resultset[i])
				print cateSet
				print result


#list_dirs = os.walk("./test)
if (len(sys.argv) < 2):
	dirpath = 'D:/data/all'
else:
	dirpath = 'D:/data/' + sys.argv[1]
list_dirs = os.walk(dirpath)
for root, dirs, files in list_dirs:
	for i in range(0, 50000):
		filename = str(i) + '.html'
		if (filename in files):
			processFile(root + "/" + filename)
	# for f in files: 
		# processFile(root + "/" + f)

#processFile('D:/tom/test/1.html')
