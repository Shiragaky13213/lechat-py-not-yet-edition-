#!python3
# -*- coding: utf-8 -*-
########################################
# _readme.txt
# 
# 



 ________  ___    ___             ___       _______   ________  ___  ___  ________  _________   
|\   __  \|\  \  /  /|           |\  \     |\  ___ \ |\   ____\|\  \|\  \|\   __  \|\___   ___\ 
\ \  \|\  \ \  \/  / /___________\ \  \    \ \   __/|\ \  \___|\ \  \\\  \ \  \|\  \|___ \  \_| 
 \ \   ____\ \    / /\____________\ \  \    \ \  \_|/_\ \  \    \ \   __  \ \   __  \   \ \  \  
  \ \  \___|\/  /  /\|____________|\ \  \____\ \  \_|\ \ \  \____\ \  \ \  \ \  \ \  \   \ \  \ 
   \ \__\ __/  / /                  \ \_______\ \_______\ \_______\ \__\ \__\ \__\ \__\   \ \__\
    \|__||\___/ /                    \|_______|\|_______|\|_______|\|__|\|__|\|__|\|__|    \|__|
         \|___|/                                                                                
python-lechat-php-suite																created 2021



BASIC DESCRIPTION
		terminal interface for LeChat-php websites
	includes client and bot modes, for manual or automated reading and posting
<>



USAGE

	BASIC
		to initialize the full package, launch with run.py or kernel.py
	
	this client is multithreaded-capable, and can run all modules in one process
	the kernel will launch the Client, and from the client you can launch other
	modules individually (explained further in FILES section of this doc), such as:
	
	/start keepalive
	
	or you can launch all side threads at once, with:
	
	/start all
	
	some modules are able to run independently, these include:
	
	keepalive
	client
	
	other modules require others to run, in order to fully function:
	
	listener
	log_chat
	log_names
	
	ADVANCED
		there are currently plans for implementing classes, for multiple instances,
	using a session queue for creating logins and assigning virtual sessions. this
	mode would necessitate some changes, such as unification across sessions of log
	handling, and only reading sessions from a queue instead of the sessionfile
	
	
<>



MODES
	
	STANDALONE
		Standalone mode works with some modules, allowing them to run in separate processes.
	some modules requires others to be running, for full functionality, in threaded mode.
	if launched in standalone mode, however, these will perform necessary additional tasks.
	For example, log_chat in threaded mode requires listener to be running, but not when in
	standalone mode. this is because in threaded mode, listener provides a unified GET source
	for fetching data from the server, in order to reduce traffic and normalize requests made.
	
	FULLY THREADED
		Fully Threaded mode combines all of the functions into a unified process. This allows
	launching keepalive, responder, and log threads all from the same terminal as your client.
	This mode starts with only the client running, and allows you to choose what other modules
	to start. typing "/help threads" in client will give information about side-threads.
<>



FILES

	file structure and descriptions:


	/	-	-	-	-	- root directory
	
	/data/names/	-	-	- names directory, for files containing random names
	/data/names/*	-	-	- default/testing namefiles, not hardcoded
	
	/data/posts/	-	-	- posts directory, for files containing random posts
	/data/posts/*	-	-	- default/testing postfiles, currently hardcoded into extra.py's random_post
	
	/data/external_proxy	- (change this to /data/user_config and add extra data,
								instead of using config.py, and put core config back into main.py)
	/data/log.txt	-	-	- chat log file, created by log_chat.py
	/data/nicknames.txt	-	- names log file, created by log_names.py
	/data/pagefile	-	-	- temporary pagefile, stores one page at a time
	/data/session	-	-	- sessionfile, stores one session at a time
	
	/_readme.txt	-	-	- this file
	/capsolver.py	-	-	- solves basic and intermediate captchas (not yet advanced)
								credits to @ninja at dan's chat for this captcha solving method
	/chat_data.py	-	-	- stores data from the chat (timezones, colors, languages, etc)
	/client.py	-	-	-	- * terminal user interface
	/config.py	-	-	-	- stores user and core configurations, will be moved to main.py and /data/user_config
	/extra.py	-	-	-	- nonessential functionality, such as random name/password/messages
	/keepalive.py	-	-	- * gives options for wait_time, message, and recipient. then posts on a timer
	/kernel.py	-	-	-	- ** launches fully threaded mode
	/listener.py	-	-	- * performs GET requests to the server, and updates the pagefile
	/log_chat.py	-	-	- * listens to the pagefile and keeps a running log of the chat (requires listener)
	/log_names.py	-	-	- * listens to the pagefile and keeps track of unique usernames (requires listener)
	/login.py	-	-	-	- * creates a new session, logging into chat
	/main.py	-	-	-	- contains the majority of core functionality
	/responder.py	-	-	- * listens to the log or pagefile and responds to preconfigured stimuli
	/run.py		-	-	-	- ** launches fully threaded mode
	/test.py		-	-	- * used for testing new or modified functions
	
	(* modules marked with a star can be launched in standalone mode)
	(** opening kernel.py, or run.py, will both start() fully-threaded mode)
<>



ROADMAP

got to use BS4 better, like for finding values in the post frame.
should be able to find exact nc, postid, etc - using BS4 wisely, instead of random [shit]

make all loggers use hostname subdir inside of /data/
subdirs could be used to separate sessions also.
instead of using single session file, use sessions folder, inside hostname subdir

make thread test with 5 different threads A-E, start each one and end them using replica of Kernel
for checking if the model of starting and joining works, with abortsignal, etc

fix support for proxy mode, using python's socks5 through tor ports
so connection methods / requests can use proxy if configured to

almost have scripts working independently, so only interconnection will be a problem
log_pubnotes now works, still need to update google
log_chat works pretty well now
responder almost worked, pretty sure it was having issues with POSTing
login works fine, but could use multi-session update
keepalive worked
should check all core functions in main.py etc, to make sure they are solid
have not tested client



<>



###############################
# End of file