#!python3
# -*- coding: utf-8 -*-
########################################
# keepalive.py
# gives options for wait_time, message, and recipient. then posts on a timer
# 



from main import *



#
# keepalive
def keepalive(abortsignal,session="",anti_timeout_wait="",anti_timeout_recipient="",anti_timeout_post="",debug=0):
	running=True
	#
	if(session==""):
		sessionfile = open('./data/session', 'r')
		session = sessionfile.read()
		sessionfile.close()
	#
	if(anti_timeout_wait==""):
		anti_timeout_wait = input("minutes between posts? (default is 10): ")
		if(anti_timeout_wait==""):
			anti_timeout_wait = 600
		else:
			anti_timeout_wait = int(anti_timeout_wait)*60
			
	#
	if(anti_timeout_post==""):
		anti_timeout_post = input("what will be sent? (default is \".\"): ")
		if(anti_timeout_post==""):
			anti_timeout_post = "."
	#
	if(anti_timeout_recipient==""):
		anti_timeout_recipient=input("anti-timeout PM recipient? (default is 0-Commands-0): ")
		if(anti_timeout_recipient==""):
			anti_timeout_recipient = "0-Commands-0"
	#
	print("session: ",session)
	#
	while(running):
		# Check for termination (not yet)
		if(abortsignal.empty()):
			page = send_post(session,anti_timeout_post,anti_timeout_recipient)
			wait(anti_timeout_wait)
		# Check for termination (received)
		else:
			print("Keepalive >> thread received abort signal.")
			running=False
			break
	print("Keepalive >> shutting down.")
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
	abortsignal = Queue() # dummy queue to replace abortsignal
	keepalive(abortsignal,session)
	#
#



########################################
# End of file