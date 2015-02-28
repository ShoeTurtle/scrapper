import os, time, random, threading, urllib2, glob
from Queue import Queue
from utilities import *
from bs4 import BeautifulSoup

MAX_THREAD = 5
home_finished_queue = Queue(maxsize = 0)

#Extract the home page and write it to the required home folder
def fetch_home_content(url_chunk, i):
	for url in url_chunk:
		try:
			req = urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'})
			response = urllib2.urlopen(req)
			write_reponse(response, get_file_name(url), 'home')
		except Exception, e:
			log(e)
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
		
#Parsing the home content and feeding it into MongoDB
def parse_home():
	#Read the files from ../resource/home
	#Title; Description; Keyword; FacebookURL; LinkedinURL; TwitterURL; AlexaURL
	parse_dir = os.path.abspath('../') + "/resource/home/*"
	file_list = glob.glob(parse_dir)
	
	for each_file in file_list:
		try:
			fobj = open(each_file)
		except Exception, e:
			log(e)
		
		soup = BeautifulSoup(fobj.read())
		title, keyword, facebook_url, twitter_url, alexa_url, linkedin, pin, gplus = '', '', '', '', '', '', '', ''
		
		title = soup.title.text
		
		if soup.find(attrs = {"name" : "description"}) is not None: 
			description = soup.find(attrs = {"name" : "description"}).get('content')
		
		if soup.find(attrs = {"name" : "keywords"}):
			keyword = soup.find(attrs = {"name" : "keywords"}).get('content')
			
		facebook_url = get_facebook_link(soup)
		
		if soup.find('a', href = re.compile(r'.*twitter.*')):
			twitter_url = soup.find('a', href = re.compile(r'.*twitter.*'))['href']
		
		if soup.find('a', href = re.compile(r'.*linkedin.*')):
			linkedin = soup.find('a', href = re.compile(r'.*linkedin.*'))['href']
			
		if soup.find('a', href = re.compile(r'.*plus\.google.*')):
			gplus = soup.find('a', href = re.compile(r'.*plus\.google.*'))['href']
			
		print "File Path - " + each_file
		print "Title - " + title
		print "Keywords - " + keyword
		print "Facebook URL - " + facebook_url
		print "Twitter URL - " + twitter_url
		print "Linkedin URL - " + linkedin
		print "Google Plus URL - " + gplus
		print "************"
	
#Initializing Home Scrapper Job
def init_home_scapper():
	
	#1. Read the url from ../resources/urls.txt
	url_list = get_url_list()

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