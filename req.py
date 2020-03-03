import requests
import re

themes = []
urls = []

def main():
	
	count_url = 0
	count_theme = 0

	with open("urls", "r") as file:
		for x in file:

			y = x.replace("\n","")
			count_url = count_url + 1
			urls.append(y)
	print("Total URLS = "+str(count_url)+"\n\n")

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
		count_theme = count_theme + 1
		#stripping out the "/themes" from "/themes/<theme_name>"
		final = print_themes.replace("themes/", "")
		print(final)
		to_store.append(final)

	print("\n\nTotal themes found = "+str(count_theme))

	#print(to_store)

	# for x in to_store:
	#  	with open("Output", "a") as result:
	#  		result.write(x+"\n")

if __name__ == '__main__':
	main()

