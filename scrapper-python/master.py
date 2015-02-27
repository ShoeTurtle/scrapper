#!/usr/bin/python

import os, threading, time
import random
from Queue import Queue

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
	varying_timer = [2, 5, 1, 6, 3]
	for url in url_chunk:
		time.sleep(random.choice(varying_timer))
		home_finished_queue.put(url)
		
def home_print_queue(url_size):
	finished_count = 0
	while (True):
		url = home_finished_queue.get()
		if (url == 'EXIT'):
			break
		finished_count = finished_count + 1
		log('Completed - [%s/%s] - %s'%(finished_count, url_size, url))
	
if(__name__ == "__main__"):
	MAX_THREAD = 5

	home_finished_queue = Queue(maxsize = 0)
	
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
		
	thread_home_print_queue = threading.Thread(target=home_print_queue, args=(len(url_list),))
	thread_home_print_queue.start()
	
	#4. Submit the jobs to the subsequent threads
	log('Initiating Home Downloads. \n')
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
		
	home_finished_queue.put('EXIT')
	
	thread_home_print_queue.join()
	
	log('\n**HOME SCRAPING COMPLETE**')