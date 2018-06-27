import multiprocessing
import time
import os
import logging 

glbfp = "/var/www/html/dispimage/"

targetlist = []
intervaltime = 10*60

def recheck(filepath):
	if filepath[-2:-1] == '/':
		return True
	else:
		return False 
	pass

def scanfilewitharg(fstr):
	list = os.listdir(fstr)
	tlist = []
	for line in list:
		filepath = os.path.join(fstr,line)
		if os.path.isdir(filepath) and recheck(filepath):			
			tlist.append(filepath)
	return tlist
	pass

def deletefolder(tlist):
	for line in tlist:
		os.chmod(line,0777)
		__import__('shutil').rmtree(line)
	pass
			

def log():
	logging.basicConfig(filename='rtproc.log', level=logging.DEBUG)
	logging.info("Proc Doing in {0}".format(time.ctime()))
	pass

def worker(interval):
	print "The process start %s" %time.ctime()
	
	while True:
		print "doki doki %s" %time.ctime()
		targetlist=scanfilewitharg(glbfp)
		print targetlist
		if targetlist:
			deletefolder(targetlist)
			log()
		
		time.sleep(interval)
		pass


if __name__ == "__main__":
	# Time is args
	p = multiprocessing.Process(target= worker, args = (intervaltime,))
	p.name = "delete routime"
	#p.daemon = True
	p.start()
	print "p.pid:", p.pid
	print "p.name is ", p.name
	print "p.is_alive", p.is_alive()
