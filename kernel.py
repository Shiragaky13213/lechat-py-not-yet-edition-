#!python3
# -*- coding: utf-8 -*-
########################################
# kernel.py
# launches fully threaded mode
# 



from queue import Queue
from threading import Thread

import threading
import time

from client import *
from config import *
from keepalive import *
from listener import *
from log_chat import *
from log_names import *
from login import *
from responder import *




# start with a blank session
session=''

# create Queues
Q = {
	'abort'		:	Queue(),	# for terminating threads
	'controls'	:	Queue(),	# for commands from client interface
	'postdata'	:	Queue(),	# for sending POSTs to the server
	'runtime'	:	Queue(),	# for selectively launching threads
	'soup'		:	Queue(),	# for passing BeautifulSoup pagedata
	'status'	:	Queue()		# no need yet
	}
#



# primary/core (main) thread
def kernel(Q=Q):
	#
	Client = Thread(target = client, args =(Q['controls'],Q['runtime'],Q['abort'], ))
	Keepalive = Thread(target = keepalive, args =(Q['abort'],session, ))
	Listener = Thread(target = listener, args =(Q['controls'],Q['soup'],Q['abort'],session, ))
	Log_Chat = Thread(target = log_chat, args =(Q['controls'],Q['soup'],Q['abort'], ))
	Log_Names = Thread(target = log_names, args =(Q['controls'],Q['soup'],Q['abort'], ))
	Responder = Thread(target = responder, args =(Q['controls'],Q['soup'],Q['abort'], ))
	#
	running = True
	print("Controller started!")
	while running:
		ui = input(">> ")
		Q['controls'].put(ui)
		if(ui=="/exit"):
			print("Kernel >> shutting down, abort signal placed in queue.")
			running=False
		elif(ui.split()[0]=="/client"):
			if(len(ui.split())>1):
				if(ui.split()[1]=="start"):
					Client.start()
					Q['runtime'].put("client")
				elif(ui.split()[1]=="stop"):
					Client.join()
			else:
				Client.start()
				Q['runtime'].put("client")
		elif(ui.split()[0]=="/keepalive"):
			if(len(ui.split())>1):
				if(ui.split()[1]=="start"):
					Keepalive.start()
					Q['runtime'].put("keepalive")
				elif(ui.split()[1]=="stop"):
					Keepalive.join()
			else:
				Keepalive.start()
				Q['runtime'].put("keepalive")
		elif(ui.split()[0]=="/listen"):
			if(len(ui.split())>1):
				if(ui.split()[1]=="start"):
					Listener.start()
					Q['runtime'].put("listener")
				elif(ui.split()[1]=="stop"):
					Listener.join()
			else:
				Listener.start()
				Q['runtime'].put("listener")
		elif(ui.split()[0]=="/logchat"):
			if(len(ui.split())>1):
				if(ui.split()[1]=="start"):
					Log_Chat.start()
					Q['runtime'].put("logchat")
				elif(ui.split()[1]=="stop"):
					Log_Chat.join()
			else:
				Log_Chat.start()
				Q['runtime'].put("logchat")
		elif(ui.split()[0]=="/lognames"):
			if(len(ui.split())>1):
				if(ui.split()[1]=="start"):
					Log_Names.start()
					Q['runtime'].put("lognames")
				elif(ui.split()[1]=="stop"):
					Log_Names.join()
			else:
				Log_Names.start()
				Q['runtime'].put("lognames")
		elif(ui.split()[0]=="/responder"):
			if(len(ui.split())>1):
				if(ui.split()[1]=="start"):
					Responder.start()
					Q['runtime'].put("responder")
				elif(ui.split()[1]=="stop"):
					Responder.join()
			else:
				Responder.start()
				Q['runtime'].put("responder")
		#
	Q['abort'].put("__sentinel__")
	print("Controller >> shutting down.")
	Client.start()
	#☺
	# Wait for all produced items to be consumed
	print("attempting to clear queues")
	while not Q['runtime'].empty():
		what = Q['runtime'].get()
		if(what=="listener"):
			Listener.join()
		elif(what=="client"):
			Client.join()
		elif(what=="keepalive"):
			Keepalive.join()
		elif(what=="lognames"):
			Log_Names.join()
		elif(what=="logchat"):
			Log_Chat.join()
		elif(what=="responder"):
			Responder.join()
	print("Kernel >> Runtime Queue cleared")
	#
	return
  #
#


# A thread that consumes data
def dummy_thread(controls,soup,abortsignal):
	running=True
	print("Log_names started!")
	old_q = ''
	while running:
		# Check for termination (not yet)
		if(abortsignal.empty()):
			time.sleep(2)
			# Get some data
			data = soup.get()
			soup.put(data)
			# Process the data
			print("Log_names >> pulled ",data," from queue")
		# Check for termination (received)
		else:
			print("Log_names >> thread received abort signal.")
			running=False
			break
	# Indicate completion
	soup.task_done()
	print("Log_names >> shutting down.")
	return
#


#
def start(mode='',session='',OWNNAME=OWNNAME,PASSWORD=PASSWORD):
	#
	print_init()
	#
	# choose mode
	if(mode==""):
		choosing=True
		while(choosing):
			mode = input("Start as BOT or CLIENT? (default is client): ")
			if(mode.lower()=="bot" or mode.lower()=="client" or mode==""):
				choosing=False
			else:
				print("please choose a valid option.")
				wait(1)
	#
	if(PASSWORD==""):
		PASSWORD = random_password()
	#
	# get session, manually or automatically
	if(session==""):
		session=input("session?: ")
	if(session=="load"):
		sessionfile = open('./data/session', 'r')
		session = sessionfile.read()
		sessionfile.close()
	elif(session=="" or session=="new"):
		session = login(OWNNAME,PASSWORD)
	#
	# start
	kernel()
#


#
if __name__ == "__main__":
	#
	start()
	#
#



###############################
# End of file