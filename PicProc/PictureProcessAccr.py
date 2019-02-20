#!/usr/bin/python

import os,time,shutil,subprocess

wkeyfilesize = 3
MMrealPath = './WKEY'

def Wolfram():
	print "#############wolfram start, wolfram service"
	if os.path.getsize(MMrealPath) == wkeyfilesize:
		CFMM = open('./WKEY', "w")
		cfr = 'RUNMM'
		print cfr
		CFMM.write(cfr)
		CFMM.close()
		return 
	else:
		time.sleep(4)
		
	if os.path.getsize(MMrealPath) == wkeyfilesize:
		CFMM = open('./WKEY', "w")
		cfr = 'RUNMM'
		print cfr
		CFMM.write(cfr)
		CFMM.close()
		return 
	else:
		time.sleep(4)
	
	if os.path.getsize(MMrealPath) == wkeyfilesize:
		CFMM = open('./WKEY', "w")
		cfr = 'RUNMM'
		print cfr
		CFMM.write(cfr)
		CFMM.close()
		return 
	else:
		p = subprocess.Popen('wolfram < LOTtestforT.wl', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
		p.communicate()
	
	print "#############worfram OK"
	pass

def Dcheck():
	if os.path.isdir('./con'):
		pass
	else:
		os.makedirs('./con')
		pass
	
	if os.path.isdir('./sig'):
		pass
	else:
		os.makedirs('./sig')
		pass
	
	if os.path.isdir('./log'):
		pass
	else:
		os.makedirs('./log')
		pass
	
	
	pass

def logdate():
	nowdate = time.strftime("%Y%m%d_%H%M")
	logfiletime = nowdate + "  " + " finished \n"
	
	logingf = open('picproc.log','a')
	logingf.write(logfiletime)
	logingf.close()
    
	nowdataD = './log/'+ nowdate
	if os.path.isdir(nowdataD):
		pass
	else:
		os.makedirs(nowdataD)
		pass
	#print nowdate
	return nowdate
	
	pass

def logf():
	print "############log start"
	while(1):
		if os.path.getsize(MMrealPath) == wkeyfilesize:
			break
		else:
			time.sleep(4)
	
	Ndate = logdate()	
	conlist = []
	conlist = scanfilewitharg('./con/')
	#print conlist
	for i in range(len(conlist)):
		constr = './con/' + conlist[i]
		logpath = os.path.abspath('.') + '/log/' + Ndate
		lognp=os.path.join(logpath,conlist[i])
		#print lognp
		shutil.move(os.path.abspath(constr), lognp)
	
	siglist = []
	siglist = scanfilewitharg('./sig/')
	#print siglist
	for i in range(len(siglist)):
		sigstr = './sig/' + siglist[i]
		logpath = os.path.abspath('.') + '/log/' + Ndate
		lognp=os.path.join(logpath,siglist[i])
		#print lognp
		shutil.move(os.path.abspath(sigstr), lognp)
	print "##############log OK"
	pass

def scanfilewitharg(fstr):
	filelist = []
	for root, dirs, files in os.walk(fstr):
		for file in files:
			#print file
			p = file
			#p=os.path.join(root,file)
			#print p
			#print os.path.abspath(p)
			filelist.append(p)
			
	return filelist
	pass

def scanfile():
	filelist = []
	for root, dirs, files in os.walk('./Cache/'):
		for file in files:
			#print file
			p = file
			#p=os.path.join(root,file)
			#print p
			#print os.path.abspath(p)
			filelist.append(p)
			
	return filelist
	pass
	
def movefile(flist):
	conpath = '/con/'
	sigpath = '/sig/'
	root = './Cache/'
	
	for i in range(len(flist)):
		#print flist[i]
		p=os.path.join(root,flist[i])
		#print os.path.abspath(p)
		#print os.path.abspath('.')
		fstr= flist[i]
		if fstr[17:20] == 'con':
			conabspath = os.path.abspath('.') + conpath
			#print conabspath
			conp=os.path.join(conabspath,flist[i])
			shutil.move(os.path.abspath(p), conp)
			#print conp
		if fstr[17:20] == 'sig':
			sigabspath = os.path.abspath('.') + sigpath
			sigp=os.path.join(sigabspath,flist[i])
			shutil.move(os.path.abspath(p), sigp)
			#print sigp
	pass

def Nextturn():
	print "NEXT TURN"
	Nflist = []
	time.sleep(7)
	Nflist = scanfile()
	print Nflist
	movefile(Nflist)
	print "10"
	
	time.sleep(7)
	Nflist = scanfile()
	print Nflist
	movefile(Nflist)
	print "20"
	
	time.sleep(7)
	Nflist = scanfile()
	print Nflist
	movefile(Nflist)
	print "30"
	
	time.sleep(7)
	Nflist = scanfile()
	print Nflist
	movefile(Nflist)
	print "40"
	
	Wolfram()
	logf()
	
	pass


def PicProc():
	Y=1
	while Y:
		#Y= Y-1
		flist = []
		#Folder exist check.
		Dcheck()

		#print "#############1. Read the file in ./Cache/"
		flist = scanfilewitharg('./Cache/')
		print flist
		#print "#############read OK"
		for i in range(len(flist)):
			fstr= flist[i]
			print fstr[17:20]
			if fstr[17:20] == 'con':
				fck = scanfilewitharg('./Cache/')
				if len(fck) == 0:
					break
				#If con image is found, to next step.
				print "##############2. con file is found, first move"
				movefile(flist)
				print "##############move ok"
				#print "3. Count: 60s count to wait"
				Nextturn()
				pass
		
		time.sleep(10)
		#print "looooop OK"

if __name__ == '__main__':
	PicProc()