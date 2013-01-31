#!/usr/bin/env python

#encoding=utf-8

import fileinput
from math import log
dictkey ={}
dict = {}
dict_count = {}

def I(args):
	total = sum(args) + 0.0
	result = 0.0
	for i in args:
		if i == 0:
			result += 0
		else:
			result += i / total * log( i / total, 2)
	return -result

def E(num, args):
	if len(args) % num != 0:
		print "Error len(args)"
	result = 0.0
	total = sum(args)
	for x in xrange(len(args) / num):
		k = x * num
		total_up = 0.0 + sum(args[k:k + num])
		result += total_up / total * I(args[k:k + num])
	return result

def Gain(i, e):
	return i - e

i = I
e = E
g = Gain

	
for line in fileinput.input("all_train.txt"):
	line = line[0:len(line) - 1]
	tmp = line.split(" ")
	if (len(tmp) < 2):
		tmp = line.split("\t")
	result = tmp[0]
	rest = tmp[1:len(tmp)]
	if (not dict.has_key(result)):
		dict[result] = {}
		dict_count[result] = 0
	dict_count[result] = dict_count[result] + 1
	subdict = dict[result]
	for token in rest:
		dictkey[token] = True
		if (subdict.has_key(token)):
			subdict[token] = subdict[token] + 1
		else:
			subdict[token] = 1
SUM = 0
for key in dict_count:
	SUM = SUM + dict_count[key]
value = []
for key in dict_count:
	value.append(dict_count[key])
entropyS = i(value)
print entropyS
	
print dict_count
for word in dictkey:
	result = word
	word_sum = 0
	value = []
	for label in dict_count:
		if (dict[label].has_key(word)):
			value.append(dict[label][word])
			value.append(dict_count[label] - dict[label][word])
			result = result + '\t' + str(dict[label][word])
			word_sum = word_sum + dict[label][word]
		else:
			value.append(0)
			value.append(dict_count[label])
			result = result + '\t' + '0'
	entropyE = e(2, value)
	gain = Gain(entropyS, entropyE)
	print result + '\t' + str(word_sum) + '\t' + str(gain)