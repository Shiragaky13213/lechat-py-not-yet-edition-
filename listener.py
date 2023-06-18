#!python3
# -*- coding: utf-8 -*-
########################################
# listener.py
# performs GET requests to the server, and updates the pagefile
# 



from main import *



#
# listener
def listener(controls,soup,abortsignal,session=""):
	#
	running=True
	#
	if(session==""):
		sessionfile = open('./data/session', 'r')
		session = sessionfile.read()
		sessionfile.close()
	#
	print("Listener >> starting up.")
	while(running):
		# Check for termination (not yet)
		if(abortsignal.empty()):
			#
			page = get_frame(session)
			Soup = BeautifulSoup(page.content, 'html.parser')
			Soup = BeautifulSoup(str(Soup).replace(SYSTEM_MSG_CHAR.replace(" ",""),'[SYSTEM_MSG_CHAR]').replace(CHAT_MSG_CHAR.replace(" ",""),'[CHAT_MSG_CHAR]'), 'html.parser')
			#
			pagefile = open(pagefilepath, 'w')
			pagefile.buffer.write(Soup.encode('utf-8'))
			pagefile.close()
			while not soup.empty():
				soup.get()
			soup.put(Soup)
			wait(wait_time)
		# Check for termination (received)
		else:
			print("Listener >> thread received abort signal.")
			running=False
			break
	print("Listener >> shutting down.")
	return
#


#
if __name__ == "__main__":
	#
	print_init()
	#
	if(session==""):
		session=input("session?: ")
	if(session==""):
		sessionfile = open('./data/session', 'r')
		session = sessionfile.read()
		sessionfile.close()
	#
	controls = Queue() # dummy queue to replace controls
	soup = Queue() # dummy queue to replace soup
	abortsignal = Queue() # dummy queue to replace abortsignal
	listener(controls,soup,abortsignal,session)
	#
#



###############################
# End of file