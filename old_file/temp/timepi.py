from time import ctime,sleep

def deljob():
	for i in range(2):
		print "I do %s" %ctime()
		sleep(1)
		
def deljob2():
	for i in range(2):
		print "i do 2 %s" %ctime()
		sleep(5)
		
if __name__ == '__main__':
	deljob()
	deljob2()
	print "all over %s" %ctime()
