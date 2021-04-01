#A4 Processing.py
#Function Definitions:
#  4.1 Sync with ffmpeg
#  4.2 Verify synced on SD
#  4.3 Export (3 files)
#      Copy of Error Log
import os
import time
import datetime
import pathlib
import subprocess
import ErrorHandling
import shutil

#path for USB drive
usbPath = "/media/pi/VIDEOS"
presentPath = "/home/pi/Desktop/Codebase"
#path for local storage -- SD card
localPath = "/home/pi/Documents/localVids"



#Helper Function for A4.1
def getVideoLength(videoFile):
    #print("in get vid len: ",videoFile)
    f = localPath + "/" + videoFile
    result = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",f],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return float(result.stdout)
#A4.1
def synchronizeVideos(duration):
    global fileNameList
    global timeStamp
    try:
    	# create merged file
        fastMerged = timeStamp + "fastMerged.mp4"
    	# use filter complex and stack videos side by side
        os.system("sudo ffmpeg -loglevel panic -i " + localPath + "/" + fileNameList[0] + " -i "+ localPath + "/" + fileNameList[1] + " -filter_complex \"[0:v:0]pad=iw*2:ih[bg]; [bg][1:v:0]overlay=w\" " + localPath + "/" + fastMerged)
        print("Processing Phase 1 Done")
    except:
        os.system("sudo python3 -c 'import ErrorHandling;ErrorHandling.errorBadFile()'")

    # if merging & synching happens properly, continue to slow and adjust video
    #try:
    #final merged file to be exported and used
    #print("Phase 2")
    fileNameList.append(fastMerged)
    mergedVideo = timeStamp + "merged.mp4"
    fileNameList.append(mergedVideo)
    #print("slowing down")
    # slow video down
    vidLength = getVideoLength(fastMerged)
    #print("video length: ",vidLength)
    ### test with diff formula ###
    #return True
    #except:
       # return False
    slowingFactor = duration/vidLength
    try:
        os.system("sudo ffmpeg -loglevel panic -i " + localPath + "/" + fastMerged + " -vf setpts=" + str(slowingFactor) + "*PTS " + localPath + "/" + mergedVideo)
    except:
        os.system("sudo python3 -c 'import ErrorHandling;ErrorHandling.errorBadSynch()'")
    #print("merged ? " ,os.path.exists(localPath + "/" + mergedVideo))
    #print("fast merged ? ", os.path.exists(localPath + "/" +fastMerged))
    print("Synchronization of videos Complete \n")
    #os.system("rm -f "+ presentPath + "/" + fastMerged)
    #os.system("sudo mv " + presentPath + "/" + mergedVideo + " " + localPath)
    #ErrorHandling.errorBadSynch()

#A4.2
# check if synched video is on SD card
def verifySynchedVideos():
    global fileNameList
    if(os.path.exists(localPath + "/" + fileNameList[len(fileNameList)-1]) == False):
        return False
	#os.system("sudo python3 -c 'import ErrorHandling;ErrorHandling.errorBadSynch()'")
    else:
        return True

#A4.3
def exportVideos():
    global fileNameList
    global timeStamp
    destPath = usbPath + "/" + timeStamp
    #src_path = localPath
    print("Exporting Files "+ ','.join(fileNameList))
    try:
        if(os.path.exists(destPath) == False):
            #os.makedirs(dest_path)
            os.system("sudo mkdir " + destPath)
        for f in fileNameList:
            #os.system("sudo cp " + localPath + "/" + f + "" 
            srcPath = localPath + "/" + f
            shutil.copy(srcPath, destPath)
        return True
    except:
        return False
	#os.system("sudo python3 -c 'import ErrorHandling;ErrorHandling.errorUSBStorage()'")



## Main ##
def Processing(fnl,duration):
        print("Starting Processing")
        print("Duration of Recording = ",duration)
        global timeStamp
        global fileNameList
        fileNameList = fnl
        print("Files : "+','.join(fileNameList))
        ts = time.time()
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
        synchronizeVideos(duration)
        vr = verifySynchedVideos()
        exportVideos()
        return vr

fileNameList = []
timeStamp = ""
# Note : make time Stamp uniform 





#ts = time.time()
#timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
#fileNameList = ["2020-10-29-13-26-18_FaceCamVideo.mp4", "2020-10-29-13-26-18_TabletCamVideo.mp4"]
#duration = 20
#print(synchronizeVideos(duration))
#print(verifySynchedVideos())
