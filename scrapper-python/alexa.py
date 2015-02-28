import urllib, sys
from utilities import *
from xml.dom import minidom

#Retrieve the alexa rating and store it into the database
def fetch_alexa_rating():
	url_list = get_url_list()
	
	for each_url in url_list:
		print alexa_rating(each_url)
		
#Fetch the Alexa Rating for each for each of the url
def alexa_rating(url):
	xml_block = urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url).read()
	xml_dom = minidom.parseString(xml_block).getElementsByTagName('REACH')
	
	for tag in xml_dom:
		rank = tag.getAttribute('RANK')
		
	return rank