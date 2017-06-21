#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPR support functions

@author: J. Andrew Howe June 2017

Copyright John Andrew Howe 2017.  This code may be freely used, modified, and distributed
as long as this text in the docstring remains unaltered, with full attribution to me, and 
under the restriction that no charge is ever levied, and no payment ever expected, requested,
accounted for, or received for it.  I've chosen not to profit by making the efforts of my
work available here, and nobody else should profit either.
"""

import numpy as np

def PrintTable(data,formats,colheads,rowheads = None):
	"""
	This function takes in a table of numbers, and returns a nicely formatted character
	string table that can be printed to the console. To directly manipulate the table
	rows, use tablist = string.split(table,'\n').
	---
	Usage: table = PrintTable(data,format,colheads,rowheads=None)
	---	
	data: (nxp) array of data
	formats: (px1) array_like of sprintf style column formats; if single string is input, every
		column is formatted identically
	colheads: (px1) array_like of column headings
	rowheads*: (nx1) optional array_like of row headings
	table: string of formatted table
	---
	ex:
  print(QB.PrintTable(rnd.rand(5,3),'%0.2f',['1','ii','three'],['one','two','three','four','five']))
	
  JAH 20121030
	"""	

	# unlike most of QREDIS_Basic, it doesnt make sense to allow input of not (n,p) array (even if n or p is 1)
	try:
		(datr,datc) = data.shape
	except Exception as e:
		raise e("Variable data must be a 2-d array: %s"%PrintTable.__doc__)
	
	# replicate formats if needed
	if type(formats) is str:
		formats = [formats]*datc
	# and make blank rowheads if needed: do this because it makes the code simpler
	if rowheads is None:
		rowheads = ['']*datr
	
	# check inputs
	try:
		# check column headers - can be either array or list, should make no difference
		if len(colheads) != datc:
			raise ValueError("The number of column headers must match number columns of data: %s"%PrintTable.__doc__)
		# check format strings - can be either array or list, should make no difference
		if len(formats) != datc:
			raise ValueError("The format strings must be 1 or match number columns of data: %s"%PrintTable.__doc__)
		# check row headers - can be either array or list, should make no difference
		if len(rowheads) != datr:
			raise ValueError("The number of row headers must match number rows of data: %s"%PrintTable.__doc__)	
	except TypeError:
		# if it comes here, it's probably because an input is not array_like i.e. len() didn't work; this will cause a typeerror
		raise TypeError("Something wrong with one of the inputs: %s"%PrintTable.__doc__)	
	
	# get lengths
	lens = np.zeros((datr+1,datc),dtype=int)
	# get lengths of column headings
	lens[0,:] = [len(ch) for ch in colheads]
	# now get the lengths of all the data
	for rcnt in range(datr):
		lens[rcnt+1,:] = [len(("%s"%formats[ccnt])%data[rcnt,ccnt]) for ccnt in range(datc)]
	# get the max lengths for each column + 1 extra column for each variable except last
	maxes = np.max(lens,axis=0)+1; maxes[-1] = maxes[-1] - 1
	extras = maxes - lens
	
	# prepare for row headings, if appropriate
	rhbars = ''
	rhclhd = ''
	if rowheads is not None:
		# get the lens and max
		rhlens = [len(rh) for rh in rowheads]
		rhmax = np.max(rhlens)+1
		# build the bar & column header space
		rhbars = '-'*rhmax
		rhclhd = ' '*rhmax
		# left-justify the row headers
		rowheads = [rowheads[rcnt]+' '*(rhmax-rhlens[rcnt]) for rcnt in range(datr)]
	
	# now build up the table string
	bars = '-'*np.sum(maxes) + rhbars
	tablestr = bars
	# first add the column headers
	thisrow = rhclhd
	for ccnt in range(datc):
		# pad is created by div'ing the extra space by 2 (if odd, rounds down) and adding one ...
		# JAH 20121221, in preparation for future use of 3.x, force integer division with //, since floor
		# division will no longer be the default		
		pad = ' '*(extras[0,ccnt]//2+1)
		# ... then taking [1:maxes+1] of the result we should get the exact length column with
		# even pads or 1 extra on the right if required DAMN I'm gooooood JAH
		thiscol = ('%s%s%s'%(pad,colheads[ccnt],pad))[1:(maxes[ccnt]+1)]
		# append the column to the row
		thisrow = thisrow + thiscol
	# append the row to the table
	tablestr +='\n'+thisrow+'\n'+bars
	
	# now do the exact same thing, but for the columns of the data
	for rcnt in range(datr):
		thisrow = rowheads[rcnt]
		for ccnt in range(datc):
			pad = ' '*(extras[rcnt+1,ccnt]//2+1)
			thiscol = ('%s%s%s'%(pad,("%s"%formats[ccnt])%data[rcnt,ccnt],pad))[1:(maxes[ccnt]+1)]
			# append the column to the row
			thisrow = thisrow + thiscol
		# append the row to the table
		tablestr +='\n'+thisrow
	tablestr+='\n'+bars
	
	return tablestr
