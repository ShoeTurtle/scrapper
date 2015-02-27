#!/usr/bin/python

import os, threading

def create_dir(dirname):
	if not os.path.exists(dirname):
		try:
			os.makedirs(dirname)
		except:
			log('Unable to create directory')
			sys.exit(0)
			
def log(msg):
	print msg

def fetch_home_content(url_chunk, i):
	for url in url_chunk:
		print url + " -- " + str(i)
		
	#Maybe insert something in the queue
	
if(__name__ == "__main__"):
	MAX_THREAD = 5
	
	home_ongoing_queue = Queue()
	facebook_ongoing_queue = Queue()
	linkedin_ongoing_queue = Queue()
	twitter_ongoing_queue = Queue()
	
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
	chunk_holder = []
	for i in range(MAX_THREAD):
		chunk_holder.append([])
	
	url_count = 0
	for url in url_list:
		chunk_holder[url_count % MAX_THREAD].append(url)
		url_count = url_count + 1
		
	#4. Submit the jobs to the subsequent threads
	my_threads = []
	thread_count = 0
	for url_chunk in chunk_holder:
		thread_fetch_home_content = threading.Thread(target=fetch_home_content, args=(url_chunk, thread_count,))
		thread_fetch_home_content.start()
		my_threads.append(thread_fetch_home_content)
		thread_count = thread_count + 1
		
	#5. Syncronize the threads
	for thread in my_threads:
		thread.join()
		
	
	