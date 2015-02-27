#!/usr/bin/python

import os

def create_dir(dirname):
	if not os.path.exists(dirname):
		try:
			os.makedirs(dirname)
		except:
			log('Unable to create directory')
			sys.exit(0)
			
def log(msg):
	print msg

if(__name__ == "__main__"):
	MAX_THREAD = 5
	
	#1. Initialize the required folder structure
	log("Creating Directory Structure.")
	folder_list = ['home', 'facebook', 'twitter', 'linkedin']
	for folder_name in folder_list:
		create_dir("../resource/" + folder_name)
	
	#2. Read the url from ../resources/urls.txt
	log("Reading URL.")
	url_path = os.path.abspath('../') + "/resource/urls.txt"
	url_list = []

	try:
		fobj = open(url_path)
		url_list = [url.strip() for url in fobj.readlines()]
		fobj.close()
	except:
		log("Unable to Open File!!")
		
	#3. Distrubute the urls for each of the threads
	log('Distributing Thread Jobs.')
	url_distribution = []
	for i in range(MAX_THREAD):
		url_distribution.append([])
	
	url_count = 0
	for url in url_list:
		url_distribution[url_count % MAX_THREAD].append(url)
		url_count = url_count + 1
