#!/usr/bin/env python
from __future__ import print_function

#This is the script for testing the functions that we've written in mt_tools.py
#Should probably do test driven design etc but man alive I'm alredy so out of my depth one thing at a time ffs

from mt_tools import OpenFile
import os

directory = os.listdir('.')
it_count = 0

for filename in directory:
	it_count +=1
	if filename[-4:] == '.mrc':
		image = OpenFile(filename, it_count)
		header = image.readMrcHeader(filename)

	else:
		continue
