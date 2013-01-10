#!/usr/bin/env python

#encoding=utf-8

import sys

import re
import os
import sys
from pyquery import PyQuery
from dateutil.parser import parse

reload(sys)
sys.setdefaultencoding(sys.stdout.encoding)

bug_status_statistics = {}

def statistics(dict, key):
	if (key in dict.keys()):
		dict[key] = dict[key] + 1
	else:
		dict[key] = 1
	return dict
	
def printStatistics(dict, name):
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

def processFile(filepath):
	#print filepath
	html = open(filepath, 'r').read()
	page = PyQuery(html)
	title = page('title').text()
	#remove invalid page
	if (cmp(title, 'Project hosting on Google Code') != 0):
		#print page('title').text()
		bug_status = page('span[@title]').eq(0).text()
		statistics(bug_status_statistics, bug_status)
		# if (cmp(bug_status, 'Fixed') == 0 or cmp(bug_status, 'Verified') == 0):
			# print bug_status
			# for item in page('a.label'):
				# print page(item).text()
			# items = page('tr.cursor_off')
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

list_dirs = os.walk("D:/tom/bugs-html")
for root, dirs, files in list_dirs:
	print root
	for f in files: 
		processFile(root + "/" + f)

printStatistics(bug_status_statistics, "bug_status_statistics")
#processFile('D:/tom/test/1.html')
