#!/usr/bin/python

from bs4 import BeautifulSoup

#import requests
#url = raw_input("Enter a website to extract the URL's from: ")
#r  = requests.get("http://" +url)


with open("nextrain.html") as fp:
    soup = BeautifulSoup(fp, "html5lib")

#for link in soup.find_all('a'):
#    print(link.get('href'))


import re
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)