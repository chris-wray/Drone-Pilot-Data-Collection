#A2,A3 -- Recording.py
#  Function Defintiions:
#    2.1 Get time
#    2.2 Start Recording
#    2.3 Chnge LED to red (now recording)
#    --- common var : time stamp, video streams ---
#    3.1 Press button to stop ; Save files ; Get Stop time
#    3.2 Verify
#    3.3 change LED to Blue (now processing)
from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
import cv2
import ErrorHandling
import LEDControl
import os
import time
import datetime
import shutil
from gpiozero import Button


#path for USB drive
usbPath = "/media/pi/VIDEOS"
#path for local storage
localPath = "/home/pi/Documents/localVids"
# button
button = Button(27)


#A2.1 -
def getTime():
    return time.time()

# Helper function : File getNewFileNames
def getNewFileNames():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    FaceCamVideo = timeStamp + "_FaceCamVideo.mp4"
    TabletCamVideo = timeStamp + "_TabletCamVideo.mp4" #picam
    return [FaceCamVideo,TabletCamVideo]

#A2.3 - Change LED to Red to singal recording has begun.
def changeLEDtoRed():
    os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnRed()'")
    print("changeLEDtoRed")

#A2.2 - starts two video streams and stores them in videoStreams. The start time is stored in startTime.
def startRecording():
  try:
    global fileNameList
    global videoStreams
    global startTime
    global stopTime
    global writer_TabletCam
    global writer_FaceCam
    stream_FaceCam = videoStreams[len(videoStreams) - 1] # penultimate stream
    stream_TabletCam = videoStreams[len(videoStreams) - 2] # ultimate stream
    output_params1 = {"-vcodec":"libx264", "-preset":"slow", "-bitrate":2000000, "-input_framerate":stream_FaceCam.framerate}
    output_params2 = {"-input_framerate":stream_TabletCam.framerate}

    startTime = getTime()
        
    changeLEDtoRed()

    print("\n")
    print("Now Recording \n")

    fileNameList = getNewFileNames()

    writer_FaceCam = WriteGear(output_filename = fileNameList[0], **output_params1) 
    writer_TabletCam = WriteGear(output_filename = fileNameList[1], **output_params2)
    
    stream_TabletCam.start()
    stream_FaceCam.start()
    # record frame by frame
    
    while(True):
        frame_TabletCam = stream_TabletCam.read()
        # read frames from stream1

        frame_FaceCam = stream_FaceCam.read()
        # read frames from stream2
        #print("stream_TabletCam.framerate:" + str(stream_TabletCam.framerate))
        #print("stream_FaceCam.framerate:" + str(stream_FaceCam.framerate))

        # check if any of two frame is None
        if((frame_TabletCam is None) or (frame_FaceCam is None)):
            stopTime = getTime()
            break
        '''
        if frame_TabletCam is None:
            print("Frame A is none")
            stopTime = getTime()
            print("Going to Stop Recording")
            break
            
        if frame_FaceCam is None:
            #if True break the infinite loop
            print("Frame B is none")
            stopTime = getTime()
            print("Going to stop Recording")
            break
        '''
        #cv2.imshow("Output Frame1", frameA)
        #cv2.imshow("Output Frame2", frameB)
        # Show output window of stream1 and stream 2 seperately
        frame_TabletCam = cv2.rotate(frame_TabletCam,cv2.ROTATE_180)
        writer_TabletCam.write(frame_TabletCam)
        writer_FaceCam.write(frame_FaceCam)
        

        if(button.is_pressed):
            stopTime = getTime()
            #print("Going to Stop Recording")
            break
        
    #cv2.destroyAllWindows()
        
  except:
    return False        
    #os.system("sudo python3 -c 'import ErrorHandling;ErrorHandling.errorRecording()'")


#A3.1 - Stop the recording streams. Assumes videoStreams is a list of the streams (face camera followed by tablet camera).
def stopRecording():
    global writer_TabletCam
    global writer_FaceCam
    global videoStreams
    print("Stopping Recording \n")
    #maybe error handling
    try:
        stream_FaceCam = videoStreams[len(videoStreams) - 2] # penultimate stream
        stream_TabletCam = videoStreams[len(videoStreams) - 1] # ultimate stream
        
        stream_FaceCam.stop()
        stream_TabletCam.stop()
        
        writer_TabletCam.close()
        writer_FaceCam.close()
        
        #Move files to localVids
        os.system("sudo mv "+fileNameList[0]+" " + localPath)
        os.system("sudo mv "+fileNameList[1]+" " + localPath)
       
        return True
    except:
        return False
        #os.system("sudo python3 -c 'import ErrorHandling;ErrorHandling.errorRecording()'")

#A3.2 - Checks that the recorded files exist in
def verifyRecordings():
    if(((os.path.exists(localPath + "/" + fileNameList[0])) and (os.path.exists(localPath + "/" + fileNameList[1]))) == True):
        return True
    else:
        #os.system("sudo python3 -c 'import ErrorHandling;ErrorHandling.errorBadFile()'")
        return False

#A3.3 - Changes LED to blue to signal recording has ended and processing will begin
def changeLEDtoBlue():
    os.system("sudo python3 -c 'import LEDControl ;LEDControl.turnBlue()'")
    print("changeLEDtoBlue")
    #return


def Recording():
    
    global videoStreams
    global writer_TabletCam
    global writer_FaceCam
    global fileNameList
    global startTime
    global stopTime
    
    #####START on button PRESS and RELEASE
    while( not button.is_pressed):
        pass
    time.sleep(.5)
    print("Button pressed")
    #wait for release
    while (button.is_pressed):
        pass
    
    ####Camera recording settings
    options_picam = {"exposure_mode": "auto", "iso": 1800, "exposure_compensation": 15, "awb_mode": "horizon", "sensor_mode": 0, "CAP_PROP_FRAME_WIDTH ":1920, "CAP_PROP_FRAME_HEIGHT":1080} # define tweak parameters
    options_webcam = {"exposure_mode": "auto", "iso": 100, "exposure_compensation": 0, "awb_mode": "sun", "sensor_mode": 0, "CAP_PROP_FRAME_WIDTH ":1920, "CAP_PROP_FRAME_HEIGHT":1080, "CAP_PROP_AUTOFOCUS": 'True'} # define tweak parameters

    try:
        videoStreams.append(VideoGear(source=2, resolution=(1920,1080),framerate=30, **options_picam).start())
    except:
        videoStreams.append(VideoGear(source=1, resolution=(1920,1080),framerate=30, **options_picam).start())

    videoStreams.append(VideoGear(source=0, resolution=(1920,1080),framerate=30, **options_webcam).start()) 
    # REMOVE THE NEXT TWO LINES
    stream_FaceCam = videoStreams[len(videoStreams) - 1] # ultimate stream
    stream_TabletCam = videoStreams[len(videoStreams) - 2] # penultimate stream

    ####Output video settings
    output_params1 = {"-vcodec":"libx264", "-preset":"slow", "-bitrate":2000000, "-input_framerate":stream_TabletCam.framerate}
    output_params2 = {"-input_framerate":stream_FaceCam.framerate}

    writer_FaceCam = WriteGear(output_filename = "blank.mkv", **output_params1) #Define writer
    writer_TabletCam = WriteGear(output_filename = "blank.mkv", **output_params2) #Define writer


    startRecording()

    #print("startRecording finished")
    #time.sleep(2)
    
    #print("Testing stopRecording")
    stopRecording()
    #print("stopRecording finished")
    
    #Verify raw vids were saved locally
    #print("Testing verifyRecordings")
    vr = verifyRecordings()
    #print(vR)
    #print("Verifying Recordings finished: ",vr)
    
    changeLEDtoBlue()

    #get duration for processing
    duration = stopTime-startTime
    print("Done with Recording \n")
    return duration, fileNameList

##TESTTING CODE
#print("Testing startRecording")
videoStreams = []
fileNameList = []
startTime = 0
stopTime = 0
#print("Duration: " + str(dur))
#print("FileNameList: " + FNL[0] + " " + FNL[1])




    
