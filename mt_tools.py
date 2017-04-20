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
				
		#reads the mrc header - Only the first 224 bytes of the header actually contain any useful information
		
		f = open(filename, 'rb')	#opens the file as read only and reads it as a binary file
		fm_string = '<'+(10*'l')+(6*'f')+(3*'l')+(3*'f')+(27*'l')+(3*'f')+(4*'c')+'lfl'	#makes a string used in struct.unpack - shamelessly stolen from Tempy
		header = list(struct.unpack(fm_string, f.read(224)))
		
		#making a readable annotated version - just used to look at whilst we're writing code lad lmao amiright
		#number = np.arange(60)
		#header_stack = np.column_stack([number[1:],header])
		#print( header_stack)
		
		return header

	def openImage(self):

		'''		
		This is a gimped function that only works on our .mrc files so will need to be edited to be more smart in the future

		There is something in the header that says when the data starts but for us it was always zero so christ knows what it means
		'''
		
		#Get relevant header information
		header = self.readMrcHeader(self.filename)
		
		col_number = header[0]
		row_number = header[1]
		
		#Making a dictionary for correct parsing of data - again taken shamelessly from Tempy
		
		mrcNumpy = {
			1: np.uint8,
			2: np.float32,
			4: np.complex64
		}
		
		#kills this function if opening a multi-dimensional mrc file like a density map or tomogram
		section_number = header[2]
		if section_number != 1:
			print('No 3-dimensional arrays please')
			self.image = False
			return self
		
		#Open the whole file and pull out correctly formatted image
		with open(self.filename, 'rb') as f:
			
			f.seek(1024) 	#Moves the current position to 1024 bytes in to the file which skips the header info which we don't want
			
			#Some sort of addition f.seek(number) that accounts for the differing start points as stipulated by the header
			
			data_chunk = np.fromfile(f, dtype = mrcNumpy[header[3]], count = col_number*row_number)	#takes all the pixel values from the mrc file
			
			image = np.reshape(data_chunk, [row_number, col_number])	#creates an array with the correct dimensions 
			
			self.image_data = image
			
			return self
		
	def binImage(self):
		
		#we will definitely want to make some kind of binned image to jack around with - better SNR and less memory needed so faster
		
		pass
		


#class FindMicrotubules():



#class BoxMicrotubules():


