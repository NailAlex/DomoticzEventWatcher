#!/usr/bin/env python

import time, sys, datetime, logging, os
import urllib2
import json
import base64
import subprocess


# Settings for the domoticz server
domoticzserver="<domoticz ip address>:<domoticz web port>"
domoticzusername = "<domoticz user name>"
domoticzpassword = "<domoticz user password>"
domoticzpasscode = ""


previousstate=-1
lastsuccess=datetime.datetime.now()
lastreported=-1
base64string = base64.encodestring('%s:%s' % (domoticzusername, domoticzpassword)).replace('\n', '')
domoticzurl = 'http://'+domoticzserver+'/json.htm?type=devices&filter=all&used=true&order=Name'

#logging vars
log_to_file = True
#set your log file path for event watcher
LOG_FILE_NAME = '/home/pi/domoticz/log/event_watcher.log'
#set your event files store for cycled processing by watcher
EVENTS_DIRECTORY = '/home/pi/domoticz/myscripts/events/'
#processing interval
CHECK_INTERVAL_SEC = 5

def domoticzrequest (url):
  request = urllib2.Request(url)
  request.add_header("Authorization", "Basic %s" % base64string)
  response = urllib2.urlopen(request)
  return response.read()


def log(message):
  print message
  if log_to_file == True:
    ntime = datetime.datetime.now()
    logfile = open(LOG_FILE_NAME, "a")
    logfile.write(str(ntime) + " -> " + message + "\n")
    logfile.close() 

def clearEvents():
    files = os.listdir(EVENTS_DIRECTORY) 
    events = filter(lambda x: x.endswith('.event'), files)
    if len(events)!=0:
	for eventname in events:
	    os.remove(EVENTS_DIRECTORY + eventname)


try:
    log("Service was started")
    log("Clear old events")
    clearEvents()
    while True:
	time.sleep(CHECK_INTERVAL_SEC)
	try:
	    files = os.listdir(EVENTS_DIRECTORY) 
	    events = filter(lambda x: x.endswith('.event'), files)
	    if len(events)==0:
		print "Wait for events..."
	    else:
		for eventname in events:
		    
		    f = open(EVENTS_DIRECTORY + eventname, 'r')
		    lines = f.readlines()
		    f.close()
		    ename = lines[0].strip('\n')
		    idx = lines[1].strip('\n')
		    stime = lines[2].strip('\n')
		    starttime = datetime.datetime.strptime(stime,"%Y-%m-%d %H:%M:%S")
		    now = datetime.datetime.now()
		    print("Now: " + str(now) + "  Start: " + str(starttime) + "  Event: " + eventname)
		    if now >= starttime:
			for i in range(3,len(lines)):
			    cmd = lines[i].strip('\n')
			    if cmd.find("cmd_dom=", 0 , len(cmd) )!=-1:
				cmd = cmd.replace("cmd_dom=", "")
				log("Execute Domoticz command: " + cmd)
				domoticzrequest(cmd)

			    if cmd.find( "cmd_os=" , 0 , len(cmd) )!=-1:
				cmd = cmd.replace("cmd_os=", "")
			        log("Execute OS command: " + cmd)
			        subprocess.check_output(cmd,shell=True)

			print ("Delete event file")
			os.remove(EVENTS_DIRECTORY + eventname)

	except  Exception:
	    error = "TYPE: %s VALUE: %s" % ( str(sys.exc_info()[0]), str(sys.exc_info()[1]) )
	    log(error)

except BaseException:
    log("Service was stopped")
