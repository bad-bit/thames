import json
import requests
import re

urls = []
def main():

	# resp = ""
	# file = open("serpstack.txt", "r")
	# x = file.readlines()
	#urls = []
	with open("serpstack.json", "r") as file:
		output = json.load(file)
		for p in output['organic_results']:
			x = p['url']
			#print(x)

			urls.append(x)

	for each_url in urls:
		cms_find(each_url)

#	print(urls)
			#print("URL: " + p['url'])

#	print(output['organic_results'])

	# file1 = open("write_json.txt", "w")
	# json.dump(x, file1) 

	# strings = json.loads(file1)
	# print(json.dumps(file1, indent = 4, sort_keys = True))

def cms_find(each_url):
	req = requests.get(each_url)
	source = req.text

	look = re.findall(r"href=\".*\"", source)
	for each_href in look:
		if "themes/" in each_href:
			print(each_href)
	
	# if look:
	# 	print("[+]Theme found")
	# else:
	# 	print("[-]Theme not found")


	# if "wp-content" in source:
	# 	print("[+] The CMS for the website "+each_url+" is WordPress")
	# else:
	# 	print("[-] The CMS for the website "+each_url+" is not WordPress")



if __name__ == '__main__':
	main()