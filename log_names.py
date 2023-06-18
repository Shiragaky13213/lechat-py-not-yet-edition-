#!python3
# -*- coding: utf-8 -*-
########################################
# log_names.py
# listens to the pagefile and keeps track of unique usernames (requires listener)
# 



from main import *



#
# log names
def log_names(controls,soup,abortsignal,session=''):
	running=True
	state = "starting"
	
#	session = input("Session: ")
	
	current_time = time.ctime()[11:19]
	current_date = str(date.today())
	timestamp = current_date + " " + current_time
	
	username = verify_session(session)
#	print("username: ",username)
	
	onlinenicks = []
	nicklogpath = "./data/name.log"
	if not os.path.exists(nicklogpath):
		nicklogfile = open(nicklogpath, 'w+')
		nicklogfile.close()
	
	nickslog = io.open(nicklogpath, 'r', encoding='utf8')
	nicks = nickslog.read()
	nickslog.__exit__()
	
	def update_log(log):
		log = log.encode('utf-8', 'ignore')
		file = open(nicklogpath, 'a+')
		file.buffer.write(log + b"\n")
		file.close()
	
	print("--------------------------------------")
	file = open(nicklogpath, 'a+')
	file.buffer.write(b"\n" + b"----------------------" + b"\n")
#	file.buffer.write(b"launched as: " + username.encode('utf-8', 'ignore') + b"\n")
	file.buffer.write(b"launched at " + timestamp.encode('utf-8', 'ignore') + b"\n\n")
	file.close()
	
	state = "firstloop"
	
	#
	while True:
		# Check for termination (not yet)
		if(abortsignal.empty()):
			current_time = time.ctime()[11:19]
			current_date = str(date.today())
			timestamp = current_date + " " + current_time
			#
			pagefile = open(pagefilepath, 'r')
			soup = pagefile.read()
			pagefile.close()
			#
			soup = BeautifulSoup(soup, 'html.parser')
			#
			#
			nicknames = soup.find("div", {"id" : "chatters"}).get_text().replace("Guests:", "").replace("Members:", "").replace("Staff:", "").replace("Admin:", "")
			if(state == "firstloop"):
				for nick in nicknames.split():
					onlinenicks.append(nick)
					if nick not in nicks:
						log = timestamp + " " + nick + " has been seen for the first time."
					else:
						log = timestamp + " " + nick + " was here on login."
					print(log)
					update_log(log)
				state = "running"
			elif(state == "running"):
				for nick in nicknames.split():
					if nick in onlinenicks:
						pass
					else:
						onlinenicks.append(nick)
						if nick not in nicks:
							log = timestamp + " " + nick + " has been seen for the first time."
						else:
							log = timestamp + " " + nick + " entered."
						print(log)
						update_log(log)
				for x in onlinenicks:
					if x not in nicknames:
						onlinenicks.remove(x)
						log = timestamp + " " + x + " left."
						print(log)
						update_log(log)
			wait(2)
		# Check for termination (received)
		else:
			print("Log_Names >> thread received abort signal.")
			running=False
			break
	print("Log_Names >> shutting down.")
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
	log_names(controls,soup,abortsignal,session)
	#
#



###############################
# End of file