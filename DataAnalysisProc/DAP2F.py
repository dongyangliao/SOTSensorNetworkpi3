import json
import os
import urllib2
import requests
import commands
import time
import sys
import subprocess
import datetime

checkallowed = 0
# DataQueue is the signal msg from the Thingspeak plugin
path="./DataQueue2f"
# log path
logpath="./Update2f.log"
# web url
localweb= 'http://localhost:3000/'
# updatelogpath
updatelogpath= "./datacheck/"
# inteval time
timeintev = 50   # about 20 s

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

# delete all data in a file(fd)
def deleteContent(fd):
	fd.seek(0)
	fd.truncate()
	pass

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

def getChannel2(msignal):
	sigsp = msignal.split(",")
	channel2 = sigsp[4]
	return channel2
	pass

def getField2(msignal):
	sigsp = msignal.split(",")
	field2 = sigsp[5]
	return field2
	pass

def signalCheck(msignal):
	# One channel check
	if len(msignal.split(",")) >= 4:
		channel = getChannel(msignal)
		field = getField(msignal)
		method = getMethod(msignal)
		results = getResult(msignal)
		channel2 = getChannel2(msignal)
		field2 = getField2(msignal)
		field2_e = field2[0]
		#print channel,field,method,results
		
		# type error check
		if((not is_number(channel)) or (not is_number(field)) or (not is_number(method)) or (not is_number(results)) or (not is_number(channel2)) or (not is_number(field2_e))):
			return 0
		
		# link check 
		checkurl = localweb+"channels/"+channel+"/fields/"+field+".json?results=1"
		rcheck = requests.get(checkurl)
		checkurl11 = localweb+"channels/" + channel2 + "/fields/" + field2_e + ".json?results=1"
		rcheck11 = requests.get(checkurl11)
		#print rcheck.status_code
		if rcheck.status_code == 404 or rcheck.status_code == 400 or rcheck11.status_code == 404 or rcheck11.status_code == 400:
			return 0
	
	print "signal check OK"
	print channel,field,method,results
	return 1
	pass

def jsonload(msignal):
	
	channel = getChannel(msignal)
	field = getField(msignal)
	field2_e = field2[0]
	checkurl2 = localweb+"channels/"+channel+"/feed/last.json"
	rcheck2 = urllib2.Request(checkurl2)
	res2 = urllib2.urlopen(rcheck2)
	
	res2 = res2.read()
	resj = json.loads(res2)
	return resj
	pass

def jsonload2(msignal):
	
	channel = getChannel2(msignal)
	field = getField2(msignal)
	
	checkurl2 = localweb+"channels/"+channel+"/feed/last.json"
	rcheck2 = urllib2.Request(checkurl2)
	res2 = urllib2.urlopen(rcheck2)
	
	res2 = res2.read()
	resj = json.loads(res2)
	return resj
	pass

def updateLogFileCheck(msignal,jsonwebdata, jsonwebdata2):
	channel= getChannel(msignal)
	field = getField(msignal)
	
	channel2= getChannel2(msignal)
	field2 = getField2(msignal)
	field2_e = field2[0]
	filerecent = updatelogpath+"C"+channel+"F"+field+"C"+channel2+"F"+field2_e+".txt"
	if os.path.exists(filerecent):
		print "updateLogFileCheck OK"
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
		if jsonwebdata2.has_key(Field): 
			createdDate2 = jsonwebdata2["created_at"]
			lastData2 = jsonwebdata2[Field]
			print createdDate,lastData
			pass
		else:
			return -1
			pass
		method=getMethod(msignal)
		results=getResult(msignal)
		dn = datetime.datetime.now()
		print dn
		fdrecent = open(filerecent, "w")
		datawritetxt = lastData+","+createdDate+","+method+","+results+","+lastData2+","+createdDate2+","+str(dn)
		print datawritetxt
		fdrecent.write(datawritetxt)
		fdrecent.close()
		return 0
	pass

# time check
def timeCheck(msignal):
	# in folder timecheck
	print "time check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	channel2= getChannel2(msignal)
	field2 = getField2(msignal)
	field2_e = field2[0]
	filerecent = updatelogpath+"C"+channel+"F"+field+"C"+channel2+"F"+field2_e+".txt"
	if os.path.exists(filerecent):
		fdrecent = open(filerecent,"r")
		fdrecenttxt = fdrecent.read()
		fdrecenttxtsplit = fdrecenttxt.split(",")
		fdrecent.close()
		dnn = datetime.datetime.now();
		strdate = datetime.datetime.strptime(fdrecenttxtsplit[6],'%Y-%m-%d %H:%M:%S.%f')
		timeoutexist = (dnn - strdate).seconds
		print timeoutexist
		if timeoutexist > timeintev:
			print "time out"
			return 1
	
	return 0
	pass

def lognewchange(jsonwebdata,msignal,jsonwebdata2):
	channel= getChannel(msignal)
	field = getField(msignal)
	Field = "field"+field
	channel2= getChannel2(msignal)
	field2 = getField2(msignal)
	field2_e = field2[0]
	Field22 = "field"+field2_e
	if jsonwebdata.has_key(Field) and jsonwebdata2.has_key(Field22) :
		lastData = jsonwebdata[Field]
		createdDate = jsonwebdata["created_at"]
		lastData2 = jsonwebdata2[Field22]
		createdDate2 = jsonwebdata2["created_at"]
		filerecent = updatelogpath+"C"+channel+"F"+field+"C"+channel2+"F"+field2_e+".txt"
		if os.path.exists(filerecent):
			fdrecent = open(filerecent, "w")
			method = getMethod(msignal)
			results = getResult(msignal)
			dn = datetime.datetime.now()
			datawritetxt = lastData+","+createdDate+","+method+","+results+","+lastData2+","+createdDate2+","+str(dn)
			print datawritetxt
			fdrecent.write(datawritetxt)
			fdrecent.close()
	pass

def datecheck(jsonwebdata,msignal,jsonwebdata2):
	#jsonload(msignal)
	print "date check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	Field = "field"+field
	channel2= getChannel2(msignal)
	field2 = getField2(msignal)
	field2_e = field2[0]
	Field22 = "field"+field2_e
	if jsonwebdata.has_key(Field) and jsonwebdata2.has_key(Field22):
		DateC = jsonwebdata["created_at"]
		DateC2 = jsonwebdata["created_at"]
		filerecent = updatelogpath+"C"+channel+"F"+field+"C"+channel2+"F"+field2_e+".txt"
		if os.path.exists(filerecent):
			fdrecent = open(filerecent,"r")
			fdrecenttxt = fdrecent.read()
			fdrecenttxtsplit = fdrecenttxt.split(",")
			fdrecent.close()
			print DateC
			print fdrecenttxtsplit[1]
			if fdrecenttxtsplit[1] != DateC or fdrecenttxtsplit[5] != DateC2:
				return 1
	
	return 0
	pass

def datacheck(jsonwebdata,msignal,jsonwebdata2):
	print "data check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	Field = "field"+field
	channel2= getChannel2(msignal)
	field2 = getField2(msignal)
	field2_e = field2[0]
	Field22 = "field"+field2_e
	if jsonwebdata.has_key(Field) and jsonwebdata2.has_key(Field22):
		lastData = jsonwebdata[Field]
		lastData2 = jsonwebdata2[Field22]
		filerecent = updatelogpath+"C"+channel+"F"+field+"C"+channel2+"F"+field2_e+".txt"
		if os.path.exists(filerecent):
			fdrecent = open(filerecent,"r")
			fdrecenttxt = fdrecent.read()
			fdrecenttxtsplit = fdrecenttxt.split(",")
			fdrecent.close()
			print lastData
			print fdrecenttxtsplit[0]
			if fdrecenttxtsplit[0] != lastData or lastData2 != fdrecenttxtsplit[4]:
				return 1
				
	return 0
	pass

def methodcheck(jsonwebdata,msignal):
	print "method check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	channel2= getChannel2(msignal)
	field2 = getField2(msignal)
	field2_e = field2[0]
	filerecent = updatelogpath+"C"+channel+"F"+field+"C"+channel2+"F"+field2_e+".txt"
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
	print "result check start"
	channel= getChannel(msignal)
	field = getField(msignal)
	channel2= getChannel2(msignal)
	field2 = getField2(msignal)
	field2_e = field2[0]
	filerecent = updatelogpath+"C"+channel+"F"+field+"C"+channel2+"F"+field2_e+".txt"
	if os.path.exists(filerecent):
		fdrecent = open(filerecent,"r")
		fdrecenttxt = fdrecent.read()
		fdrecenttxtsplit = fdrecenttxt.split(",")
		fdrecent.close()
		if fdrecenttxtsplit[3] != getResult(msignal):
			return 1
	
	return 0
	pass

def execMM2(msignal):
	#log
	print "log process" 
	updatelog= open(logpath,"a")
	channel=getChannel(msignal)
	field = getField(msignal)
	method = getMethod(msignal)
	results = getResult(msignal)
	channel2=getChannel2(msignal)
	field2 = getField2(msignal)
	field2_e = field2[0]
	datalog= "Update T:"+ time.asctime(time.localtime(time.time()))+ " C:"+ channel+" F:"+ field + "C:"+ channel2 + "F:" + field2_e + " M:" + method +" R:" + results +"\n"
	updatelog.write(datalog)
	updatelog.close()
	
	#exec
	print "run data analsys in MM"
	CFMM=open('./ChannelAndField2f',"w")
	cfr = channel+","+field+","+method+","+results
	#print cfr
	CFMM.write(cfr)
	CFMM.close()
	
	if method == "1":
		print "method 1"
		subprocess.Popen('wolfram < ./2Method1LF.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
		pass
	
	if method == "2":
		print "method 2"
		#subprocess.Popen('wolfram < ./Method2F.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
		pass
	
	pass

def DAP2F():
	Y=1
	while(Y):
		Y=Y-1
		MMperm = MMstate(0)
		if os.stat(path).st_size == 0:  
			#print "No data in array"
			pass
		else:
			fd = open(path, 'r+')  # exist!
			allsignal = fd.readlines()
			#deleteContent(fd)
			for msignal in allsignal:
				if len(msignal.split(",")) >= 6 and signalCheck(msignal):
					jsonwebdata = jsonload(msignal)
					jsonwebdata2 = jsonload2(msignal)
					if updateLogFileCheck(msignal,jsonwebdata,jsonwebdata2):
						
						if datecheck(jsonwebdata,msignal,jsonwebdata2) or datacheck(jsonwebdata,msignal,jsonwebdata2) or methodcheck(jsonwebdata,msignal) or resultscheck(jsonwebdata,msignal):
							lognewchange(jsonwebdata,msignal,jsonwebdata2)
							MMperm.setallowed()
							pass
						
						if timeCheck(msignal):
							lognewchange(jsonwebdata,msignal,jsonwebdata2)
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
						execMM2(msignal)
						
						MMperm.setdisalowed()
						pass
					
				pass
			pass
		pass
	pass


# daemon process 
if __name__ == '__main__':
	DAP2F()
