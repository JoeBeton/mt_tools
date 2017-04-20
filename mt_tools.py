#!/usr/bin/env python
from __future__ import print_function

#This is the library which contains all the functions that we will be writing 
#to track and box microtubules as well as anything else that we'll be doing.

import numpy as np
import struct
from skimage import io, measure, draw, feature
from scipy import ndimage

class OpenFile(object):
	'''
	A class for opening .mrc image files of motionCorr corrected EM images
	
	The class constructs an object containing all the image data and important information needed for calculations later in the code, such as image dimensions and filename
	
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
		
		self.col_number = header[0]
		self.row_number = header[1]
		
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
			
			data_chunk = np.fromfile(f, dtype = mrcNumpy[header[3]], count = self.col_number*self.row_number)	#takes all the pixel values from the mrc file
			
			image = np.reshape(data_chunk, [self.row_number, self.col_number])	#creates an array with the correct dimensions 
			
			self.image_data = image
			
			return self

	def makeConfig(self):
		pass
		
	
	def openConfig(self):
		
		pixel_size = 1.39
		
		self.pixel_size = pixel_size
		
		return self


class FindMicrotubules(object):		#called with the image_object from openImage class - this will almost certainly create a massive headache down the line
	def __init__(self):
		pass
	
	def bandPassFilter(self, image_data):
		#Apply a band pass filter of desired dimensions (in real space) to the image - couldn't find any prewritten stuff on skimage or ndimage so may as well write our own lel.
		
		#Need to get the fourier transform of the original image and apply a circular mask of appropriate size? - I'm SURE there's a better mathmatical way to do this.
		
		fft_image = np.fft.fft2(image_data)
		fft_dimensions = np.shape(fft_image)	
		
		#Constructing a circular mask to apply to the FFT
		central_coordinate = [int(fft_dimensions[0]/2), int(fft_dimensions[1]/2)]
		radius = 10 #this will need to calculated depending on the extent of filtering required
		mask_shape_x, mask_shape_y = draw.circle(central_coordinate[0], central_coordinate[1], radius)
		fft_mask = np.zeros((fft_dimensions[0], fft_dimensions[1]), dtype = np.complex128)				#making an initisalised array of 0's
		fft_mask[mask_shape_x, mask_shape_y] = 1														#building in the circular mask in to the array
		
		#Reordering the mask so that it can be applied to the wierdly ordered FFT
		quadrant4 = fft_mask[0:central_coordinate[0], 0:central_coordinate[1]]
		quadrant2 = quadrant4[::-1]
		quadrant1 =  fft_mask[central_coordinate[0]:fft_dimensions[0], central_coordinate[1]:fft_dimensions[1]]
		quadrant3 = quadrant1[::-1]
		half1 = np.concatenate((quadrant1,quadrant2), axis = 1)
		half2 = np.concatenate((quadrant3,quadrant4), axis = 1)
		fft_mask = np.append(half1,half2, axis = 0)

		#Applying the mask to the fft of the original image
		filtered_fft = np.multiply(fft_image, fft_mask) 			#remains a complex128 array after masking
		filtered_image = np.fft.fft2(filtered_fft)
		
		io.imsave('quadrant.tiff',np.float32(fft_mask))
		io.imsave('filtered_image.tiff',np.float32(filtered_image))
		
		return np.float32(filtered_image)
		
		
	def findIce(self):
		#Will always want to box microtubules that are sitting in the ice and not over carbon
		#However, there isn't always carbon in an image and there is often absolutely loads of carbon in an image
		#how in gods name can we deal with that problem
		
		#could try to find the ice/carbon interface using a sobel filter? - need to bin and remove high frequency components?
		
		binned_image = measure.block_reduce(self.image_data, block_size = (4,4), func = np.mean)
		
		filtered_image = FindMicrotubules.bandPassFilter(self, binned_image)
		
		sobel_image = ndimage.sobel(filtered_image)
		
		canny_image = feature.canny(filtered_image, 5)
		
		io.imsave('canny_image.tiff',np.float32(canny_image))
		
		


#class BoxMicrotubules():


###################################################
#Function Tests
###################################################

if __name__ == '__main__':
	pass
	#run some tests
