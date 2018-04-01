# SheduledEvent

## Event Watcher(sheduler) for Domoticz with executing OS calls and Domoticz JSON calls

by Niskorodnov Alexander aka NailAlex(NailMan)

License: MIT License
https://mit-license.org/ 

The scheduler is used to create pending jobs with system calls or Domoticz calls with an unlimited number of command calls. 
He checks the directory with job files for the specified time and performs the task if the execution time has come. Then the event is deleted.

Supporting all Raspbian/Debian/Ubuntu platforms and including example script to create sheduled job. 

Features:
- Used with Python version 3+
- The Watcher is installed and launched as a system service
- The Watcher uses job storage in the form of files on the disk, therefore, intensive use of tasks for sensors can increase the wear of flash memory.
- Recommended for systems with Domoticz, deployed on HDD / SSD disks
- The created event for overwrites the previous one(for same device), if it has not already been executed. The date and time of its execution are updated.
- The script for creating a pending job is used to perform actions when the device is activated (for example, turning on the lamp) and performing a pending job (turning off after 10 minutes).
- The Watcher can call the system command (if necessary), for example call Ping ;)
- When the Watcher starts, it deletes all uncommitted jobs from the queue and create Events directory if it not exist
- The Watcher uses the logging of tasks and events

Typical use cases:
- actions for motion sensors with a delayed shutdown (for example, a backlight lamp)
- automatic security mode arming after a short time after the departure of the host
- many many other applications!

Download the latest version (version 1.0) here :
https://github.com/NailAlex/DomoticzEventWatcher


## HOW TO USE

Install procedure:

1. Download package. Unpack.

2. Create Event Watcher directory (example /home/pi/domoticz/eventwatcher) and put into this directory all scripts in package.

3. Copy the attached file "event_watcher.service" into /etc/systemd/system/ directory

4. Edit "event_watcher.service" file: change Event Watcher directory to your created path(step 2)

5. Edit "event_watcher.py": change log file path, events storage dir path, Check Delay

6. Run "systemctl daemon-reload"

7. Run "systemctl enable event_watcher"

8. Run "service event_watcher start"

9.1. Make sure that the scheduler is started(need installed "htop". run the command: "htop". You must see(for example): "python /home/pi/domoticz/eventwatcher/event_watcher.py"

9.2. Make sure that the event store directory was created and exist.

10. Voila!


Using Event Watcher:
A. Setup creator script for event:
A.1. Copy the attached file "event_create_template.py" and setup informative name for your device. Example: "MySens_UV-LAMP_10min.py"

A.2. Edit new creator script: 
- setup Domoticz address, port, credentials
- setup LOG_FILE_NAME path to logging, or disable logging by log_to_file
- setup Domoticz device identifiers: device_idx - the index of the main switch that makes the task to the Watcher), 
								HWSwitch_idx - optional index for switch assosiated with mySensors hardware)
								name - just informative name for device/event (no spaces or special symbols!)
- event_delay - execution delay. Range between CHECK_INTERVAL_SEC and 23:59:59, 24h format "H:M:S" 
- execute_cmd_x - one on many command lines with comands: if you need call domoticz use CMD_DOMOTICZ prefix. If you need call OS command, use CMD_OS prefix
- add "f.write(execute_cmd_X + "\n")" lines to write block
- add the current actions for the device activation event. Example call domoticz for light up the UV_LAMP (see example)

B. Test creator script by manual run

C. Put script path to switch action in Domoticz (edit switch). Example: "script:///home/pi/domoticz/myscripts/exec_scripts/uv-lamp_mysw_10min.py"

D. Push your switch, a job file appears in the Event store directory

E. After little time job will be completed and commands will be executed. Finished events will be deleted automatically.


## History

(April 2018) v1.0 - First release . 