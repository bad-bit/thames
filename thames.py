#!/usr/bin/python3
#
#Thames - A software to scrape the internet to identify the themes of websites built on WordPress.
#Author - Vaibhav Choudhari (Twitter - badbit0)

from threading import Thread
from os import path
import requests
import json
import re
import time
import sys
import os
import argparse

#tic = time.perf_counter()

urls = []
themes = []

def main():
	
	parser = argparse.ArgumentParser(
		description='A software to scrape the web for WordPress websites and to identify their themes.', 
		prog='thames.py',
		usage='%(prog)s --help <for help> -k <Serpstack API key> -d <comma seperated Google Dorks in double quotes> -f (OPTIONAL) <path to Google Dork files> -v (OPTIONAL) <verbosity level>')
	parser.add_argument("-k", "--key", help="Your API key as received from Serpstack", required=True, dest='key')
	parser.add_argument("-d", "--dork", help="Comma seperated Google Dorks. Eg: thames.py -d \"intitle: Wordpress, site:.wordpress.com\"", type=str)
	parser.add_argument("-f", "--file", help=" Full path of file listing your search terms / Google Dorks. Eg: thames.py -f C:\somedir\dorkfile.txt", dest='file')
	parser.add_argument("-v", "--verbose", help="Verbosity level", action='count', default=0, dest='verb')
	parser.add_argument("-p", "--page", help="Number of Google search result pages to scrape. Default value is set to 5 pages.", default=5, dest='page', type=int)



	args = parser.parse_args()
	
	if sys.platform.startswith("win"):
		cwd = os.getcwd()
		#need to change directory to CWD for Windows systems where in Python is not in the environment variables.
		os.chdir(cwd)
		if os.path.isfile("serpstack_20.json") and os.path.isfile("Output.txt"):
			os.remove("serpstack_20.json")
			os.remove("Output.txt")
	elif sys.platform.startswith("linux"):
		if os.path.isfile("serpstack_20.json") and os.path.isfile("Output.txt"):
			os.remove("serpstack_20.json")
			os.remove("Output.txt")
			
	if args.file:
		with open(args.file, "r") as dorkfile:
			query = dorkfile.read().splitlines()
	elif args.dork:
		query = args.dork.split(",")
	else:
		print("[--] Please input dorks as comma seperated values in double quotes or input a file containing a list of dorks.\nType thames.py --help for more info.")
		exit()

	
	url = "http://api.serpstack.com/search"
	api_key = args.key 
	#query = ["intitle: Wordpress"] #, "Proudly powered by WordPress", "site:.wordpress.com"]
	num = "10"
	page = args.page
	print(r"""	
				___               _  __ 
				 | |_|  /\  |\/| |_ (_  
				 | | | /--\ |  | |__ _) . py  v1.0

		  						-	badbit0
		""")			 

	print("[+] Execution began!\nScraping "+str(page)+" pages of Google for the given dork(s).\n")
	if page >= 20:
		print("""[~] Please note that the number of search results given by Google usually do not exceed 150. Thus, increasing
the number of pages beyond 20 doesn't really increase the number of scraped URLs. The problem is not with the tool, that is just how
Google works. :D""")
	
	for each_query in query:
		page = args.page
		for page_no in range(1, page+1):			
			page_num = str(page_no)
			request = url+"?"+"access_key="+api_key+"&"+"query="+each_query+"&"+"num="+num+"&"+"page="+page_num
			if args.verb == 1:
				print("[+] Scraping URLs from Google results from page: "+page_num+" for the dork: "+each_query)
			api_request = requests.get(request)
			response = api_request.text

			with open("serpstack_20.json", "a") as file:
				file.write(response)
	
	print("\n")			
	scraper(args.verb)

def scraper(verb_value):

	count = 0

	with open("serpstack_20.json", "r") as file:
		jArray = file.read()
		#converting SERP data into a single JSON object for processing
		newJArray = jArray.replace("}{","},{")
		json_data = json.loads(f'[{newJArray}]')

	try:	
		for i in json_data:	
			for results in i['organic_results']:
				url_list = results['url']
				urls.append(url_list)
	except KeyError:
		print("[-] Your API usage limit has been exhausted on https://www.serpstack.com")
		exit()

	for all_urlz in urls:
		count = count + 1

	print("[+] Total URLs scraped = "+str(count))
	print("\n")		
	t = Thread(target=locator(verb_value))
	t.start()

def locator(verb_value):

	count_url = 0
	count_theme = 0

	print("[+] Attempting to extract themes from scraped websites.\nThis should take time.")

	for each_url in urls:
		#stripping TLD logic goes here.

		count_url += 1
		try:
			req = requests.get(each_url, timeout=30)
			if req.status_code == 302:
				print("    [*]The url: "+each_url+" was redirected." )
			source = req.text
			
			if "wp-content" in source or "wp-includes" in source:
				if verb_value == 2:
					print("[+] The CMS for the website "+each_url+" is WordPress")

				try:					
					finder = re.search(r"themes/[a-zA-Z0-9]+|theme\\/[a-zA-Z0-9]+|themeSlug\":\"[a-zA-Z0-9-]+\\/[a-zA-Z0-9-]+", source)
					l = finder.group()
					themes.append("The theme for the domain: "+each_url+" is - "+l)
				except:
					if verb_value == 2:
						print("[-] Theme not found for - "+each_url+"\nThe CMS for the webiste might not be WordPress\n")		

			else:
				if verb_value == 2:
					print("[-] The CMS for the website "+each_url+" is not WordPress")
		except:			
			print("[-] URL - "+each_url+" seems unreachable, moving to next URL \n\n")	

	#print("\n\n[*] Total URLs listed = "+str(count_url))

	#A new list for only unique hits of "/themes/<theme_name>" from each website's source as a
	#website can have multiple instances of "/themes/<theme_name>" in its source
	to_store = []
	uniq_themes = []
	locked = []
	not_found_list = []
	notctr = 0

	if verb_value == 1:
		print("\n\n[+] Printing themes found: \n")
	
	for all_themes in themes:
		count_theme += 1
		#The list - [themes] will contain junk from the regex. The replace statement below will clean the data and will produce only theme names.
		final = all_themes.replace("themes/", "").replace(r"theme\/", "").replace("themeSlug\":\"pub\\/", "").replace("themeSlug\":\"premium\\/", "")
		if verb_value == 1:
			print(final)
		to_store.append(final)	

	for x in to_store:
	 	with open("Output.txt", "a") as result:
	 		result.write(x+"\n")

	print("\n[*] Total themes found = "+str(count_theme)+"\nThe result has been stored in \"Output.txt\" file. Please copy the output to some other destination if required. The file will be deleted in the next execution.")

	 		
	if verb_value == 1:
		for stored_urls in themes:
			#Filtering out just the URLs from the the list - to_store which will contain the string "The theme for the domain - <URL> is : <theme name>"
			lock = re.search(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", stored_urls)
			p = lock.group()
			locked.append(p)

		print("\n\n")
		
		for not_found in urls:
			if not_found not in locked:
				notctr += 1
				nf = "[*] The theme was not found for the URL: "+not_found 
				not_found_list.append(nf)
		
		print("[*] Theme couldn't be found for the following "+str(notctr)+" websites:\nThe websites might not be using WordPress.\n")
		for all_webs in not_found_list:
			print(all_webs)

# tac = time.perf_counter()
# print("\n\n")	
# print(tac - tic)

if __name__ == '__main__':
	main()
