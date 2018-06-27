import json
import os
import urllib2
import requests
import commands
import time
import sys
import subprocess

def deleteContent(fd):
    fd.seek(0)
    fd.truncate()
    pass


def execMM(channel,field,method,results):
    # into mathematica
    CFMM=open('./dispimage/ChannelAndField.txt',"w")  #gai
    # write channel and field and results
    cfr = channel+","+field+","+method+","+results
    #print cfr
    CFMM.write(cfr)
    CFMM.close()
    CFMMcheck= open('./dispimage/ChannelAndField.txt',"r")
    print CFMMcheck.read()
    CFMMcheck.close()
    if method == "1":
        print "method 1"
	subprocess.Popen('wolfram < ./dispimage/Method1F.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
	#out, err = p.communicate()
	#print p.returncode
	#(status, output) = commands.getstatusoutput('xvfb-run -a -e /dev/stdout MathematicaScript -script Method1LF.m')
	#os.system('xvfb-run -a -e /dev/stdout --auto-servernum MathematicaScript -script Method1LF.m')
	#print status,output
    if method == "2":
        print "method 2"
        subprocess.Popen('wolfram < ./dispimage/Method2F.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
    if method == "3":
        print "method 3"
    #CFMM.close()
    pass

def exec2MM(channel,field,method,results,channel2,field2):
    # into mathematica
    CFMM=open('./dispimage/ChannelAndField2.txt',"w")  #gai
    # write channel and field and results
    cfr = channel+","+field+","+method+","+results+","+channel2+","+field2
    #print cfr
    CFMM.write(cfr)
    CFMM.close()
    CFMMcheck= open('./dispimage/ChannelAndField2.txt',"r")
    print CFMMcheck.read()
    CFMMcheck.close()
    if method == "1":
        print "method 1"
	subprocess.Popen('xvfb-run -a -e /dev/stdout MathematicaScript -script 2Method1LF.m', stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)  # , close_fds=True)
        #out, err = p.communicate()
	#print p.returncode
	#(status, output) = commands.getstatusoutput('xvfb-run -a -e /dev/stdout MathematicaScript -script 2Method1LF.m')
	#os.system('xvfb-run -a -e /dev/stdout --auto-servernum MathematicaScript -script Method1LF.m')
	#print status,output
    if method == "2":
        print "method 2"
    if method == "3":
        print "method 3"
    #CFMM.close()
    pass


x=1
while x:
    #x=x-1
    path="./dispimage/DataQueue"
    updatepath="./dispimage/Update.log"

    if os.stat(path).st_size == 0:  #gai
            #print "No data in array"
        pass
    else:
        fd = open(path, 'r+')  #gai
        allturn = fd.readlines()
        deleteContent(fd)
        NoType=0
        for turn in allturn:
                #print turn
            turnsp = turn.split(",")
            #4 6
            if len(turnsp) == 4:
                #print "4"
                channel = turnsp[0]
                field = turnsp[1]
                method = turnsp[2]
                results = turnsp[3]
                if channel == "" or field == "" or method == "" or results == "":
            	    NoType = 1
            	    pass
                #print channel,field,method,results
                checkurl = "http://localhost:3000/channels/"+channel+"/fields/"+field+".json?results=1"
                rcheck = requests.get(checkurl)
                #print rcheck
                # check link error
                if NoType == 1 or rcheck.status_code == 404 or rcheck.status_code == 400:
            	    NoType = 0
                    pass
                else: # no link error
                    checkurl2 = "http://localhost:3000/channels/"+channel+"/feed/last.json"
                    rcheck2 = urllib2.Request(checkurl2)
                    res2 = urllib2.urlopen(rcheck2)
                    res2 = res2.read()
                    resj = json.loads(res2)
                    Field = "field"+field
                        # check key error and data exist
                    if resj.has_key(Field): # no key error
                        datacheck = resj[Field]   # the last data
                        datecheck = resj["created_at"]
                        filerecentpath = "./dispimage/C"+channel+"F"+field+".txt"
                        #"./dispimage/C"+channel+"F"+field+".txt"  #gai
                        filerecent = filerecentpath  #gai
                        # check recent file exist?
                        if os.path.exists(filerecent): # existed and open
                            message = 'OK, the "%s" file exists.'
                            fdrecent = open(filerecent,"r")
                            fdrecenttxt = fdrecent.read()
                            fdrecenttxtsplit = fdrecenttxt.split(",")
                            #print fdrecenttxtsplit
                            #print datacheck
                            #print datecheck
                            if datacheck != fdrecenttxtsplit[0]:    # data is not same ?
                                    #print "data update"
                                fdrecent.close()
                                #log
                                updatelog= open(updatepath,"a")
                                datalog= "Data update T:"+ time.asctime(time.localtime(time.time()))+ " C:"+ channel+" F:"+ field + " M:" + method +" R:" + results
                            #print datalog
                                updatelog.write(datalog)
                                updatelog.close()
                                fdrecent = open(filerecent, "w")
                                datawritetxt = datacheck + "," + datecheck + "," + method + "," + results
                                fdrecent.write(datawritetxt)
                                fdrecent.close()
                                execMM(channel,field,method,results)

                            elif datecheck != fdrecenttxtsplit[1]:
                                #print "date update"
                                fdrecent.close()
                                #log
                                updatelog= open(updatepath,"a")
                                datalog= "Date update T:"+ time.asctime(time.localtime(time.time()))+ " C:"+ channel+" F:"+ field + " M:" + method +" R:" + results
                                #print datalog
                                updatelog.write(datalog)
                                updatelog.close()
                                fdrecent = open(filerecent, "w")
                                datawritetxt = datacheck + "," + datecheck + "," + method + "," + results
                                fdrecent.write(datawritetxt)
                                fdrecent.close()
                                execMM(channel,field,method,results)
                            elif method != fdrecenttxtsplit[2]:
                                #print "method change update"
                                fdrecent.close()
                                #log
                                updatelog= open(updatepath,"a")
                                datalog= "Method update T:"+ time.asctime(time.localtime(time.time()))+ " C:"+ channel+" F:"+ field + " M:" + method +" R:" + results
                                #print datalog
                                updatelog.write(datalog)
                                updatelog.close()
                                fdrecent = open(filerecent, "w")
                                datawritetxt = datacheck + "," + datecheck + "," + method + "," + results
                                fdrecent.write(datawritetxt)
                                fdrecent.close()
                                execMM(channel,field,method,results)
                            elif results != fdrecenttxtsplit[3]:
                                #print "result change update"
                                fdrecent.close()
                                #log
                                updatelog= open(updatepath,"a")
                                datalog= "Results update T:"+ time.asctime(time.localtime(time.time()))+ " C:"+ channel+" F:"+ field + " M:" + method +" R:" + results
                                #print datalog
                                updatelog.write(datalog)
                                updatelog.close()
                                fdrecent = open(filerecent, "w")
                                datawritetxt = datacheck + "," + datecheck + "," + method + "," + results
                                fdrecent.write(datawritetxt)
                                fdrecent.close()
                                execMM(channel,field,method,results)

                            else:
                                #print "No exec"
                                pass
                        else: # no existed and create one
                            #log
                            updatelog= open(updatepath,"a")
                            datalog= "New C update T:"+ time.asctime(time.localtime(time.time()))+ " C:"+ channel+" F:"+ field + " M:" + method +" R:" + results
                            #print datalog
                            updatelog.write(datalog)
                            updatelog.close()
                            fdrecent = open(filerecent, "w")
                            # write newest data and time to file
                            datawritetxt = datacheck+","+datecheck+","+method+","+results
                            fdrecent.write(datawritetxt)
                            fdrecent.close()
                            #print "create file and exec"
                            execMM(channel,field,method,results)
                    #fdrecent.close()
                    else:
                        #print "dont have data"
                        pass

            elif len(turnsp) == 6:
                #print "6"
                channel = turnsp[0]
                field = turnsp[1]
                method = turnsp[2]
                results = turnsp[3]
                channel2 = turnsp[4]
                field2 = turnsp[5]
                field2_e = field2[0]
                #print field2_e

                if channel == "" or field == "" or method == "" or results == "" or channel2 == "" or field2_e == "":
                    NoType = 1
                    pass
                checkurl = "http://localhost:3000/channels/"+channel+"/fields/"+field+".json?results=1"
                rcheck = requests.get(checkurl)
                checkurl11 = "http://localhost:3000/channels/" + channel2 + "/fields/" + field2_e + ".json?results=1"
                rcheck11 = requests.get(checkurl11)
                #print rcheck.status_code,rcheck11.status_code
                if NoType == 1 or rcheck.status_code == 404 or rcheck.status_code == 400 or rcheck11.status_code == 400 or rcheck11.status_code == 404:
                    NoType = 0
                    pass
                else:
                    checkurl2 = "http://localhost:3000/channels/"+channel+"/feed/last.json"
                    rcheck2 = urllib2.Request(checkurl2)
                    res2 = urllib2.urlopen(rcheck2)
                    res2 = res2.read()
                    resj = json.loads(res2)

                    checkurl22 = "http://localhost:3000/channels/" + channel2 + "/feed/last.json"
                    rcheck22 = urllib2.Request(checkurl22)
                    res22 = urllib2.urlopen(rcheck22)
                    res22 = res22.read()
                    resj2 = json.loads(res22)

                    Field = "field" + field
                    Field2 = "field" + field2_e
                    #print res2, res22
                    #print field2
                    if resj.has_key(Field) and resj2.has_key(Field2): # no key error
                        datacheck = resj[Field]  # the last data
                        datecheck = resj["created_at"]
                        filerecentpath = "./dispimage/C"+channel+"F"+field+".txt"
                        # "./dispimage/C"+channel+"F"+field+".txt"  #gai
                        filerecent = filerecentpath  # gai
                        datacheck2 = resj2[Field2]  # the last data
                        datecheck2 = resj2["created_at"]
                        filerecentpath2 = "./dispimage/C"+channel2+"F"+field2_e+".txt"
                        # "./dispimage/C"+channel+"F"+field+".txt"  #gai
                        filerecent2 = filerecentpath2  # gai
                        if os.path.exists(filerecent) and os.path.exists(filerecent2):  # existed and open
                            message = 'OK, the "%s" file exists.'
                            fdrecent = open(filerecent, "r")
                            fdrecenttxt = fdrecent.read()
                            fdrecenttxtsplit = fdrecenttxt.split(",")
                            fdrecent2 = open(filerecent2, "r")
                            fdrecenttxt2 = fdrecent2.read()
                            fdrecenttxtsplit2 = fdrecenttxt2.split(",")
                            # print fdrecenttxtsplit
                            # print datacheck
                            # print datecheck
                            if datacheck != fdrecenttxtsplit[0] or datacheck2 != fdrecenttxtsplit2[0]:  # data is not same ?
                                print "data update"
                                fdrecent.close()
                                # log
                                updatelog = open(updatepath, "a")
                                datalog = "Data update T:" + time.asctime(time.localtime(
                                    time.time())) + " C:" + channel + " F:" + field + " M:" + method + " R:" + results +"C2:"+channel2 + "F2" + field2_e
                                # print datalog
                                updatelog.write(datalog)
                                updatelog.close()

                                fdrecent = open(filerecent, "w")
                                datawritetxt = datacheck + "," + datecheck + "," + method + "," + results
                                fdrecent.write(datawritetxt)
                                fdrecent.close()

                                fdrecent2 = open(filerecent2, "w")
                                datawritetxt2 = datacheck2 + "," + datecheck2 + "," + method + "," + results
                                fdrecent2.write(datawritetxt2)
                                fdrecent2.close()

                                exec2MM(channel, field, method, results, channel2, field2_e)

                            elif datecheck != fdrecenttxtsplit[1] or datecheck2 != fdrecenttxtsplit2[1] :
                                print "date update"
                                fdrecent.close()
                                # log
                                updatelog = open(updatepath, "a")
                                datalog = "Date update T:" + time.asctime(time.localtime(
                                    time.time())) + " C:" + channel + " F:" + field + " M:" + method + " R:" + results +"C2:"+channel2 + "F2" + field2_e
                                # print datalog
                                updatelog.write(datalog)
                                updatelog.close()

                                fdrecent = open(filerecent, "w")
                                datawritetxt = datacheck + "," + datecheck + "," + method + "," + results
                                fdrecent.write(datawritetxt)
                                fdrecent.close()

                                fdrecent2 = open(filerecent2, "w")
                                datawritetxt2 = datacheck2 + "," + datecheck2 + "," + method + "," + results
                                fdrecent2.write(datawritetxt2)
                                fdrecent2.close()

                                exec2MM(channel, field, method, results, channel2, field2_e)
                            elif method != fdrecenttxtsplit[2]:
                                # print "method change update"
                                fdrecent.close()
                                # log
                                updatelog = open(updatepath, "a")
                                datalog = "Method update T:" + time.asctime(time.localtime(
                                    time.time())) + " C:" + channel + " F:" + field + " M:" + method + " R:" + results +"C2:"+channel2 + "F2" + field2_e
                                # print datalog
                                updatelog.write(datalog)
                                updatelog.close()

                                fdrecent = open(filerecent, "w")
                                datawritetxt = datacheck + "," + datecheck + "," + method + "," + results
                                fdrecent.write(datawritetxt)
                                fdrecent.close()

                                fdrecent2 = open(filerecent2, "w")
                                datawritetxt2 = datacheck2 + "," + datecheck2 + "," + method + "," + results
                                fdrecent2.write(datawritetxt2)
                                fdrecent2.close()

                                exec2MM(channel, field, method, results, channel2, field2_e)
                            elif results != fdrecenttxtsplit[3]:
                                # print "result change update"
                                fdrecent.close()
                                # log
                                updatelog = open(updatepath, "a")
                                datalog = "Results update T:" + time.asctime(time.localtime(
                                    time.time())) + " C:" + channel + " F:" + field + " M:" + method + " R:" + results +"C2:"+channel2 + "F2" + field2_e
                                # print datalog
                                updatelog.write(datalog)
                                updatelog.close()

                                fdrecent = open(filerecent, "w")
                                datawritetxt = datacheck + "," + datecheck + "," + method + "," + results
                                fdrecent.write(datawritetxt)
                                fdrecent.close()

                                fdrecent2 = open(filerecent2, "w")
                                datawritetxt2 = datacheck2 + "," + datecheck2 + "," + method + "," + results
                                fdrecent2.write(datawritetxt2)
                                fdrecent2.close()

                                exec2MM(channel, field, method, results, channel2, field2_e)

                            else:
                                # print "No exec"
                                pass
                        else:  # no existed and create one
                            # log
                            updatelog = open(updatepath, "a")
                            datalog = "New C update T:" + time.asctime(time.localtime(
                                time.time())) + " C:" + channel + " F:" + field + " M:" + method + " R:" + results + "C2:" + channel2 + "F2" + field2_e
                            # print datalog
                            updatelog.write(datalog)
                            updatelog.close()
                            if os.path.exists(filerecent2):
                                fdrecent = open(filerecent, "w")
                                # write newest data and time to file
                                datawritetxt = datacheck + "," + datecheck + "," + method + "," + results
                                fdrecent.write(datawritetxt)
                                fdrecent.close()
                                # print "create file and exec"
                            if os.path.exists(filerecent):
                                fdrecent = open(filerecent2, "w")
                                # write newest data and time to file
                                datawritetxt2 = datacheck2 + "," + datecheck2 + "," + method + "," + results
                                fdrecent.write(datawritetxt2)
                                fdrecent.close()

                            exec2MM(channel, field, method, results, channel2, field2_e)

                    # fdrecent.close()
                    else:
                        # print "dont have data"
                        pass

                        print "OK"
                        pass



    time.sleep(0.5)

