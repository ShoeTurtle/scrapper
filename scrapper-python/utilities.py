import os, re

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