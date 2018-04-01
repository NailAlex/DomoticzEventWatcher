#!/usr/bin/python

import sys
import time
import datetime
from datetime import timedelta
import calendar
import urllib2
import json
import base64


# https://www.domoticz.com/wiki/Presence_detection#Installing_arping

# Settings for the domoticz server
domoticzserver="<domoticz ip address>:<domoticz web port>"
domoticzusername = "<domoticz user name>"
domoticzpassword = "<domoticz user password>"
domoticzpasscode = ""

#for domoticz call use this prefix
CMD_DOMOTICZ = "cmd_dom="
#for os call use this prefix
CMD_OS = "cmd_os="

#logging
log_to_file = True
LOG_FILE_NAME = '/home/pi/domoticz/log/event_watcher.log'


#domoiticz IDX for object (must be enabled and existed)
#This Example with two paired switches:
# - first(device_idx) - selector switch with many states and different scripts callback on each state 
# - second(HWSwitch_idx) - simple switch accosiate with one mySensors Relay (220V Socket and UV Lamp)
device_idx = "28"
#optional IDX for 
HWSwitch_idx = "30"
#Just name for visual identify
name = "UV_LAMP"
EVENT_NAME = "domoticz_id_" + device_idx + "_" + name
EVENT_FILE_NAME = "/home/pi/domoticz/myscripts/events/" + EVENT_NAME + ".event"
#time format - %H:%M:%S    - delay between 5sec - 23H:59M:59S
event_delay = "00:10:00"
#Event commands, than be executed after time is reached
#command 1  - deactivate hardware switch
execute_cmd_1 = CMD_DOMOTICZ + "http://" + domoticzserver + "/json.htm?type=command&param=switchlight&idx=" + HWSwitch_idx + "&switchcmd=Off"
#command 2  - deactivate selector switch
execute_cmd_2 = CMD_DOMOTICZ + "http://" + domoticzserver + "/json.htm?type=command&param=switchlight&idx=" + device_idx + "&switchcmd=Off"
#command 3  - push notification
execute_cmd_3 = CMD_DOMOTICZ + "http://" + domoticzserver + "/json.htm?type=command&param=sendnotification&subject=" + name + "-" + device_idx + "&body=%D0%A3%D0%A4-%D0%BB%D0%B0%D0%BC%D0%BF%D0%B0%20%D0%B2%D1%8B%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B0!"
#just example! Not need in real task! Ping a google DNS server and store output to file
execute_cmd_4 = CMD_OS + "ping -c 3 8.8.8.8 >/tmp/google.log"

previousstate=-1
lastsuccess=datetime.datetime.now()
lastreported=-1
base64string = base64.encodestring('%s:%s' % (domoticzusername, domoticzpassword)).replace('\n', '')
domoticzurl = 'http://'+domoticzserver+'/json.htm?type=devices&filter=all&used=true&order=Name'

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
    logfile.write(str(ntime) + ": " + message + "\n")
    logfile.close() 

now = datetime.datetime.now()
#print now
deltime = datetime.datetime.strptime(event_delay,"%H:%M:%S");
#print deltime
starttime = now + timedelta(hours=deltime.hour, minutes=deltime.minute, seconds=deltime.second)
#print starttime


f = open(EVENT_FILE_NAME, 'w')
f.write(name+"\n")
f.write(device_idx+"\n")
f.write(starttime.strftime("%Y-%m-%d %H:%M:%S")+"\n")
f.write(execute_cmd_1 + "\n")
f.write(execute_cmd_2 + "\n")
f.write(execute_cmd_3 + "\n")
f.write(execute_cmd_4 + "\n")
log(str(now) + " -> Create event for device: " + name + "[" + device_idx + "] Start time: " + starttime.strftime("%Y-%m-%d %H:%M:%S"))
f.close()

#Enable hardware switch and light up the UV Lamp!
domoticzrequest("http://" + domoticzserver + "/json.htm?type=command&param=switchlight&idx=" + HWSwitch_idx + "&switchcmd=On")
