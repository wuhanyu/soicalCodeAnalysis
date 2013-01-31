#!/usr/bin/env python

#encoding=utf-8

import sys

import re
import os
import sys
import nltk
import time
from nltk.corpus import wordnet as wn
from pyquery import PyQuery
from dateutil.parser import parse
from dateutil.relativedelta import *


	
def getDifTime(starttime, endtime):
	result = None
	dif = (endtime - starttime)
	difdays = dif.days
	if (difdays > 2 and starttime.isoweekday() > endtime.isoweekday()): difdays = difdays - 2
	# if (dif.years > 0): return '>1Year'
	# elif (dif.months > 5): return '>HalfYear'
	# elif (dif.months > 2): return '>QuarterYear'
	# elif (dif.months > 0): return '>1Month'
	# elif (dif.days > 14): return '>2Week'
	if (difdays > 14): result = None
	elif (difdays > 6): result = '>1Week'
	elif (difdays > 2): result = '>2Day'
	else: result = '<=2Day'
	if (result != None):
		return result + '\ts' + str(starttime.isoweekday()) + '\te' + str(endtime.isoweekday())
	else:
		return None
	
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
				if (getDifTime(starttime, time) != None):
					return getDifTime(starttime, time), count, len(devSet.keys())
	return None
	
def getCommentNum(num):
	result = ''
	if (num > 25): result = 'Com>25'
	elif (num > 10): None#result = 'Com>10'
	elif (num > 4): None#result = 'Com>4'
	else: result = 'Com=' + str(num)
	if (result != None):
		return ' ' + result
	else: return ''
	
def getDevNum(num):
	result = ''
	if (num > 3): result = None#'Dev>3'
	else: result = 'Dev=' + str(num)
	if (result != None):
		return ' ' + result
	else: return ''
	
def getDesLen(num):
	if (num > 100): return 'DesW>100'
	elif (num > 50): return 'DesW>50'
	elif (num > 25): return 'DesW>25'
	elif (num > 12): return 'DesW>12'
	elif (num > 5): return 'DesW>5'
	else: return 'DesW<=5'
	
def getIR(text):
	tokens = nltk.word_tokenize(text)
	words = {}
	for token in tokens:
		tmp = wn.morphy(token.lower())
		if (tmp != None): words[tmp] = True
	result = ''
	# for word in words.keys():
		# result = result + ' ' + word
	# return result
	return ' ' + getDesLen(len(words.keys()))
	
def getReportDomain(reporter):
	index = reporter.find('@')
	if (index > 0):
		return ' ' + reporter[index:len(reporter)]
	else:
		return ''

def processFile(filepath):
	# print '----------------'
	# print filepath
	# print '----------------'
	html = open(filepath, 'r').read()
	page = PyQuery(html)
	title = page('title').text()
	#remove invalid page
	if (cmp(title, 'Project hosting on Google Code') != 0 and cmp(title, '500 Server Error') != 0):
		#print page('title').text()
		bug_status = page('span[@title]').eq(0).text()
		if (bug_status and (cmp(bug_status.lower(),'verified') == 0 or cmp(bug_status.lower(),'fixed') == 0)):
		# if (bug_status and (cmp(bug_status.lower(),'fixed') == 0)):
			tmp = getTime(page)
			if (tmp):
				reporter = page("div.author").eq(0).find('a').eq(0).text()
				result = tmp[0]
				# result = result + getReportDomain(reporter)
				# result = result + getCommentNum(tmp[1])
				# result = result + getDevNum(tmp[2])
				# for item in page('a.label'):
					# labeltext = page(item).text()
					# labeltext = labeltext.lower().replace(' ', '')
					# if (labeltext.find('pri-') >= 0):
						# if (cmp(labeltext, 'pri-1') != 0 and cmp(labeltext, 'pri-2') != 0):
							# result = result + ' ' + labeltext
					# elif (labeltext.find('feature-') >= 0):
						# result = result + ' ' + 'feature'
					# elif (labeltext.find('area-') >= 0):
						# result = result + ' ' + 'area'
					# elif (labeltext.find('os-') >= 0):
						# result = result + ' ' + 'os'
					# elif (labeltext.find('feature-') >= 0):
						# result = result + ' ' + labeltext
					# elif (labeltext.find('area-') >= 0):
						# result = result + ' ' + labeltext
					# elif (labeltext.find('os-') >= 0):
						# result = result + ' ' + labeltext
					# elif (labeltext.find('mstone-') >= 0):
						# result = result + ' ' + labeltext
						
				# irstr = getIR(page('pre').eq(0).text())
				# result = result + irstr
				print result


# list_dirs = os.walk("./test")
list_dirs = os.walk("D:/tom/bugs-html")
for root, dirs, files in list_dirs:
	for f in files: 
		processFile(root + "/" + f)

#processFile('D:/tom/test/1.html')
