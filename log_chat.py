#!python3
# -*- coding: utf-8 -*-
########################################
# log_chat.py
# listens to the pagefile and keeps a running log of the chat (requires listener)
# 



from main import *



#
# log_chat
def log_chat(controls,soup,abortsignal,session='',printing='off'):
	running=True
	#
	SMC=SYSTEM_MSG_CHAR
	try:
		logfile = open(logpath, encoding='utf-8')
		prev_log = logfile.read()
		logfile.close()
	except:
		logfile = open(logpath, 'w')
		loginit=SMC+" python-lechat-php chatlog\n"+SMC+"\n"+SMC+"\n"+SMC+"\n"+SMC+""
		logfile.buffer.write(loginit.encode('utf-8'))
		logfile.close()
		prev_log = ''
	#
	def update_log(msg):
		file = open(logpath, 'a+')
		file.buffer.write(b"\n" + msg.encode('utf-8'))
		file.close()
	#
	log = []
	prev_log = prev_log.split("\n")#[::-1]
	#
	def fix_multiline(prevlog):
		i=0
		tofix=[]
		Fixed = []
		line=''
		while(i<len(prevlog)):
			line=prevlog[i]
			if(line != ''):
				if(line[0]==SYSTEM_MSG_CHAR[0]):
					pass
				elif(line[0]==CHAT_MSG_CHAR[0]):
					pass
				else:
					tofix.append(i)
			else:
				tofix.append(i)
			i+=1
		i=0
		if(tofix!=[]):
			fixing=tofix[0]-1
		while(i<len(tofix)):
			prevlog[fixing]+="\n"+prevlog[tofix[i]]
			if(i==len(tofix)-1):
				Fixed.append(fixing)
				pass
			else:
				if(tofix[i+1] == tofix[i]+1):
					pass
				else:
					Fixed.append(fixing)
					fixing=tofix[i+1]-1
			i+=1
		for each in reversed(tofix):
			prevlog.pop(each)
		return prevlog,Fixed
	#
	prev_log,Fixed = fix_multiline(prev_log)
	rec_log = prev_log[:-20]
	#
	current_time = time.ctime()[11:19]
	current_date = str(date.today())
	timestamp = current_date + " " + current_time
	#
	update_log(SMC+"\n"+SMC+"\n"+SMC+"\n"+SMC+"---------------------------------------\n"+SMC+" launched at:  at: " + timestamp + "\n"+SMC+"\n"+SMC)
	#
	firstloop=True
	#
	while(running):
		# Check for termination (not yet)
		if(abortsignal.empty()):
			#
			pagefile = open(pagefilepath, 'rb')
			soup = BeautifulSoup(pagefile.read().decode('utf-8', 'ignore'), 'html.parser')
			pagefile.close()
			#
			cleanSoup = BeautifulSoup(str(soup).replace("<br/>", "\n").replace("</br>", "\n").replace("<br>", "\n").replace("</ br>", "\n"), 'html.parser')
			#
			if(firstloop):
				for msg in cleanSoup.find_all('div', class_="msg")[::-1]:
					#
					msg = CHAT_MSG_CHAR+msg.get_text(separator=" ")
					#
					log.append(msg)
					if msg in prev_log:
						if(printing=='on'):
							print(msg[2:])
					else:
						update_log(msg)
						if(printing=='on'):
							print(msg[2:])
				firstloop=False
			else:
				msgpool = cleanSoup.find_all('div', class_="msg")[::-1]
				#msgpool = msgpool[:-20:-1]
				for msg in msgpool:
					#
					msg = CHAT_MSG_CHAR+msg.get_text(separator=" ")
					#
					if msg in log:
						pass
					else:
						update_log(msg)
						log.append(msg)
						if(printing=='on'):
							print(msg[2:])
			wait(2)
		# Check for termination (received)
		else:
			print("Log_Chat >> thread received abort signal.")
			running=False
			break
	print("Log_Chat >> shutting down.")
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
	log_chat(controls,soup,abortsignal,session,'on')
	#
#



###############################
# End of file