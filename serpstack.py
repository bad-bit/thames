import requests
import json
import re

urls = []

def main():

	url = "http://api.serpstack.com/search"
	api_key = "a5cdb1b4a31855554f51374c382641b5"
	query = "immunity inc"
	num = "20"

	request = url+"?"+"access_key="+api_key+"&"+"query="+query+"&"+"num="+num
	#print(request)


def scraper(request)
   #urls = []
	api_request = requests.get(request)
	response = api_request.text
	#print(response)

	with open("serpstack_20.json", "w") as file:
		file.write(response)

	with open("serpstack_20.json", "r") as file:
		output = json.load(file)
		for p in output['organic_results']:
			url_list = p['url']
			urls.append(url_list)

	for each_url in urls:
		cms_find(each_url)
	

def cms_find(each_url):
	req = requests.get(each_url)
	source = req.text

	#regex to identify themes/<theme name> = themes/[a-zA-Z0-9]+
	if "wp-content" in source:
		print("[+] The CMS for the website "+each_url+" is WordPress")
	else:
		print("[-] The CMS for the website "+each_url+" is not WordPress")



if __name__ == '__main__':
	main()
