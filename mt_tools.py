#!/usr/bin/env python
from __future__ import print_function

#This is the library which contains all the functions that we will be writing 
#to track and box microtubules as well as anything else that we'll be doing.

import numpy as np
import struct
from skimage import io


class OpenFile(object):
	'''
	A class for opening .mrc image files of motionCorr corrected EM images
	
	Not at all sure that this needs to be a class rather than a list of functions but oh well
	
	The structure of the mrc header information can be found at: http://www.ccpem.ac.uk/mrc_format/mrc2000.php
	'''
	
	def __init__(self, filename):
		
		self.filename = filename
		

	def readMrcHeader(self, filename):
				
		#reads the mrc header lol
		f = open(filename, 'rb')	#opens the file as read only and reads it as a binary file
		fm_string = '<'+(10*'l')+(6*'f')+(3*'l')+(3*'f')+(27*'l')+(3*'f')+(4*'c')+'lfl'
		header = list(struct.unpack(fm_string, f.read(224)))
		
		#making a readable annotated version - just used to look at whilst we're writing code lad lmao amiright
		number = np.arange(60)
		header_stack = np.column_stack([number[1:],header])
		print( header_stack)
		
		return header

	def openImage(self):

		'''
		THIS FUNCTION IS CURRENTLY BROKEN - SAVED IMAGE HAS NO FEATURES AND STRANGE LEVELS
		
		This is a gimped function that only works on our .mrc files so will need to be edited to be more smart in the future

		There is something in the header that says when the data starts but for us it was always zero so christ knows what it means
		'''
		
		#Get relevant header information
		header = self.readMrcHeader(self.filename)
		
		col_number = header[0]
		row_number = header[1]
		print( col_number, row_number)
		
		'''
		data_start = header[4]	would want to use this for the code to be more flexible - cba to do this at the moment though
		'''
		#kills this function if opening an multi-dimensional mrc file like a density map or tomogram
		section_number = header[2]
		if section_number != 1:
			print('No 3-dimensional arrays please')
			return
		
		#Open the whole file and pull out correctly formatted image
		with open(self.filename, 'rb') as f:
			
			#length of total file is 56956944
					
			#Making a string for opening the file using the C-struct open function - 1024*x ignores all bytes in the header file
			#this is gimped to always use floats which might not always be ideal
			data_open_string = '<'+(1024*'x')+((col_number*row_number)*'f')
			
			#This unpacks the data in the file - the *4 scaling is TOTALLY gimped and I have no idea why its 4 and not 8 for example
			whole_file = struct.unpack(data_open_string, f.read((col_number*row_number)*4+1024))

			data_chunk = np.float32(whole_file)
			
			image = np.reshape(data_chunk, [col_number, row_number])
						
			io.imsave('test.tiff',image)
			
			self.image = image 

#class FindMicrotubules():



#class BoxMicrotubules():


