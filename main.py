#!python3
# -*- coding: utf-8 -*-
########################################
# main.py
# contains the majority of core functionality
# 
# Todo:
#	add script to automatically install requirements
#	BS4, pillow, imagehash, 
#	much more... see _readme.txt


from bs4 import BeautifulSoup
from configparser import ConfigParser
from datetime import date
from queue import Queue
from sys import exit as terminate
from time import sleep as wait

import io
import os
#import socks
import time

from config import *
from chat_data import *



# this can be changed if you want to save/load configuration from a different location
configfile='./data/user_config'

# loads long-term configurable variables from ./data/user_config
def load_config():
	config = ConfigParser()
	#
	config.read(configfile)
	#
	print(config.get('main', 'key1')) # -> "value1"
	print(config.get('main', 'key2')) # -> "value2"
	print(config.get('main', 'key3')) # -> "value3"
	#
	# getfloat() raises an exception if the value is not a float
	a_float = config.getfloat('main', 'a_float')
	#
	# getint() and getboolean() also do this for their respective types
	an_int = config.getint('main', 'an_int')
	#
	return
#

# saves long-term configurable variables in ./data/user_config
def save_config():
	config = ConfigParser()
	#
	config.read(configfile)
	config.add_section('main')
	config.set('main', 'key1', 'value1')
	config.set('main', 'key2', 'value2')
	config.set('main', 'key3', 'value3')
	#
	with open(configfile, 'w') as f:
		config.write(f)
	#
	return
#


# GET a frame, defaults to 'view' frame (messages) can also be used for profile, admin, etc
def get_frame(session="",action="",base_url=base_url):
	url = base_url
	if(len(action)>1):
		url = url+"?action="+action
		if(len(session)>1):
			url = url+"&session="+str(session)
	if(len(action)==0 and len(session)>1):
		url = url+"?action=view&session="+session
	if(debug>=1):
		print("GET: ",url)
		print("session: "+session)
		print("action: "+action)
	page = websession.get(url, headers=request_headers)
	return page
#

# verify a session, returns username on success, or error notice on failure
def verify_session(session):
	page = get_frame(session,"post")
	soup = BeautifulSoup(page.content, 'html.parser')
	try:
		username = soup.find("tr", {"id" : "firstline"}).get_text().split(":")[0]
		if(debug>=1):	print("username: "+username)
		return username
	except:
		return "Error: Invalid/expired session."
#

# get hidden "values" from post frame, including nonce and postID
def get_values(session):
	values = []
	page = get_frame(session,"post")
	soup = BeautifulSoup(page.content, 'html.parser')
	for x in soup.find_all("input", type="hidden"):
		values += [x['value']]
	nc = values[1]
	postid = values[4]
	if(debug>=1):
		print_values(values)
	return values
#

# print a page's hidden values
def print_values(values):
	i = 0
	for value in values:
		print("value[",str(i),"]: ",value)
		i+=1
	return
#

# POST data to the server, structured as a dict={'1':'a','2':'b'}
def post_data(data):
	if(debug>=1):
		print("POST: ",url)
	page = websession.post(url, headers=request_headers, data=data)
	return page
#


def get_values(session):
	values = []
	page = get_frame(session,"post")
	soup = BeautifulSoup(page.content, 'html.parser')
	for x in soup.find_all("input", type="hidden"):
		values += [x['value']]
	print(values)
	nc = values[1]
	#postid = nc
	postid = values[4] # they should be different, but are often the same
	return nc,postid

# send a POST to the chat server
def send_post(session,msg="",sendto="all",kick="",purge=""):
	nc,postid = get_values(session)
	print("_______________________________")
	#if(debug>=1):
	#	print_values(values)
	if(sendto=="all") or (sendto=="") or (sendto==" ") or (sendto=="a"):
		sendto = 's *'
	elif(sendto=="mem") or (sendto=="members") or (sendto=="m"):
		sendto = 's ?'
	elif(sendto=="staff") or (sendto=="s") or (sendto=="st") or (sendto=="stf"):
		sendto = 's #'
	elif(sendto=="admin") or (sendto=="adm") or (sendto=="a"):
		sendto = 's &amp;'
	if(msg=="KILL"):
		running=0
	if(kick=="kick"):
		data = {'action'  : 'post',
				'session' : session,
				"message": msg,
				'multi'   : '',
				"lang": "en",
				"nc" : nc,
				"sendto" : sendto,
				"postid" : postid,
				'kick'	: "kick",
				'what'	: purge}
	else:
		data = {'action'  : 'post',
				'session' : session,
				"message": msg,
				'multi'   : '',
				"lang": "en",
				"nc" : nc,
				"sendto" : sendto,
				"postid" : postid}
	
	page = post_data(data)
	return page
#

# parse a message to find the sender
def find_sender(post,own_name=OWNNAME):
	sender = ""
	if(debug>=1):
		print("split[0]: ",post.split()[0])
		print("split[1]: ",post.split()[1])
		print("split[2]: ",post.split()[2])
		print("split[3]: ",post.split()[3])
		print("split[4]: ",post.split()[4])
		print("split[5]: ",post.split()[5])
	#	print("split[6]: ",post.split()[6])
	print("split[0]: ",post.split()[0])
	print("split[1]: ",post.split()[1])
	print("split[2]: ",post.split()[2])
	print("split[3]: ",post.split()[3])
	print("split[4]: ",post.split()[4])
	print("split[5]: ",post.split()[5])
	print(post)
	if(len(post) > 3):
		if(post.split()[3] == "["):
			if(post.split()[4] == own_name):
				sender = post.split()[6]
			else:
				sender = post.split()[4]
		else:
			sender = post.split()[3]
	else:
		sender = "s *"
	return sender
#

# this is how it was, for some reason .decode was not wanted
def find_sender2(post,own_name=OWNNAME):
	sender = ""
	if(debug>=1):
		print("split[0]: ",post.decode('utf-8').split()[0])
		print("split[1]: ",post.decode('utf-8').split()[1])
		print("split[2]: ",post.decode('utf-8').split()[2])
		print("split[3]: ",post.decode('utf-8').split()[3])
		print("split[4]: ",post.decode('utf-8').split()[4])
		print("split[5]: ",post.decode('utf-8').split()[5])
	#	print("split[6]: ",post.decode('utf-8').split()[6])
	if(post.decode('utf-8').split()[3] == "["):
		if(post.decode('utf-8').split()[4] == own_name):
			sender = post.decode('utf-8').split()[6]
		else:
			sender = post.decode('utf-8').split()[4]
	else:
		sender = post.decode('utf-8').split()[3]
	return sender
#

# check session, 
def check_session(session):
	page = get_frame(session,"post")
#	

# log out the current session
def logout(session):
	data = {'action'  : 'logout',
			'session' : session}
	page = post_data(data)
	return page
#

#
def print_init(time=1):
	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	print(" ___       _______   ________  ___  ___  ________  _________    ")
	print("|\\  \\     |\\  ___ \\ |\\   ____\\|\\  \\|\\  \\|\\   __  \\|\\___   ___\\  ")
	print("\\ \\  \\    \\ \\   __/|\\ \\  \\___|\\ \\  \\\\\\  \\ \\  \\|\\  \\|___ \\  \\_|  ")
	print(" \\ \\  \\    \\ \\  \\_|/_\\ \\  \\    \\ \\   __  \\ \\   __  \\   \\ \\  \\   ")
	print("  \\ \\  \\____\\ \\  \\_|\\ \\ \\  \\____\\ \\  \\ \\  \\ \\  \\ \\  \\   \\ \\  \\  ")
	print("   \\ \\_______\\ \\_______\\ \\_______\\ \\__\\ \\__\\ \\__\\ \\__\\   \\ \\__\\ ")
	print("    \\|_______|\\|_______|\\|_______|\\|__|\\|__|\\|__|\\|__|    \\|__| ")
	print("\n\n")
	wait(time)
#



###############################
# End of file