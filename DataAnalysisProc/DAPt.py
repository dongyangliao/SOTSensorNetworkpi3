import datetime
import json
import os
import threading
import time
import Queue
import urllib2
import requests

#
#   Check the file(-1) and log
#

mmfilesize = 3  # type: int

MMPath = r"C:\Users\liao\Documents\text1.txt"
MMrealPath = './ChannelAndField'
#
checkallowed = 0
# DataQueue is the signal msg from the Thingspeak plugin
path = "./DataQueue"
# log path
logpath = "./Update.log"
# web url
localweb = 'http://localhost:3000/'
# updatelogpath
updatelogpath = "./datacheck/"
# inteval time
timeintev = 60  # about 20 s

#
#  signalQ is a queue maintain the signal which need to compute in mathematica(MM)
#
signalQ = Queue.LifoQueue()


#
#  check the signal is the first time?
#
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
	



#
#  check folder existed ?
#
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


#
#   Two channel is not finished
#

# Check the signal error and exist. return 1 is no problem
#
#  if Ok, return 1
#  else return 0
#
def signalCheck(msignal):
	# One channel check
	if len(msignal.split(",")) >= 4:
		channel = getChannel(msignal)
		field = getField(msignal)
		method = getMethod(msignal)
		results = getResult(msignal)
		# print channel,field,method,results
		
		if channel == '0' or field == '0' or method == '0' or results == '0':
			return 0
		
		# type error check
		if ((not is_number(channel)) or (not is_number(field)) or (not is_number(method)) or (not is_number(results))):
			return 0

		# link check
		checkurl = localweb + "channels/" + channel + "/fields/" + field + ".json?results=1"
		rcheck = requests.get(checkurl)
		# print rcheck.status_code
		if rcheck.status_code == 404 or rcheck.status_code == 400:
			return 0

	# print "signal check OK"
	print channel, field, method, results
	return 1
	
#
# the raw json type to interpretable json
# return json type data
# it can use resj.subarray 
#
def jsonload(msignal):
    channel = getChannel(msignal)
    field = getField(msignal)

    checkurl2 = localweb + "channels/" + channel + "/feed/last.json"
    rcheck2 = urllib2.Request(checkurl2)
    res2 = urllib2.urlopen(rcheck2)

    res2 = res2.read()
    resj = json.loads(res2)
    return resj
    # no need
    # print resj
    # Field = "field"+field
    # if resj.has_key(Field):
    #	print "OK"

    pass

#
# check recent log file exist.
# if existed return 1
# No , first time return 0
# Error return -1
#
def updateLogFileCheck(msignal, jsonwebdata):
    channel = getChannel(msignal)
    field = getField(msignal)

    filerecent = updatelogpath + "C" + channel + "F" + field + ".txt"
    if os.path.exists(filerecent):
        # print "updateLogFileCheck OK"
        return 1
    else:
        print "No, Create it and write into file"
        Field = "field" + field
        if jsonwebdata.has_key(Field):
            createdDate = jsonwebdata["created_at"]
            lastData = jsonwebdata[Field]
            print createdDate, lastData
            #if lastData == None or lastData == "":
			#	return -1
            #pass
        else:
            return -1
            pass
        #method = getMethod(msignal)
        #results = getResult(msignal)
        #dn = datetime.datetime.now()
        # print dn
        #fdrecent = open(filerecent, "w")
        #datawritetxt = lastData + "," + createdDate + "," + method + "," + results + "," + str(dn)
        # print datawritetxt
        #fdrecent.write(datawritetxt)
        #fdrecent.close()
        return 0
    pass


#
#  format: lastData+","+createdDate+","+method+","+results+","+str(dn)
#
#
#  date check
#  if success return 1
#
def datecheck(jsonwebdata, msignal):
	# jsonload(msignal)
	# print "date check start"
	channel = getChannel(msignal)
	field = getField(msignal)
	Field = "field" + field
	if jsonwebdata.has_key(Field):
		DateC = jsonwebdata["created_at"]
		filerecent = updatelogpath + "C" + channel + "F" + field + ".txt"
		if os.path.exists(filerecent):
			fdrecent = open(filerecent, "r")
			fdrecenttxt = fdrecent.read()
			fdrecent.close()
			if len(fdrecenttxt) < 10:
				fdrecent.close()
				return -1

			fdrecenttxtsplit = fdrecenttxt.split(",")
			if fdrecenttxtsplit[1] != DateC:
				return 1
	return 0

#
#  data check
#  if success return 1
#
def datacheck(jsonwebdata, msignal):
	# print "data check start"
	channel = getChannel(msignal)
	field = getField(msignal)
	Field = "field" + field
	if jsonwebdata.has_key(Field):
		lastData = jsonwebdata[Field]
		if lastData == None or lastData == "":
			print("data check false")
			return 0
		filerecent = updatelogpath + "C" + channel + "F" + field + ".txt"
		if os.path.exists(filerecent):
			fdrecent = open(filerecent, "r")
			fdrecenttxt = fdrecent.read()
			if len(fdrecenttxt) < 10:
				fdrecent.close()
				return -1
			fdrecent.close()
			fdrecenttxtsplit = fdrecenttxt.split(",")
			# print lastData
			# print fdrecenttxtsplit[0]
			if fdrecenttxtsplit[0] != lastData:
				return 1
	return 0

#
#  method check
#  if success return 1
#
def methodcheck(jsonwebdata, msignal):
	# print "method check start"
	channel = getChannel(msignal)
	field = getField(msignal)
	filerecent = updatelogpath + "C" + channel + "F" + field + ".txt"
	if os.path.exists(filerecent):
		fdrecent = open(filerecent, "r")
		fdrecenttxt = fdrecent.read()
		fdrecent.close()
		if len(fdrecenttxt) < 10:
			fdrecent.close()
			return -1
		
		fdrecenttxtsplit = fdrecenttxt.split(",")
		if fdrecenttxtsplit[2] != getMethod(msignal):
			return 1
	return 0

#
#  result check
#  if success return 1
#
def resultscheck(jsonwebdata, msignal):
	# print "result check start"
	channel = getChannel(msignal)
	field = getField(msignal)
	filerecent = updatelogpath + "C" + channel + "F" + field + ".txt"
	if os.path.exists(filerecent):
		fdrecent = open(filerecent, "r")
		fdrecenttxt = fdrecent.read()
		fdrecent.close()
		if len(fdrecenttxt) < 10:
			fdrecent.close()
			return -1
		fdrecenttxtsplit = fdrecenttxt.split(",")
		if fdrecenttxtsplit[3] != getResult(msignal):
			return 1
	return 0


#
#  log
#
def lognewchange(jsonwebdata, msignal):
	channel = getChannel(msignal)
	field = getField(msignal)
	Field = "field" + field
	lastData = ""
	if jsonwebdata.has_key(Field):
		lastData = jsonwebdata[Field]
		createdDate = jsonwebdata["created_at"]
		filerecent = updatelogpath + "C" + channel + "F" + field + ".txt"
		if os.path.exists(filerecent):
			fdrecent = open(filerecent, "w")
			method = getMethod(msignal)
			results = getResult(msignal)
			dn = datetime.datetime.now()
			#print lastData
			#print createdDate
			#print 
			if lastData:
				if lastData == None or lastdata == "":
					#lastData = str(1)
					fdrecent.close()
					return -1
			else:
				return -1
			datawritetxt = lastData + "," + createdDate + "," + method + "," + results + "," + str(dn)
			print datawritetxt
			fdrecent.write(datawritetxt)
			fdrecent.close()
			return 0
	return -1


# time check
#
#  if success return 1
#  in folder timecheck
#
def timeCheck(msignal):
	# print "time check start"
	channel = getChannel(msignal)
	field = getField(msignal)
	filerecent = updatelogpath + "C" + channel + "F" + field + ".txt"
	if os.path.exists(filerecent):
		fdrecent = open(filerecent, "r")
		fdrecenttxt = fdrecent.read()
		fdrecenttxtsplit = fdrecenttxt.split(",")
		if len(fdrecenttxt) < 10:
			fdrecent.close()
			return -1
		fdrecent.close()
		dnn = datetime.datetime.now()
		strdate = datetime.datetime.strptime(fdrecenttxtsplit[4], '%Y-%m-%d %H:%M:%S.%f')
		timeoutexist = (dnn - strdate).seconds
		print timeoutexist
		if timeoutexist > timeintev:
			print "time out"
			return 1
	return 0

def logRecentMsgForCompare(jsonwebdata, msignal):
	channel = getChannel(msignal)
	field = getField(msignal)
	method = getMethod(msignal)
	results = getResult(msignal)
	dn = datetime.datetime.now()
	# print dn
	lastData = ""
	createdDate = ""
	Field = "field" + field
	if jsonwebdata.has_key(Field):
		lastData = jsonwebdata[Field]
		createdDate = jsonwebdata["created_at"]
	else:
		return -1
	filerecent = updatelogpath + "C" + channel + "F" + field + ".txt"
	fdrecent = open(filerecent, "w")
	if lastData == None or lastData == "":
		lastData = "1"
	datawritetxt = lastData + "," + createdDate + "," + method + "," + results + "," + str(dn)
	# print datawritetxt
	fdrecent.write(datawritetxt)
	fdrecent.close()
	return 0


#
#   all check in here
#
#
def allcheck(msignal):
	
	# signal check
	sc = signalCheck(msignal)
	if sc == 0:
		print("Log: signal check false")
		return 0
	
	# logfile check first in or have logfile ?
	jsonwebdata = jsonload(msignal)
	ulfc=updateLogFileCheck(msignal, jsonwebdata)
	if ulfc == -1:
		assert ulfc == -1, 'updateLogFileCheck error'
		return 0
	if ulfc == 0:
		print("Log: First time, No need check")
		lrmfc = logRecentMsgForCompare(jsonwebdata, msignal)
		if lrmfc == -1:
			return 0
		return 1
	if ulfc == 1:
		print("Log: Need four check")
	
	# check logfile 
	if datecheck(jsonwebdata, msignal) or datacheck(jsonwebdata, msignal) or methodcheck(jsonwebdata, msignal) or resultscheck(jsonwebdata, msignal):
		print("Four check is ok")
		lrmfc = logRecentMsgForCompare(jsonwebdata, msignal)
		if lrmfc == -1:
			print("Field data is Null")
			return 0
		return 1
	elif datecheck(jsonwebdata, msignal) == -1 or datacheck(jsonwebdata, msignal) == -1 or methodcheck(jsonwebdata, msignal) == -1 or resultscheck(jsonwebdata, msignal) == -1:
		
		lrmfc = logRecentMsgForCompare(jsonwebdata, msignal)
		#lnc = lognewchange(jsonwebdata, msignal)
		if lrmfc == -1:
			return 0
		return 1
	
	# time check ?
	if timeCheck(msignal):
		lrmfc = logRecentMsgForCompare(jsonwebdata, msignal)
		if lrmfc == -1:
			return 0
		print("Time check is ok")
		return 1
		pass



#
#  log before to MM
#
def logbeforemm(mmsignal):
    channel = getChannel(mmsignal)
    field = getField(mmsignal)
    method = getMethod(mmsignal)
    results = getResult(mmsignal)
    # log
    updatelog = open(logpath, "a")
    datalog = "Update T:" + time.asctime(
        time.localtime(time.time())) + " C:" + channel + " F:" + field + " M:" + method + " R:" + results + "\n"
    updatelog.write(datalog)
    updatelog.close()
    pass



#
#  thread 1
#  to get the signal from file and put the right signal to queue
#
def toGetRightSignal():
    while 1:
		# folder exited?
		print(" ")
		print("toGetRightSignal thread: T1")
		folderExisted()
		if os.stat(path).st_size == 0: #  check file have signal ?  else is exited
			print("No existed")
			pass
		else:
			print("open DataQueue")
			fd = open(path, 'r+')
			print("file discripter:", fd.fileno())
			allsignal = fd.readlines()
			deleteContent(fd)   # delete signal which have read
    			for msignal in allsignal:
				#
				#   From here to GotoMM is the check of signal
				#   two channel is NO FINISDED
				#   signal large then 7 is two
				#   else is one
				
				if len(msignal.split(",")) >= 7:
					pass
				else:
					if allcheck(msignal):
						print("sys")
						print(msignal)
						signalQ.put(msignal)   #  put the signal to queue
					else:
						pass
		time.sleep(2)
    
    pass

#
#  thread 2
#  to get the signal from queue and put the signal to MM
#
def toMM():
	while 1:
		print(" ")
		print("toMM thread: T2")
		#print(os.path.getsize(MMrealPath))
		if signalQ.empty():
			print("NO SIGNAL IN QUEUE")
			pass
		elif os.path.getsize(MMrealPath) == mmfilesize:
			mmsignal = signalQ.get()
			logbeforemm(mmsignal)  # log before mm
			channel = getChannel(mmsignal)
			field = getField(mmsignal)
			method = getMethod(mmsignal)
			results = getResult(mmsignal)
			CFMM = open('./ChannelAndField', "w")
			cfr = channel + "," + field + "," + method + "," + results
			print cfr
			CFMM.write(cfr)
			CFMM.close()
			pass
		else:
			print("NOPE3")
			
		time.sleep(2)

#
#  Daemon start.
#
def DAP():
    t1 = threading.Thread(target=toGetRightSignal)
    t2 = threading.Thread(target=toMM)
    t1.start()
    t2.start()

#
# daemon process
#
if __name__ == '__main__':
    DAP()
