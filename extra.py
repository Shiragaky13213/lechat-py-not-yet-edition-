#!python3
# -*- coding: utf-8 -*-
########################################
# extra.py
# nonessential functionality, such as random name/password/messages
# 



import random
import string



#
class extend_class(set):
	def __init__(self, *args, **kwargs):
		self._lock = Lock()
		super(extend_class, self).__init__(*args, **kwargs)
	
	def add(self, elem):
		self._lock.acquire()
		try:
			super(extend_class, self).add(elem)
		finally:
			self._lock.release()
	
	def delete(self, elem):
		self._lock.acquire()
		try:
			super(extend_class, self).delete(elem)
		finally:
			self._lock.release()
#

#
def lock_decorator(method):
	def new_deco_method(self, *args, **kwargs):
		with self._lock:
			return method(self, *args, **kwargs)
	return new_deco_method
#
class Decorator_class(set):
	def __init__(self, *args, **kwargs):
		self._lock = Lock()
		super(Decorator_class, self).__init__(*args, **kwargs)
	
	@lock_decorator
	def add(self, *args, **kwargs):
		return super(Decorator_class, self).add(elem)
	
	@lock_decorator
	def delete(self, *args, **kwargs):
		return super(Decorator_class, self).delete(elem)
#


#
def random_name(sets=''):
	CHOSEN = 0
	namesdir = S.fix_path('data/names/')
	namefiles = os.listdir(namesdir)
	namesets = []
	names = []
	quant  = 0
	for namefile in namefiles:
		namesets.append(namefile)
		print(namefile + " added to the selection")
	while(CHOSEN==0):
		print("")
		print("[RANDOM NAME SELECTOR] OPTIONS: all (a), " + str(namesets))
		print("If you do not type any input here it will default to 'all'")
		sets = input("which set(s) would you like to choose from? >> ")
		if(sets==''): 
			sets = 'a'
		if(sets=='a') or (sets=='any'):
			CHOSEN = 1
			for nameset in namesets:
				with open(namesdir+nameset, "r") as namefile:
					for name in namefile:
						names.append(name)
						quant=quant+1
		else:
			CHOSEN = 1
			for nameset in namesets:
				if(sets.find(nameset) != -1):
					with open(namesdir+nameset, "r") as namefile:
						for name in namefile:
							names.append(name)
							quant=quant+1
		#else:
		#	print("error.. try again.")
	d2 = ''
	CHOSEN=0
	print("# quant: "+str(quant))
	while(CHOSEN==0):
		d2 = names[random.randint(0, (quant))]
		d2 = d2.replace('\r', '')
		d2 = d2.replace('\n', '')
		random_name=d2
		if(len(random_name) >=3):
			if(random_name.find("#") == -1):
				print("")
				print(("choose "+random_name+" as a random name."))
				user_choice = input("use this name? y or * >> ")
				if(user_choice=='y'): CHOSEN=1
	return random_name
#

#
def random_post(type_of_speech='null',volume='silent'):
	CHOSEN=0
	posts_basepath = "./data/posts/"
	PATH = {
				"conspiracy"	:	"conspiracy.txt",
				"fact"			:	"fact.txt",
				"insult"		:	"insult.txt",
				"meme"			:	"meme.txt",
				"music"			:	"music.txt",
				"nuetral"		:	"nuetral.txt",
				"poetry"		:	"poetry.txt",
				"question"		:	"question.txt",
				"shitpost"		:	"shitpost.txt"
			}
	posts = []
	postfilepath = posts_basepath
	while(CHOSEN==0):
		if(type_of_speech=='null'): 
			print("")
			print("RANDOM POST SELECTOR: ")
			print(" (n=nuetral, s=shitpost, q=question, f=fact, c=conspiracy, p=poem) ")
			print("If you do not type any input here it will default to 'nuetral'")
			type_of_speech = input("which set would you like to choose from? >> ")
		if(type_of_speech==''): 
			type_of_speech = 'n'
		type_of_speech = type_of_speech.lower()
		if(type_of_speech=='c') or (type_of_speech=='conspiracy'):
			CHOSEN = 1
			postfilepath += PATH['conspiracy']
		elif(type_of_speech=='i') or (type_of_speech=='insult'):
			CHOSEN = 1
			postfilepath += PATH['insult']
		elif(type_of_speech=='f') or (type_of_speech=='fact'):
			CHOSEN = 1
			postfilepath += PATH['fact']
		elif(type_of_speech=='meme'):
			CHOSEN = 1
			postfilepath += PATH['meme']
		elif(type_of_speech=='music'):
			CHOSEN = 1
			postfilepath += PATH['music']
		elif(type_of_speech=='n') or (type_of_speech=='nuetral'):
			CHOSEN = 1
			postfilepath += PATH['nuetral']
		elif(type_of_speech=='p') or (type_of_speech=='poetry'):
			CHOSEN = 1
			postfilepath += PATH['poetry']
		elif(type_of_speech=='q') or (type_of_speech=='question'):
			CHOSEN = 1
			postfilepath += PATH['question']
		elif(type_of_speech=='s') or (type_of_speech=='shitpost'):
			CHOSEN = 1
			postfilepath += PATH['shitpost']
		else:
			print("error.. try again.")
	#
	with open(postfilepath, "r") as postsfile:
		lines  = 0
		for line in postsfile:
			posts.append(line)
			lines=lines+1
	d2 = ''
	CHOSEN=0
	if(volume=="silent"):
		while(CHOSEN==0):
			d2 = posts[random.randint(0, (lines-1))]
			d2 = d2.replace('\r', '')
			d2 = d2.replace('\n', '')
			random_post=d2
			if(len(random_post) >=3):
				if(random_post.find("#") == -1):
					CHOSEN=1
	else:
		while(CHOSEN==0):
			d2 = posts[random.randint(0, (lines-1))]
			d2 = d2.replace('\r', '')
			d2 = d2.replace('\n', '')
			random_post=d2
			if(len(random_post) >=3):
				if(random_post.find("#") == -1):
					print("")
					print(("chose "+random_post+" as a random post."))
					user_choice = input("use this post? y or * >> ")
					if(user_choice=='y'): CHOSEN=1
	return random_post
#

#
def random_password(length = 32):
	characters = string.ascii_letters + string.digits + string.punctuation
	password = ''.join(random.choice(characters) for i in range(length))
	return password
#


#
'''
def waiting_room_handler(content):
	if(VERBOSE >= 2): print("# ------------- waiting_room_handler start -------------")
	MOD_APPROVAL_ON = 0
	WAITING = 0
	HAD_TO_WAIT = 0
	wait_time = 0
	session_found = 0
	pagedata = content	
	if pagedata.find("your login has been delayed") != -1:
		print("# Waiting Room Handler engaged..")
		WAITING = 1
		HAD_TO_WAIT = 1
	if pagedata.find("moderator") != -1:
		MOD_APPROVAL_ON = 1
	if (MOD_APPROVAL_ON == 0): 
		while (WAITING == 1):
			print("# ")
				#[o_o]< find wait time
			wt_bef = content.find('you can access the chat in ')
			wt_aft = content.find(' seconds.</p>')
			wt_tmp = content[wt_bef:wt_aft]
			wt1 = len(wt_tmp)
			wt2 = wt1 - 13
			wt3 = wt_tmp[27:wt1]
			wait_time = int(wt3)
			print(("# wait time set to: " + str(wait_time)))
				#[o_o]< waiting room session finder
			if(session_found==0):
				print("# attempting to isolate sessionID from page...")
				sbef = content.find('<input type="hidden" name="session" value="')
				saft = content.find('"><input type="submit" value="Reload" >')
				sess1 = content[sbef:saft]
				len1 = len(sess1)
				len2 = len1 - 39
				sess2 = sess1[43:len1]
	#			print(sess1)
	#		   print("# sessionID is: " + sess2)
				session = sess2
				print(("# sessionID is saved as: " + session))
				wsf=open(datadir+'SESSION','w')
				wsf.write(session)
				wsf.close()
				session_found = 1
				#[o_o]< NC/ Next PostID / post verification value finder
				#[o_o]<	if(VERBOSE >= 2): print(content)
			if(VERBOSE >= 2): print("# this should be an error handler ;p")
			print("# attempting to isolate next postID from post box...")
			string1 = '<input type="hidden" name="nc" value="'
			string2 = '"><input type="hidden" name="action" value='
			pid_bef = content.find(string1)
			pid_aft = content.find(string2)
			pid1 = content[pid_bef:pid_aft]
			len1 = len(pid1)
			len2 = len1 - len(string2)
			pid2 = pid1[38:len1]
#		   print(pid1)
#		   print("# sessionID is: " + pid2)
			npid = pid2
#		   print("# next post ID is: " + npid)
			npidf=open(datadir+'NPID','w')
			npidf.write(session)
			npidf.close()
			time.sleep(wait_time+10)
			send_message = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
			post_data = urllib.parse.urlencode({
										'lang'  : 'en',
										'nc'  : npid,
										'action'  : 'wait',
										'session' : session})
			req = urllib.request.Request(url+"?action=post&session="+session+"&lang=en")
			content = send_message.open(url, post_data.encode()).read().decode('utf-8')
			if content.find("your login has been delayed") < 1:
				WAITING = 0
	if (MOD_APPROVAL_ON == 1): 
		while (WAITING == 1):
			wait_time = 15
			print("# waiting for moderator approval...")
			time.sleep(wait_time)
			print("# checking back every 15 seconds or so...")
				#[o_o]< waiting room session finder
			if(session_found==0):
				print("# attempting to isolate sessionID from page...")
				sbef = content.find('<input type="hidden" name="session" value="')
				saft = content.find('"><input type="submit" value="Reload" >')
				sess1 = content[sbef:saft]
				len1 = len(sess1)
				len2 = len1 - 39
				sess2 = sess1[43:len1]
				print(sess1)
#			   print("# sessionID is: " + sess2)
				session = sess2
				print(("# sessionID is saved as: " + session))
				wsf=open(datadir+'SESSION','w')
				wsf.write(session)
				wsf.close()
				session_found = 1
				#[o_o]< NC/ Next PostID / post verification value finder
				#	if(VERBOSE >= 2): print(content)
			if(VERBOSE >= 2): print("# this should be an error handler ;p")
			print("# isolating next postID from page...")
			string1 = '<input type="hidden" name="nc" value="'
			string2 = '"><input type="hidden" name="action" value='
			pid_bef = content.find(string1)
			pid_aft = content.find(string2)
			pid1 = content[pid_bef:pid_aft]
			len1 = len(pid1)
			len2 = len1 - len(string2)
			pid2 = pid1[38:len1]
#		   print(pid1)
#		   print("# sessionID is: " + pid2)
			npid = pid2
#		   print("# next post ID is: " + npid)
			npidf=open(datadir+'NPID','w')
			npidf.write(session)
			npidf.close()
			send_message = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
			post_data = urllib.parse.urlencode({
										'lang'  : 'en',
										'nc'  : npid,
										'action'  : 'wait',
										'session' : session})
			req = urllib.request.Request(url+"?action=post&session="+session+"&lang=en")
			content = send_message.open(url, post_data.encode()).read().decode('utf-8')
			#[o_o]< add "you have been kicked" support
			#[o_o]< add timedout support
			if content.find("your login has been delayed") < 1:
				WAITING = 0
	if HAD_TO_WAIT == 1:
		print("# had to wait")
	if(VERBOSE >= 2): print("# ------------- waiting_room_handler end -------------")
	return content
#
'''
#



###############################
# End of file