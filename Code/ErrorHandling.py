#A5 ErrorHandling.py
#Function Definitions:
#  Error5.1-5.6:
#    Error log update
#    Change LED pattern
#    Call UpdateErrorLog(time,ErrorName)

import LEDControl
import os
from time import sleep
import datetime
import time
import shutil

numCycles = 3
dotOn = 0.1
dotOff = 0.2
dashOn = 0.4
dashOff = 0.2
endTime = 1

#A5.1
def errorFaceCam():
    print("errorFaceCam")
    updateErrorLog("No Face Cam detected")

    for i in range(numCycles):
        #dot 1
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dotOff)

        #dot 2
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dotOff)

        #dot 3
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(endTime)

    os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")


#A5.2
def errorTabletCam():
    print("errorTabletCam")
    updateErrorLog("Tablet Cam not detected")

    for i in range(numCycles):
        #dot 1
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dotOff)

        #dot 2
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dotOff)

        #dash
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dashOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(endTime)



#A5.3
def errorUSBDetect():
    print("errorUSBDetect")
    updateErrorLog("No USB Detected")

    for i in range(numCycles):

        #dot
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dotOff)

        #dash
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dashOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dashOff)

        #dot
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(endTime)

#A5.4
def errorUSBStorage():
    print("errorUSBStorage")
    updateErrorLog("No USB Storage")
    for i in range(numCycles):

        #dot
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dotOff)

        #dash
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dashOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dashOff)

        #dash
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dashOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(endTime)

#A5.5
def errorBadFile():
    print("errorBadFile")
    updateErrorLog("Bad File Save")
    
    while(True):

        #dash
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dashOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dashOff)

        #dot
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dotOff)

        #dot
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(endTime)

#A5.6
def errorBadSynch():
    print("errorBadSynch")
    updateErrorLog("Bad Vid Sync")
    ##For this error dump all data to USB
    
    shutil.copy("/home/pi/Documents/localVids", "/media/pi/VIDEOS/")

    while (True):

        #dash
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dashOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dashOff)

        #dot
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dotOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(dotOff)

        #dash
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(dashOn)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(endTime)

#Error signaling some problem in Recording process
def errorRecording():
    print("errorRecording")
    updateErrorLog("Bad Raw Files")
    shutil.copy("/home/pi/Documents/localVids","/media/pi/VIDEOS")
    while(True):

        #dash
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(.5)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(.1)

        #dash
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(.5)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(.1)

        #dot
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnOrange()'")
        sleep(.1)
        os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnCustom(0, 0, 0)'")
        sleep(1)


#A5.7
def updateErrorLog(errorName):
  try:
    print("Updating Error Log")
    #os.system("sudo errorName  >> /media/pi/VIDEOS/errorLog.txt")
    #os.popen("sudo 'test'?? /media/pi/VIDEOS/errorLog.txt")
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    #usbLog = open("/media/pi/VIDEOS/errorLog.txt", "a")
    sdLog = open("/home/pi/Documents/localVids/errorLog.txt", "a")

    #usbLog.write(errorName + " " + str(timeStamp)+"\n")
    sdLog.write(errorName + " " + str(timeStamp)+"\n")
    sdLog.close()
    if(os.path.exists("/media/pi/VIDEOS")):
       print("usb path detected")
       shutil.copy("/home/pi/Documents/localVids/errorLog.txt", "/media/pi/VIDEOS/")
    print(errorName)
    return True
    #usbLog.close()
    #sdLog.close()
  except:
    return False

#errorFaceCam()
