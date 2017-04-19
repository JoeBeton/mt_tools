#!/usr/bin/env python
from __future__ import print_function

#This is the library which contains all the functions that we will be writing 
#to track and box microtubules as well as anything else that we'll be doing.

import numpy as np
import struct


class OpenFile(object):
	'''
	A class for opening .mrc image files of motionCorr corrected EM images
	
	Not at all sure that this needs to be a class rather than a list of functions but oh well
	
	The structure of the mrc header information can be found at: http://www.ccpem.ac.uk/mrc_format/mrc2000.php
	'''
	
	def __init__(self, filename, it_count):
		
		self.filename = filename
		self.it_count = it_count

		

		#some numpy initialisation which is in the Tempy code, no idea what we need to do though

	def readMrcHeader(self, filename):
		#reads the mrc header lol
		f = open(filename, 'rb')	#opens the file as read only and reads it as a binary file
		fm_string = '<'+(10*'l')+(6*'f')+(3*'l')+(3*'f')+(27*'l')+(3*'f')+(4*'c')+'lfl'
		header = list(struct.unpack(fm_string, f.read(224)))
		
		#making a readable annotated version 
		number = np.arange(60)
		header_stack = np.column_stack([number[1:],header])
		print( header_stack)


#class FindMicrotubules():



#class BoxMicrotubules():


