from threading import Thread
import requests
import json
import re
import time
import os
import argparse

urls = []
themes = []

#parse the following:
#mandatory - api key, path to dorks, no. of pagese to scrape in google (should be less than 100)
#optional - 



def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-k", "--key", help="Your API key as received from Serpstack")
	parser.add_argument("-f", "--file", help="Path of file listing your search terms / Google Dorks")
	args = parser.parse_args()



	url = "http://api.serpstack.com/search"
	api_key = "a5cdb1b4a31855554f51374c382641b5"
	query = ["site:.wordpress.com", "Proudly powered by WordPress", "intitle: Wordpress"]
	num = "100"
	page= "1"

	for each_query in query:
		for page in range(1, 11):
			page_num = str(page)
			request = url+"?"+"access_key="+api_key+"&"+"query="+each_query+"&"+"num="+num+"&"+"page="+page_num

#			print(request)
			scraper(request)

def scraper(request):
   #urls = []
	api_request = requests.get(request)
	response = api_request.text
	#print(response)

	with open("serpstack_20.json", "w") as file:
		file.write(response)

	with open("serpstack_20.json", "r") as file:
		output = json.load(file)
		for results in output['organic_results']:
			url_list = results['url']
			urls.append(url_list)

	#print(urls)
	#for each_url in urls:		
	#	cms_find(each_url)
	cms_find()

def cms_find():
			
	t = Thread(target=locator)
	t.start()

def locator():
	for each_url in urls:
		try:
			req = requests.get(each_url, timeout=30)
			source = req.text

			# #regex to identify themes/<theme name> = themes/[a-zA-Z0-9]+
			if "wp-content" in source:
				print("[+] The CMS for the website "+each_url+" is WordPress")
				theme = re.findall(r"themes/[a-zA-Z0-9-]+", source)
				for i in theme:
					website = each_url
					#Appends wach hit for /themes in the list themes[]		
					themes.append("The theme for the domain: "+website+" is - "+i)
					

			else:
				print("[-] The CMS for the website "+each_url+" is not WordPress")
		except:
			print("[-] Moving to next URL \n\n")		

	#A new list for only unique hits of "/themes/<theme_name>" from each website's source as a
	#website can have multiple instances of "/themes/<theme_name>" in its source
	to_store = []
	uniq_themes = []

	print("\n\n[+] Printing themes found: \n")
	for all_themes in themes:
		#Only select unique hits of "/themes/<theme_name>"		
		if all_themes not in uniq_themes:
			uniq_themes.append(all_themes)

	for print_themes in uniq_themes:
		#stripping out the "/themes" from "/themes/<theme_name>"
		final = print_themes.replace("themes/", "")
		print(final)
		to_store.append(final)

	#print(to_store)

	for x in to_store:
	 	with open("Output", "a") as result:
	 		result.write(x+"\n")

if __name__ == '__main__':
	main()
