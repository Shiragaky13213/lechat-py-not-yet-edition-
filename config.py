#!python3
# -*- coding: utf-8 -*-
########################################
# config.py
# stores user and core configurations, will be moved to main.py and /data/user_config
# 



import requests



##### USER CONFIGURATION #####

OWNNAME = "test"
PASSWORD = "idgjso8eguy4w0p8tg4r5w3egt"
# username / password, for if you always want to use the same one


proxification = "pythonproxy"
# OPTIONS: "externalproxy", "pythonproxy"
# defines whether to use python proxy, or external proxification (such as whonix)
# the externalproxy mode will probably be known as "direct" in the next version


TOR_type = "tbb"
# OPTIONS: "tbb", "torservice"
# this could be simplified, but is used to select proper port 9150 (tbb) or 9050 (service)


target = "bhc"
# OPTIONS: "clear", "onion"
# determines url to use for requests to the server
# in testing, only clear and onion are used, referencing chat.danwin1210.me, the demo chat
# this should be usable for defining a custom chat url







##### SCRIPT CONFIGURATION #####
#
mode=""
session=""
debug = 0
running = 1
wait_time = 5
#
logpath = "./data/chat.log"
pagefilepath = "./data/pagefile"
#
#
#
#
SYSTEM_MSG_CHAR = '✪ '
CHAT_MSG_CHAR = '❖ '
post = {}
values = []
last_msg = ""
msg = ""
sender = ""
kick = ""
purge = ""



##### NETWORK CONFIGURATION #####

# create a method for communication with the server
websession = requests.session()

# set default headers for use in any request
request_headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'en-US,en;q=0.5',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
	#		'Cookie': 'language=en; chat_session='+session,
	#		'Host'	:	'chat.danwin1210.me',
	#		'TE'	:	'Trailers',
			'Upgrade-Insecure-Requests' : '1',
			'User-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'
	}
#

# defines tor proxies
python_tor_proxies = {
						'tbb'			:	{
												'http' : "socks5h://127.0.0.1:9150",
												'https' : "socks5h://127.0.0.1:9150"
											},
						'torservice'	:	{
												'http' : "socks5h://127.0.0.1:9050",
												'https' : "socks5h://127.0.0.1:9050"
											}
	}
#


url_clear = ""
url_onion = ""
if(proxification=="pythonproxy"):
	if(TOR_type=="tbb"):
		websession.proxies = python_tor_proxies['tbb']
	else:
		websession.proxies = python_tor_proxies['torservice']
else:
	if(os.path.exists("./data/external_proxy")):
		pass
	else:
		confirmation=input("you are about to send requests over the network, and python proxification is not enabled. your traffic will be sent over clearnet, unless you are using external proxification. is this your intent? (type \"yes\" to continue): ")
		if(confirmation=="yes"):
			confirmation=input("would you like to not be reminded of this? (if you type \"yes\" the script will not warn you again): ")
			if(confirmation=="yes"):
				tempfile = open("./data/external_proxy", 'w+')
				tempfile.close()
		else:
			terminate("confirmation not given to send unproxied traffic,\n exiting software.")
#



#
URL = {
	"placeholder"		:	"blank",
	#
	"dans_clear"		:	"https://chat.danwin1210.me/chat.php",
	"dans_onion"		:	"https://danschat356lctri3zavzh6fbxg2a7lo6z3etgkctzzpspewu7zdsaqd.onion/chat.php",
	#
	"blackhat"			:	"http://blkhatjxlrvc5aevqzz5t6kxldayog6jlx5h7glnu44euzongl4fh5ad.onion/index.php",
	#
	}
#


#
if(target=="clear"):
	base_url = URL['dans_clear']
elif(target=="onion"):
	base_url = URL['dans_onion']
elif(target=="bhc" or target=="blackhat"):
	base_url = URL['blackhat']
else:
	base_url = URL['dans_clear']
url = base_url
#



###############################
# End of file