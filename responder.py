#!python3
# -*- coding: utf-8 -*-
########################################
# responder.py
# listens to the log or pagefile and responds to preconfigured stimuli
# 



from main import *
from extra import *



#
# responder
def responder(controls,soup,abortsignal,session=""):
	#
	if(session==""):
		sessionfile = open('./data/session', 'r')
		session = sessionfile.read()
		sessionfile.close()
	#
	logfile = open(logpath, encoding='utf-8')
	prev_log = logfile.read().split("\n")[::-1]
	logfile.close()
	own_name = verify_session(session)
	#
	checked=[]
	responded=[]
	#
	def postqueue(msg):
		send_post(msg)
		'''
		if ():
			pq.put(msg)
		elif():
			send_post(msg)
		else:
			print("!shrug")'''
		return
	#
	#
	while(running==1):
		logfile = open(logpath, encoding='utf-8')
		log = logfile.read().split("\n")#[::-1]
		logfile.close()
		#
		msgpool = log[:-20:-1]
		#print("MSGPOOL: \n",msgpool)
		for msg in msgpool:
			#print("MSG: \n",msg)
			if msg in checked:
				pass
			elif(SYSTEM_MSG_CHAR in msg):
				pass
			elif(CHAT_MSG_CHAR not in msg):
				pass
			else:
				#print(msg)
				checked.append(msg)
				msg = msg.replace(CHAT_MSG_CHAR,'')
				print("finding sender for message: /n",msg)
				sender = find_sender(msg)
				print("sender was: \n",sender)
				#
				#
				if(msg.split()[3]=="["):
					post_status = "private"
					if(len(msg.split())>=10):
						if("public" in msg):
							recipient = "s *"
						else:
							recipient = sender
					else:
						recipient = sender
				else:
					post_status = "public"
					recipient = "s *"
					#
				if(post_status == "private") or (post_status == "public" and msg.split[5] == "@"+own_name):
					#
					print(session)
					nc,postid = get_values(session)
					# MUSIC
					if "!music" in str(msg):
						if(debug>=1):
							print("Responder >> !music requested by: "+sender)
						data = {
							"action" : 'post',
							"message" : random_post("music"),
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : recipient,
							"postid" : postid}
						#sending = 1
						postqueue(data)
					#
					# MEME
					if "!meme" in str(msg):
						if(debug>=1):
							print("Responder >> !meme requested by: "+sender)
						data = {
							"action" : 'post',
							"message" : random_post("meme"),
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : recipient,
							"postid" : postid}
						print("SENDING: \n",data)
						postqueue(data)
					#
					# INSULT
					if "!insult" in str(msg):
						if(debug>=1):
							print("Responder >> !insult requested by: "+sender)
						data = {
							"action" : 'post',
							"message" : random_post("insult"),
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : recipient,
							"postid" : postid}
						postqueue(data)
					#
					# FACT
					if "!fact" in str(msg):
						if(debug>=1):
							print("Responder >> !fact requested by: "+sender)
						data = {
							"action" : 'post',
							"message" : random_post("fact"),
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : recipient,
							"postid" : postid}
						postqueue(data)
					#
					# CONSPIRACY
					if "!conspiracy" in str(msg):
						if(debug>=1):
							print("Responder >> !conspiracy requested by: "+sender)
						data = {
							"action" : 'post',
							"message" : random_post("conspiracy"),
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : recipient,
							"postid" : postid}
						postqueue(data)
					#
					# QUESTION
					if "!question" in str(msg):
						if(debug>=1):
							print("Responder >> !question requested by: "+sender)
						data = {
							"action" : 'post',
							"message" : random_post("question"),
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : recipient,
							"postid" : postid}
						postqueue(data)
					#
					# SHITPOST
					if "!shitpost" in str(msg):
						if(debug>=1):
							print("Responder >> !shitpost requested by: "+sender)
						data = {
							"action" : 'post',
							"message" : random_post("shitpost"),
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : recipient,
							"postid" : postid}
						postqueue(data)
					#
					# POEM
					if "!poem" in str(msg) or "!poetry" in str(msg):
						if(debug>=1):
							print("Responder >> !poem requested by: "+sender)
						data = {
							"action" : 'post',
							"message" : random_post("poetry"),
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : recipient,
							"postid" : postid}
						postqueue(data)
					#
					# DELETE ALL
					if "!delete-all" in str(msg):
						if(debug>=1):
							print("Responder >> !delete-all issued by: "+sender)
						data = {'action' : 'delete',
								'confirm' : 'yes',
								'session' : session,
								'nc' : values[1],
								'what' : 'all'}
						postqueue(data)
					#
					# DELETE LAST
					if "!delete-last" in str(msg):
						if(debug>=1):
							print("Responder >> !delete-last issued by: "+sender)
						data = {'action' : 'delete',
								'session' : session,
								'nc' : values[1],
								'what' : 'last'}
						postqueue(data)
					#
					# LOGOUT
					if "!logout" in str(msg):
						print("Responder >> !logout command issued by: "+sender)
						logout(session)
					#
					# KICK
					if "!kicktest" in str(msg):
						if(debug>=1):
							print("Responder >> !kicktest issued by: "+sender)
						data = {
							"action" : 'post',
							"message" : "fuck off",
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : sender,
							"postid" : postid,
							'kick'	: "kick"}
						postqueue(data)
					#
					# KICK+PURGE
					if "!kickpurgetest" in str(msg):
						if(debug>=1):
							print("Responder >> !kickpurgetest issued by: "+sender)
						data = {
							"action" : 'post',
							"message" : "fuck off",
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : sender,
							"postid" : postid,
							'kick'	: "kick",
							'what'	: purge}
						postqueue(data)
					'''
					if(sending==1):
						values = get_values(session)
						page = post_data(data)
					'''
					#
					#
					#
					if last_msg == msg:
						#print("lst: ",last_msg)
						pass
					elif last_msg != msg:
						pass
		#
		wait(2)
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
	responder(controls,soup,abortsignal,session)
	#
#



###############################
# End of file