import os

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