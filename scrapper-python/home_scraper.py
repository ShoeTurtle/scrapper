import os, time, random, threading
from Queue import Queue
from utilities import *

MAX_THREAD = 5
home_finished_queue = Queue(maxsize = 0)

#Extract the home page and write it to the required home folder
def fetch_home_content(url_chunk, i):
	varying_timer = [2, 5, 1, 6, 3]
	for url in url_chunk:
		time.sleep(random.choice(varying_timer))
		home_finished_queue.put(url)

#Prints the completed task
def home_print_queue(url_size):
	finished_count = 0
	while (True):
		url = home_finished_queue.get()
		if (url == 'EXIT'):
			break
		finished_count = finished_count + 1
		log('Completed - [%s/%s] - %s'%(finished_count, url_size, url))
		
#Initializing Home Scrapper Job
def init_home_scapper():
	
	#1. Read the url from ../resources/urls.txt
	log("Reading URL.")
	url_path = os.path.abspath('../') + "/resource/urls.txt"
	url_list = []

	try:
		fobj = open(url_path)
		url_list = [url.strip() for url in fobj.readlines()]
		fobj.close()
	except:
		log("Unable to Open File!!")
		
	
	#2. Distrubute the urls for each of the threads
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
	
	#3. Submit the jobs to the subsequent threads
	log('Initiating Home Downloads. \n')
	my_threads = []
	thread_count = 0
	for url_chunk in chunk_holder:
		thread_fetch_home_content = threading.Thread(target=fetch_home_content, args=(url_chunk, thread_count,))
		thread_fetch_home_content.start()
		my_threads.append(thread_fetch_home_content)
		thread_count = thread_count + 1
		
	#4. Syncronize the threads
	for thread in my_threads:
		thread.join()
		
	home_finished_queue.put('EXIT')
	thread_home_print_queue.join()