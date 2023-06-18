#!python3
# -*- coding: utf-8 -*-
########################################
# client.py
# terminal user interface
# 



from main import *
from extra import *



#
# client
def client(controls,runtime,abortsignal,session=""):
	running=True
	#
	if(session==""):
		sessionfile = open('./data/session', 'r')
		session = sessionfile.read()
		sessionfile.close()
	#
	if(debug>=1):
		print("session: ",session)
	#
	values = []
	#
	page = get_frame(session,"post")
	#
	# main loop
	while(running):
		# Check for termination (not yet)
		if(abortsignal.empty()):
			values = []
			print("_______________________________________________________________________________")
			soup = BeautifulSoup(page.content, 'html.parser')
			for x in soup.find_all("input", type="hidden"):
				values +=[x['value']]
			nc = values[1]
			postid = values[4]
			#print("# postid: ",postid)
		#
		# end/message/kick/logout
			if not(controls.empty()):
				action = controls.get()
			else:
				action=""
				wait(0.5)
			#action = input(" >> ")
		#
		# logout
			if(action=="/logout"):
				running=False
				logout(session)
				break
		#
		# help
			elif(action.split()[0]=="/help"):
				if(action.split()[1]=="threads"):
					help_threads()
				elif(action.split()[1]=="member"):
					help_member()
				elif(action.split()[1]=="staff"):
					help_staff()
				elif(action.split()[1]=="admin"):
					help_admin()
				else:
					help_client()
		#
		# message
			elif(action.split()[0]=="/post"):
				msg = input("msg:")
				sendto = input("send to:")
				if(sendto=="all" or sendto=="" or sendto=="a"):
					sendto = 's *'
				elif(sendto=="mem" or sendto=="members" or sendto=="m"):
					sendto = 's ?'
				elif(sendto=="staff" or sendto=="s"):
					sendto = 's #'
				elif(sendto=="admin"):
					sendto = 's &amp;'
				data = {"action" : 'post',
						"message" : msg,
						"session" : session,
						"lang" : "en",
						"nc" : nc,
						"sendto" : sendto,
						"postid" : postid}
				page = post_data(data)
		#
		# kick
			elif(action.split()[0]=="/kick"):
				sendto = input("kick who?:")
				msg = input("kick message:")
				purge = input("purge?:")
			#
			# purge
				if(purge=="y" or purge=="yes"):
					data = {"action" : 'post',
							"message" : msg,
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : sendto,
							"postid" : postid,
							'kick' : "kick",
							'what' : "purge"}
				else:
					data = {"action" : 'post',
							"message" : msg,
							"session" : session,
							"lang" : "en",
							"nc" : nc,
							"sendto" : sendto,
							"postid" : postid,
							'kick' : "kick",}
				page = post_data(data)
		#
		# delete
			elif(action.split()[0]=="/delete"):
				if(len(action.split())==1):
					what = input("last or all?: ")
				else:
					what = action.split()[1]
			#
			# delete last
				if(what=="last"):
					data = {'action' : 'delete',
							'session' : session,
							'nc' : nc,
							'what' : 'last'}
					page = post_data(data)
			#
			# delete all
				elif(what=="all"):
					data = {'action' : 'delete',
							'confirm' : 'yes',
							'session' : session,
							'nc' : nc,
							'what' : 'all'}
					page = post_data(data)
				#
			#
		#
		# colour
			elif(action.split()[0]=="/colour"):
				colour = action.split()[1]
				if colour in colours:
					colour = colours[colour]
				data = {"action" : 'profile',
					"session" : session,
					"timestamps" : "on",
					"do" : "save",
					"nc" : nc,
					"colour" : colour}
				page = post_data(data)
				#print_messages()
		#
		# check
			elif(action.split()[0]=="/check"):
				i = 0
				for value in values:
					print("value[",str(i),"]: ",value)
					i+=1
				print("nc: ",nc)
				print("pid: ",postid)
				print("action: ",action)
				print("session: ",session)
			else:
				print("_______________________________________________________________________________")
				print("sorry, that was not a recognized command.")
				print("try: /help for more info about valid commands")
				wait(2)
		# Check for termination (received)
		else:
			print("Client >> thread received abort signal.")
			running=False
			break
	abortsignal.put("__sentinel__")
	print("Client >> shutting down.")
	'''
	get_frame(session,"admin")
	get_frame(session,"controls")
	get_frame(session,"help")
	get_frame(session,"post")
	get_frame(session,"profile")
	get_frame(session,"view")
	get_frame(session,"viewpublicnotes")
	'''
	return
#


#
def help_client():
    print("Commands:")
#

#
def help_threads():
	print("/start <thread>")
	print("available threads: keepalive, listener, logchat, lognames, responder")
	print("")
#

#
def help_member():
    print("Members commands:")
#

#
def help_staff():
    print("Staff Commands:")
#

#
def help_admin():
    print("Admin Commands:")
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
	runtime = Queue() # dummy queue to replace runtime
	abortsignal = Queue() # dummy queue to replace abortsignal
	#
	client(controls,runtime,abortsignal,session)
	#
#



###############################
# End of file