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
#change url to "domain" in the key organic_results



def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-k", "--key", help="Your API key as received from Serpstack")
	parser.add_argument("-f", "--file", help="Path of file listing your search terms / Google Dorks")
	args = parser.parse_args()



	url = "http://api.serpstack.com/search"
	api_key = "f0503c3e3c3760fcb21678fbe54ca38c" # ppcall - "322655c5ba05066cbb7afb7b2d85f52d" # vc@gmail.com - "a5cdb1b4a31855554f51374c382641b5"
	query = ["site:.wordpress.com"] #, "Proudly powered by WordPress", "intitle: Wordpress"]
	num = "15"
	page= "3"

	for each_query in query:
		for page in range(1, 4):
			page_num = str(page)
			request = url+"?"+"access_key="+api_key+"&"+"query="+each_query+"&"+"num="+num+"&"+"page="+page_num

#			print(request)
			print("Sending request for page: "+page_num)

			api_request = requests.get(request)
			response = api_request.text

			with open("serpstack_20.json", "a") as file:
				file.write(response)
	print("\n\n")			
	scraper()

def scraper_2(request):
	jsonz = []

	api_request = requests.get(request)
	response = api_request.text
	jsonz.append(response)

	for all_reqs in jsonz:	
		reks = json.dumps(all_reqs)
		#output = json.load(reks)
		for results in reks['organic_results']:
			url_list = results['url']
			urls.append(url_list)

	for all_urlz in urls:
		print(all_urlz)

def scraper():
	
	# print(page_num)
	urls = []
	count = 0
	# api_request = requests.get(request)
	# response = api_request.text
	# #print(response)

	# with open("serpstack_20.json", "a") as file:
	# 	file.write(response)

	with open("serpstack_20.json", "r") as file:
		jArray = file.read()
		newJArray = jArray.replace("}{","},{")
		json_data = json.loads(f'[{newJArray}]')

	for i in json_data:	
		for results in i['organic_results']:
			url_list = results['url']
			urls.append(url_list)

	for all_urlz in urls:
		count = count + 1

	print("[+] Total urls found = "+str(count))
	print("Printing all URLs: \n")
	
	for all_urls in urls:
		print(all_urls)


	# 	output = json.load(file)
	# 	for results in output['organic_results']:
	# 		url_list = results['url']
	# 		urls.append(url_list)

	# for all_urlz in urls:
	# 	print(all_urlz)

	#print(urls)
	#for each_url in urls:		
	#	cms_find(each_url)
	#cms_find()

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
