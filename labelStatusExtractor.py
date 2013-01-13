#!/usr/bin/env python

#encoding=utf-8

import sys

import re
import os
import sys
from pyquery import PyQuery
from dateutil.parser import parse

statisticsSet = {}

def statistics(dict, key):
	if (key in dict.keys()):
		dict[key] = dict[key] + 1
	else:
		dict[key] = 1
	return dict
	
def statisticsByName(name, key):
	if (name not in statisticsSet.keys()):
		statisticsSet[name] = {}	
	statistics(statisticsSet[name], key)
	
def printStatistics(dict, name):
	print '----%s----' % name
	file_object = open(name + '.txt', 'w')
	sum = 0
	for item in dict:
		sum = sum + dict[item]
		output = "%s	%d" % (item, dict[item])
		print output
		file_object.write(output + '\n')
	output = "Sum	%d" % sum
	print output
	file_object.write(output + '\n')
	file_object.close( )
	print ''
	print ''

def processFile(filepath):
	#print filepath
	html = open(filepath, 'r').read()
	page = PyQuery(html)
	title = page('title').text()
	#remove invalid page
	if (cmp(title, 'Project hosting on Google Code') != 0 and cmp(title, '500 Server Error') != 0):
		#print page('title').text()
		bug_status = page('span[@title]').eq(0).text()
		if (bug_status):
			bug_status = bug_status.lower()
			# statics for label
			bug_status = bug_status.replace(' ', '')
			result = bug_status
			for item in page('a.label'):
				labeltext = page(item).text()
				labeltext = labeltext.lower()
				labeltext = labeltext.replace(' ', '')
				result = result + ' ' + labeltext
			print result
			#items = page('tr.cursor_off')
				# print len(items)

#list_dirs = os.walk("./test")
list_dirs = os.walk("D:/tom/bugs-html")
for root, dirs, files in list_dirs:
	for f in files: 
		processFile(root + "/" + f)

for key in statisticsSet:
	printStatistics(statisticsSet[key], key)
#processFile('D:/tom/test/1.html')
