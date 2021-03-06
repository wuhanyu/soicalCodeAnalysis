#!/usr/bin/env python

#encoding=utf-8

import sys

import re
import os
import sys
from pyquery import PyQuery
from dateutil.parser import parse

statisticsSet = {}
PATH = './result/'

def statistics(dict, key):
	#python's dict doesnt differ the case
	if (key): key = key.lower()
	else: return
	if (key in dict.keys()):
		dict[key] = dict[key] + 1
	else:
		dict[key] = 1
	
def statisticsByName(name, key):
	name = name.lower()
	if (name not in statisticsSet.keys()):
		statisticsSet[name] = {}	
	statistics(statisticsSet[name], key)
	
def printStatistics(dict, name):
	print '----%s----' % name
	file_object = open(PATH + name + '.txt', 'w')
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
	if (cmp(title, 'Project hosting on Google Code') != 0):
		#print page('title').text()
		bug_status = page('span[@title]').eq(0).text()
		statisticsByName('bug_status_statistics', bug_status)
		# statics for label
		for item in page('a.label'):
			tmp = page(item).text().split('- ')
			if (len(tmp) == 2): statisticsByName(tmp[0], tmp[1])
		items = page('tr.cursor_off')
			# print len(items)
			
			# authordiv = page("div.author")
			# starttime = parse(page(authordiv).find('span.date').attr('title'))
			# for item in items:
				# status = page(item).find('div.box-inner')
				# if (len(status) > 0):
					# print status.text()
					# timestr = page(item).find('span.date').attr('title')
					# time = parse(timestr)
					# print time - starttime

#list_dirs = os.walk("./test")
list_dirs = os.walk("D:/tom/bugs-html")
for root, dirs, files in list_dirs:
	print root
	for f in files: 
		processFile(root + "/" + f)

for key in statisticsSet:
	printStatistics(statisticsSet[key], key)
#processFile('D:/tom/test/1.html')
