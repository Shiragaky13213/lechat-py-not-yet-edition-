#!python3
# -*- coding: utf-8 -*-
########################################
# test.py
# used for testing new or modified functions
# 



from bs4 import BeautifulSoup
 


#
def test():
	test = u"Hägar"
	print(str(test))
	print(str(test.encode()))
	print(test.encode('utf-8').decode())
#


	def fix_multiline(prevlog):
		i=0
		tofix=[]
		Fixed = []
		line=''
		while(i<len(prevlog)):
			line=prevlog[i]
			if(line != ''):
				if(line[0]=='✪'):
					pass
				elif(line[0]==MSG_START.decode()[0]):
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
		return prevlog
#
if __name__ == "__main__":
	#
	test()
	#
#



###############################
# End of file