#!/usr/bin/python

from utilities import *
from home_scraper import *

if(__name__ == "__main__"):
	#1. Initialize the required folder structure
	log("Creating Directory Structure.")
	folder_list = ['home', 'facebook', 'twitter', 'linkedin']
	for folder_name in folder_list:
		create_dir("../resource/" + folder_name)
		
	#2. Initialize Home Scrapper
	init_home_scapper()
	
	#3. Initialize Facebook Scrapper
	
	#4. Initialize Twitter Scrapper
	
	#5. Initialize Linkedin Scrapper
	
	log('\n**SCRAPING COMPLETE**')