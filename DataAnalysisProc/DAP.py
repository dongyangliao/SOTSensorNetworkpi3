
import json
import os
import urllib2
import requests
import commands
import time
import sys
import subprocess
import datetime
from Queue import Queue
#import threading

checkallowed = 0
# DataQueue is the signal msg from the Thingspeak plugin
path="./DataQueue"
# log path
logpath="./Update.log"
# web url
localweb= 'http://localhost:3000/'
# updatelogpath
updatelogpath= "./datacheck/"
# inteval time
timeintev = 60   # about 20 s


class MMstate:
	
	def __init__(self, checkallowed):
		self.checkallowed = checkallowed
	
	def getMMstate(self):
		print self.checkallowed
		if self.checkallowed == 1:
			return 1
		else:
			return 0
		pass
	
	def setallowed(self):
		self.checkallowed = 1
	pass
	
	def setdisalowed(self):
		self.checkallowed = 0
	pass
	

class FIFOstate:
	def __init__(self, checkallowed):
		self.checkallowed = checkallowed
		self.q = Queue()
	
	def selfput(data):
		self.q.put(data)
	
	def selfget(data):
		self.q.get(data)
	
	pass

#fifo = FIFOstate(1)

def setdisalowed():
	checkallowed = 0
	pass

def folderExisted():
	if os.path.exists(updatelogpath):
		pass
	else:
		os.mkdir(updatelogpath)
		os.chmod(updatelogpath, 755)
		pass
	pass

# delete all data in a file(fd)
def deleteContent(fd):
	fd.seek(0)
	fd.truncate()
	pass

# check the string is a number?. 
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		pass
	
	try:
		import unicodedata
		unicodedata.numeric(s)
		return True
	except (TypeError, ValueError):
		pass
	
	return False

#
def getChannel(msignal):
	sigsp = msignal.split(",")
	channel = sigsp[0]
	return channel
	pass

#
def getField(msignal):
	sigsp = msignal.split(",")
	field = sigsp[1]
	return field
	pass

#
def getMethod(msignal):
	sigsp = msignal.split(",")
	method = sigsp[2]
	return method
	pass

#
def getResult(msignal):
	sigsp = msignal.split(",")
	results = sigsp[3]
	return results
	pass

# exec the Mathematica file in one channel.


# Check the signal error and exist. return 1 is no problem
def signalCheck(msignal):
	# One channel check
	if len(msignal.split(",")) >= 4:
		channel = getChannel(msignal)
		field = getField(msignal)
		method = getMethod(msignal)
		results = getResult(msignal)
		#print channel,field,method,results
		
		# type error check
		if((not is_number(channel)) or (not is_number(field)) or (not is_number(method)) or (not is_number(results))):
			return 0
		
		# link check 
		checkurl = localweb+"channels/"+channel+"/fields/"+field+".json?results=1"
		rcheck = requests.get(checkurl)
		#print rcheck.status_code
		if rcheck.status_code == 404 or rcheck.status_code == 400:
			return 0
	
	#print "signal check OK"
	print channel,field,method,results
	return 1
	pass

def jsonload(msignal):
	
	channel = getChannel(msignal)
	field = getField(msignal)
	
	checkurl2 = localweb+"channels/"+channel+"/feed/last.json"
	rcheck2 = urllib2.Request(checkurl2)
	res2 = urllib2.urlopen(rcheck2)
	
	res2 = res2.read()
	resj = json.loads(res2)
	return resj
	# no need
	#print resj
	#Field = "field"+field
	#if resj.has_key(Field): 
	#	print "OK"
	
	pass

def updateLogFileCheck(msignal,jsonwebdata):
	channel= getChannel(msignal)
	field = getField(msignal)
	
	filerecent = updatelogpath+"C"+channel+"F"+field+".txt"
	if os.path.exists(filerecent):
		#print "updateLogFileCheck OK"
		return 1
	else:
		print "No, Create it and write into file"
		Field = "field"+field
		if jsonwebdata.has_key(Field): 
			createdDate = jsonwebdata["created_at"]
			lastData = jsonwebdata[Field]
			print createdDate,lastData
			pass
		else:
			return -1
			pass
		method=getMethod(msignal)
		results=getResult(msignal)
		dn = datetime.datetime.now()
		#print dn
		fdrecent = open(filerecent, "w")
		datawritetxt = lastData+","+createdDate+","+method+","+results+","+str(dn)
		#print datawritetxt
		fdrecent.write(datawritetxt)
		fdrecent.close()
		return 0
	pass

#
#  format: lastData+","+createdDate+","+method+","+results+","+str(dn)
#

def datecheck(jsonwebdata,msignal):
	#jsonload(msignal)
	#print "date check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	Field = "field"+field
	if jsonwebdata.has_key(Field):
		DateC = jsonwebdata["created_at"]
		filerecent = updatelogpath+"C"+channel+"F"+field+".txt"
		if os.path.exists(filerecent):
			fdrecent = open(filerecent,"r")
			fdrecenttxt = fdrecent.read()
			fdrecenttxtsplit = fdrecenttxt.split(",")
			fdrecent.close()
			#print DateC
			#print fdrecenttxtsplit[1]
			if fdrecenttxtsplit[1] != DateC:
				return 1
	
	return 0
	pass

def datacheck(jsonwebdata,msignal):
	#print "data check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	Field = "field"+field
	if jsonwebdata.has_key(Field):
		lastData = jsonwebdata[Field]
		filerecent = updatelogpath+"C"+channel+"F"+field+".txt"
		if os.path.exists(filerecent):
			fdrecent = open(filerecent,"r")
			fdrecenttxt = fdrecent.read()
			fdrecenttxtsplit = fdrecenttxt.split(",")
			fdrecent.close()
			#print lastData
			#print fdrecenttxtsplit[0]
			if fdrecenttxtsplit[0] != lastData:
				return 1
				
	return 0
	pass

def methodcheck(jsonwebdata,msignal):
	#print "method check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	filerecent = updatelogpath+"C"+channel+"F"+field+".txt"
	if os.path.exists(filerecent):
		fdrecent = open(filerecent,"r")
		fdrecenttxt = fdrecent.read()
		fdrecenttxtsplit = fdrecenttxt.split(",")
		fdrecent.close() 
		if fdrecenttxtsplit[2] != getMethod(msignal):
			return 1
	
	return 0
	pass

def resultscheck(jsonwebdata,msignal):
	#print "result check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	filerecent = updatelogpath+"C"+channel+"F"+field+".txt"
	if os.path.exists(filerecent):
		fdrecent = open(filerecent,"r")
		fdrecenttxt = fdrecent.read()
		fdrecenttxtsplit = fdrecenttxt.split(",")
		fdrecent.close()
		if fdrecenttxtsplit[3] != getResult(msignal):
			return 1
	
	return 0
	pass

def lognewchange(jsonwebdata,msignal):
	channel= getChannel(msignal)
	field = getField(msignal)
	Field = "field"+field
	if jsonwebdata.has_key(Field):
		lastData = jsonwebdata[Field]
		createdDate = jsonwebdata["created_at"]
		filerecent = updatelogpath+"C"+channel+"F"+field+".txt"
		if os.path.exists(filerecent):
			fdrecent = open(filerecent, "w")
			method = getMethod(msignal)
			results = getResult(msignal)
			dn = datetime.datetime.now()
			datawritetxt = lastData+","+createdDate+","+method+","+results+","+str(dn)
			#print datawritetxt
			fdrecent.write(datawritetxt)
			fdrecent.close()
	pass


# time check
def timeCheck(msignal):
	# in folder timecheck
	#print "time check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	filerecent = updatelogpath+"C"+channel+"F"+field+".txt"
	if os.path.exists(filerecent):
		fdrecent = open(filerecent,"r")
		fdrecenttxt = fdrecent.read()
		fdrecenttxtsplit = fdrecenttxt.split(",")
		fdrecent.close()
		dnn = datetime.datetime.now();
		strdate = datetime.datetime.strptime(fdrecenttxtsplit[4],'%Y-%m-%d %H:%M:%S.%f')
		timeoutexist = (dnn - strdate).seconds
		print timeoutexist
		if timeoutexist > timeintev:
			print "time out"
			return 1
	
	return 0
	pass

def execMM(msignal):
	#log
	#print "MM process" 
	updatelog= open(logpath,"a")
	channel=getChannel(msignal)
	field = getField(msignal)
	method = getMethod(msignal)
	results = getResult(msignal)
	datalog= "Update T:"+ time.asctime(time.localtime(time.time()))+ " C:"+ channel+" F:"+ field + " M:" + method +" R:" + results +"\n"
	updatelog.write(datalog)
	updatelog.close()
	
	#exec
	#print "FIFO queue in MM"
	CFMM=open('./ChannelAndField',"w")
	cfr = channel+","+field+","+method+","+results
	print cfr
	CFMM.write(cfr)
	CFMM.close()
	
	print("Put one")
	if method == "1":
		print "method 1"
		subprocess.Popen('wolfram < ./Method1F.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
		pass
	
	if method == "2":
		print "method 2"
		subprocess.Popen('wolfram < ./Method2F.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
		pass
	
	pass
	if method == "3":
                print "method 3"
                subprocess.Popen('wolfram < ./Method3F.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close$
                pass

        pass
	if method == "4":
                print "method 4"
                subprocess.Popen('wolfram < ./Method4F.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close$
                pass

        pass

# main process
# Signal type(one channel): channel,field,method,result,\n (e.g. 5,1,1,100,\n)
# Signal type(two channel): waiting...
#

def DAP():
	Y=1
	while Y:
		folderExisted()
		MMperm = MMstate(0)
		#......................Check the DataQueue data exist?
		if os.stat(path).st_size == 0:  
			#print "No data in array"
			pass
		else:
		#.......................signal array exist!
			fd = open(path, 'r+')  # exist!
			allsignal = fd.readlines()
			#.........................delete the current signal after read out 
			deleteContent(fd)
			# loop it
			for msignal in allsignal:
				#  This is the demand for the one channel and two channel
				#  Yes is two , NO is one
				#
				# two channel
				if len(msignal.split(",")) >= 7:
					pass
				
				# one channel
				else:
					if signalCheck(msignal):
						jsonwebdata = jsonload(msignal)
						if updateLogFileCheck(msignal,jsonwebdata):
							#jsonwebdata = jsonload(msignal)
							#print jsonwebdata
							if datecheck(jsonwebdata,msignal) or datacheck(jsonwebdata,msignal) or methodcheck(jsonwebdata,msignal) or resultscheck(jsonwebdata,msignal):
								lognewchange(jsonwebdata,msignal)
								MMperm.setallowed()
								pass
							
							if timeCheck(msignal):
								lognewchange(jsonwebdata,msignal)
								MMperm.setallowed()
								pass
							pass
						else:
							print "first in"
							MMperm.setallowed()
							pass
						
						# MM
						if MMperm.getMMstate():
							print "permission OK"
							execMM(msignal)
							
							MMperm.setdisalowed()
							pass
						pass
					pass
				
				
			pass
	pass



# daemon process 
if __name__ == '__main__':
	DAP()







