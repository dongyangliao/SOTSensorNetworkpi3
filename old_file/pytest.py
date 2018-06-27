import subprocess, time,commands
#from subprocess import call

def timetest():
	start = time.time()
	print "start"
	#p=subprocess.Popen('wolfram < LOTtestforT.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
	p=subprocess.Popen('wolfram < ./dispimage/Method1F.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
	#(status, outp)=commands.getstatusoutput('wolfram < ./dispimage/Method1F.m')
	#print outp
	p.communicate()
	print "end"
	#timeforrun = (time.clock() - start)
	end = time.time()
	print end-start
	runtime = end -start
	f = open('./Method1RunTime.txt','a')
	f.write(str(runtime) + '\n')
	f.close()

for i in range(0,48):
	timetest()
#print("Time used :" + str(timeforrun) + "sec") 

#call(['wolfram','-script', 'LOTtestbyliao2.m'])
