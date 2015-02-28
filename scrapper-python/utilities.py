import os, re, urllib2
from xml.dom import minidom

#Print log message to the console
def log(msg):
	print msg
	
#Create the directory of the given name
def create_dir(dirname):
	if not os.path.exists(dirname):
		try:
			os.makedirs(dirname)
		except:
			log('Unable to create directory')
			sys.exit(0)
			
#Get file name from the url
def get_file_name(url):
	url = re.sub(r'https?:\/\/(www\.)?', '', url)
	return url.split('.')[0]
			
#Write the web content response to a file
def write_reponse(response, file_name, scrapper_type):
	dir_path = os.path.abspath('../') + '/resource/' + scrapper_type
	try:
		fobj = open(os.path.join(dir_path, file_name), 'w+')
		fobj.write(response.read())
		fobj.close()
	except Exception, e:
		log(e)
		
#Extract Facebook fan page link
def get_facebook_link(soup):
	facebook_url = None

	if not facebook_url and soup.find('a', href = re.compile(r'.*facebook.*')):
		facebook_url = soup.find('a', href = re.compile(r'.*facebook.*'))['href']
	if not facebook_url and soup.find('div', {"class" : "fb-like"}):
		facebook_url = soup.find('div', {"class" : "fb-like"})['data-href']
	if not facebook_url and soup.find('div', {"class" : "fb-like-box"}):
		facebook_url = soup.find('div', {"class" : "fb-like-box"})["data-href"]
		
	return facebook_url if facebook_url else ''
	
#Read URL From the Resource file.
def get_url_list():
	log("Reading URL.")
	url_path = os.path.abspath('../') + "/resource/urls.txt"
	url_list = []

	try:
		fobj = open(url_path)
		url_list = [url.strip() for url in fobj.readlines()]
		fobj.close()
	except:
		log("Unable to Open File!!")
		
	return url_list