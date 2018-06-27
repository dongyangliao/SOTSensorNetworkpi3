import subprocess
#from subprocess import call
print "start"
p=subprocess.Popen('wolfram < LOTtestforT.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
p.communicate()

print "end"


#call(['wolfram','-script', 'LOTtestbyliao2.m'])
