from bs4 import BeautifulSoup
from datetime import date
import requests
import urllib3
import socks
import time
import http.client
import io
import os
import threading
import re
import base64

url = "http://blkhatjxlrvc5aevqzz5t6kxldayog6jlx5h7glnu44euzongl4fh5ad.onion/"
session = input("Session: ")

if(session==""):
	sessionfile = open('./data/session', 'r')
	session = sessionfile.read()
	sessionfile.close()


header = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'en-US,en;q=0.5',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests' : '1',
			'User-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'
}


if not os.path.exists('./data/'):
	os.mkdir('./data/')
base_path = './data/'+url.replace("https:","").replace("http:","").replace("/","").replace(".onion","")
if not os.path.exists(base_path):
	os.mkdir(base_path)
base_path = base_path+'/Public Notes/'
if not os.path.exists(base_path):
	os.mkdir(base_path)

ledited = []
notes = []
whens = []
whos = []

data = {'lang': 'en',
		'action': 'viewpublicnotes',
		'session': session}
page = requests.post(url, headers=header, data=data)
soupf = BeautifulSoup(page.content, 'html.parser')
soup = BeautifulSoup(str(soupf).replace("<br/>", "\n"), 'html.parser')
notesbody = soup.find('body', {'class': 'publicnotes'}).find('p')
print(notesbody)
# append notes to the list and extract textarea to get the last edited time
for x in notesbody.find_all('textarea'):
	notes.append(x.get_text())
	x.extract()
# get text from the html
notesbody = notesbody.get_text()
# get last edited and nicknames
for line in notesbody.splitlines():
	if line != '':
		who = line.split()[3]
		when = line.split()[5]+'@'+line.split()[6]
		when=when.replace(":","")
		whens.append(when)
		whos.append(who)
		ledited.append(line)
for ledit, note, when, who in zip(ledited, notes, whens, whos):
	fol = base_path+who
	if not os.path.exists(fol):
		os.mkdir(fol)
	fil = fol+'/'+when
	file = open(fil, 'w+')
	file.buffer.write(b"\n" + ledit.encode('utf-8')+b'\n\n'+note.encode('utf-8'))
	file.close()
