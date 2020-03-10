#!/usr/bin/python3
#
#Thames - A software to scrape the web for WordPress websites and to identify there themes
#Author - Vaibhav Choudhari (badbit)
#Website - https://www.badbit.vc


from threading import Thread
import requests
import json
import re
import time
import os
import argparse

urls = []
themes = []

#TODO
#1. parse the following:
#mandatory - api key, path to dorks, no. of pagese to scrape in google (should be less than 100)
#3. Add to WP detection logic - Done
#4. Optimize/Lean the regex
#5. Color & font
#6. Cool logo
#7. Learn to format print statements the pro way by using curly braces
#8. Stress test program on VPS

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-k", "--key", help="Your API key as received from Serpstack")
	parser.add_argument("-f", "--file", help="Path of file listing your search terms / Google Dorks")
	args = parser.parse_args()



	url = "http://api.serpstack.com/search"
	api_key = "f0503c3e3c3760fcb21678fbe54ca38c" #shriyakulkarni -  # ppcall - "322655c5ba05066cbb7afb7b2d85f52d" # vc@gmail.com - "a5cdb1b4a31855554f51374c382641b5"
	query = ["site:.wordpress.com"] #, "Proudly powered by WordPress", "intitle: Wordpress"]
	num = "15"
	page= "4"

	for each_query in query:
		for page in range(1, 5):
			page_num = str(page)
			request = url+"?"+"access_key="+api_key+"&"+"query="+each_query+"&"+"num="+num+"&"+"page="+page_num

			print("Sending request for page: "+page_num)

			api_request = requests.get(request)
			response = api_request.text

			with open("serpstack_20.json", "a") as file:
				file.write(response)
	print("\n\n")			
	scraper()

def scraper():
	
	# print(page_num)
	count = 0

	with open("serpstack_20.json", "r") as file:
		jArray = file.read()
		#converting SERP data into a single JSON object for processing
		newJArray = jArray.replace("}{","},{")
		json_data = json.loads(f'[{newJArray}]')

	for i in json_data:	
		for results in i['organic_results']:
			url_list = results['url']
			urls.append(url_list)

	for all_urlz in urls:
		count = count + 1

	print("[+] Total urls found = "+str(count))
	print("\n\n")		
	t = Thread(target=locator())
	t.start()

def locator():

	count_url = 0
	count_theme = 0

	for each_url in urls:
#		print(each_url)
		count_url += 1
		try:
			req = requests.get(each_url, timeout=30)
			if req.status_code == 302:
				print("    [*]The url: "+each_url+" was redirected." )
			source = req.text

			# #regex to identify themes/<theme name> = themes/[a-zA-Z0-9]+
			if "wp-content" or "wp-includes" in source:
				print("[+] The CMS for the website "+each_url+" is WordPress")

				try:					
					finder = re.search(r"themes/[a-zA-Z0-9]+|theme\\/[a-zA-Z0-9]+|themeSlug\":\"[a-zA-Z0-9-]+\\/[a-zA-Z0-9-]+", source)
					l = finder.group()
					themes.append("The theme for the domain: "+each_url+" is - "+l)
				except:
					print("Unable to regex")		

			else:
				print("[-] The CMS for the website "+each_url+" is not WordPress")
		except:
			print("[-] URL seems unreachable, moving to next URL \n\n")	

	print("\n\n[*] Total URLs listed = "+str(count_url))

	#A new list for only unique hits of "/themes/<theme_name>" from each website's source as a
	#website can have multiple instances of "/themes/<theme_name>" in its source
	to_store = []
	uniq_themes = []

	print("\n\n[+] Printing themes found: \n")
	
	for all_themes in themes:
		count_theme += 1
		final = all_themes.replace("themes/", "").replace(r"theme\/", "").replace("themeSlug\":\"pub\\/", "").replace("themeSlug\":\"premium\\/", "")
		print(final)
		to_store.append(final)

	print("\n\n[*] Total themes found = "+str(count_theme))	

	for x in to_store:
	 	with open("Output", "a") as result:
	 		result.write(x+"\n")


	for not_found in urls:
		if not_found not in to_store:
			print("\n\nThe theme was not found for the URL: "+not_found)


if __name__ == '__main__':
	main()
