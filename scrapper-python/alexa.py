import urllib, sys, threading
from utilities import *
from xml.dom import minidom
from Queue import Queue

alexa_url_queue = Queue(maxsize = 0)
ALEXA_THREAD_COUNT = 5

#The Worker Funtion for the Alexa Thread Block
def alexa_worker():
	while True:
		url = alexa_url_queue.get()
		print alexa_rating(url)
		alexa_url_queue.task_done()

#Retrieve the alexa rating and store it into the database
def fetch_alexa_rating():
	url_list = get_url_list()
	
	for i in range(ALEXA_THREAD_COUNT):
		alexa_thread = threading.Thread(target=alexa_worker)
		alexa_thread.daemon = True
		alexa_thread.start()
		
	#Queue up all the urls
	for each_url in url_list:
		alexa_url_queue.put(each_url)
		
	alexa_url_queue.join()
	
#Fetch the Alexa Rating for each for each of the url
def alexa_rating(url):
	xml_block = urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url).read()
	xml_dom = minidom.parseString(xml_block).getElementsByTagName('REACH')
	
	for tag in xml_dom:
		rank = tag.getAttribute('RANK')
		
	return rank