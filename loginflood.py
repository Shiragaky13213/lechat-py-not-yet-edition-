#!python3
# -*- coding: utf-8 -*-
########################################
# login.py
# creates a new session, logging into chat
# 



import base64

from main import *
from capsolver import *



# log in
def login(nickname="",password=""):
	colour = "#FFFFFF"
	values = []
	page = get_frame()
	soup = BeautifulSoup(page.content, 'html.parser')
	#find values
	for x in soup.find_all("input", type="hidden"):
		values += [x['value']]
	nc = values[1]
	challenge = values[3]
	if(nickname==""):
		nickname = input("nick:")
	if(password==""):
		password = input("pass:")
	if(debug>=1):
		print("nc:", nc)
		print("challenge:", challenge)
	#
	#find and solve captcha
	# add code here to detect size of CAPTCHA image, and only pass to solver.py if it is smaller size
	# for larger image (level 3) return to manual review and solving functions
	captcha = solver(base64.b64decode(soup.find("img", alt="")['src'].replace("data:image/gif;base64,","")))
	#
	if(debug>=1):
		print("captcha: ",captcha)
	#
	data = {'lang'		:	'en',
			'nc' : nc,
			'action' : 'login',
			'nick' : nickname,
			'pass' : password,
			'challenge' : challenge,
			'captcha' : captcha,
			'colour'	: '000000'}
	#
	req = requests.Request('POST',url, headers=request_headers,data=data)
	prepared = req.prepare()
	page = websession.send(prepared)
	soup = BeautifulSoup(page.content, 'html.parser')
	#
	values = []
	for x in soup.find_all("input", type="hidden"):
		values +=[x['value']]
	if(debug>=1):
		print("values:",values)
	session = values[7]
	if(debug>=1):
		print("session:",session)
	
	sessionfile = open('./data/session', 'w')
	sessionfile.write(session)
	sessionfile.close()
	return session
#


#
if __name__ == "__main__":
	#
	print_init()
	#
	login()
	#
#



###############################
# End of file