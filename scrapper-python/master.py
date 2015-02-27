#!/usr/bin/python

import os

def create_dir(dirname):
	if not os.path.exists(dirname):
		try:
			os.makedirs(dirname)
		except:
			print 'Unable to create directory'
			sys.exit(0)

if(__name__ == "__main__"):
	THREAD_COUNT = 20
	
	#Initialize the required folder structure
	folder_list = ['home', 'facebook', 'twitter', 'linkedin']
	for folder_name in folder_list:
		create_dir("../resource/" + folder_name)
	print "Directory Creation Complete"

