#!/usr/bin/python

from utilities import *
from home_scraper import *
from alexa import *

if(__name__ == "__main__"):
	#1. Initialize the required folder structure
	log("Creating Directory Structure.")
	folder_list = ['home', 'facebook', 'twitter', 'linkedin']
	for folder_name in folder_list:
		create_dir("../resource/" + folder_name)
		
	#2. Initialize Home Scrapper; Write the Home stats to the database
	# init_home_scapper()
	# parse_home()
	fetch_alexa_rating()
	# get_page_rank()
	
	log('\n**SCRAPING COMPLETE**')