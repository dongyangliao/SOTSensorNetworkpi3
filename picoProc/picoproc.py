import io
import os
import csv
import urllib3
import shutil
from time import sleep

opath="/home/pi/picof"
movepath="/var/www/html/picoProc/old"

def pico(filerow):
    f = io.open(filerow, 'r',encoding="utf-8_sig")
    reader = csv.reader(f)
    rdlist = list(reader)
	#print(len(rdlist))
    Selectindex = 0
    StdC = 0
    for rowindex in range(len(rdlist)):
        try:
            if rdlist[rowindex][0] == "Selected:B":
            #print(rowindex)
                Selectindex = rowindex
            if rdlist[rowindex][0] == "StandardCurve":
            #print(rowindex)
                StdC = rowindex
        except IndexError:
            pass

    Rindex = Selectindex + 2
    SEndindex = StdC - 1
    Onenum = (SEndindex - Rindex)/3
    Onenumi = int(Onenum)
    #print(Rindex) #print(SEndindex) #print(Onenumi)
    http = urllib3.PoolManager()

    for i in range(Onenumi):
        # check the data or out of range
        if rdlist[Rindex][5] == "":
            #print("kong")
            rdlist[Rindex][5] = "0"
        if rdlist[Rindex][6] == "":
            #print("kong")
            rdlist[Rindex][6] = "0"

        r = http.request('GET', 'http://localhost:3000/update?key=LECO1UNUU9Y86N9P&field2=' + \
                     rdlist[Rindex+i][5] + '&field3='+rdlist[Rindex+Onenumi+i][5]+'&field4='+rdlist[Rindex+Onenumi+Onenumi+i][5] \
                     +'&field5='+rdlist[Rindex+i][6] + '&field6='+rdlist[Rindex+Onenumi+i][6]+'&field7='+rdlist[Rindex+Onenumi+Onenumi+i][6] + '')
        sleep(0.5)
        pass


def folderexist(opath):
	if os.path.exists(opath):
		pass
	else:
		os.mkdir(opath)
		os.chmod(opath, 755)
		pass
	pass

def scanfilewitharg(fstr):
	filelist = []
	for root, dirs, files in os.walk(fstr):
		for file in files:
			#print file
			#p = file
			#absp = os.path.abspath(p)
			p=os.path.join(root,file)
			#print p
			#print os.path.abspath(p)
			filelist.append(p)
			
	return filelist
	pass

def movefile(frow):
	mpath = os.path.join(movepath,os.path.basename(frow))
	shutil.move(frow,mpath)
	pass

def picostd():
	#Y=1
	while 1:
		#Y = Y-1
		folderexist(opath)
		flist = scanfilewitharg(opath)
		for frow in flist:
			pico(frow)
			movefile(frow)
			pass
	sleep(6)
	pass


if __name__ == '__main__':
    picostd()
