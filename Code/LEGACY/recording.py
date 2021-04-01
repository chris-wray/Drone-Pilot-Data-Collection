# UAS Pilot Data Collection Tool
# CSCE 483 - Texas A&M University
# Spring 2020
# Rahul Rana, Aranpreet Gill, Maria Tyas, Juan Minor, Adolfo Herrera
# This code was created for our senior design project intended for UAS Pilot Researchers

# This file acts as the main program that opens all of the video streams and records them

# Imports
from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
from vidgear.gears import PiGear
from gpiozero import Button
import cv2
import time
import processing
import error
import os
import subprocess

#################################### ERROR LOG ####################################
errorOut = error.create("PI_ERROR_LOG.txt", 22)
################################# END ERROR LOG ###################################

################################ USB Capacity Check ###############################
# any disk with capacity more than 90% will throw error
# framework courtesy of https://stackoverflow.com/questions/34842735/python-script-to-verify-disk-space-output-from-linux
# variable 'disk_name' should be changed to that of the usb drive

threshold = 90
count = 0
disk_name = "/dev/sda1"

child = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE)
output = child.communicate()[0].strip().decode().split("\n")

diskExists = False

for disk in output:
    if disk_name in disk:
        usb_drive = disk
        print("USB drive exists")
        diskExists = True

if (not diskExists):
    errorOut.write(3, "USB drive not detected!")

if int(usb_drive.split()[4][:-1]) >= threshold:
    count = count + 1
    print("USB drive exceeds threshold! Reduce capacity.")

if count >= 1:
    errorOut.write(4, "USB drive exceeds threshold! Reduce capacity.")
################################ END CAPACITY CHECK ###############################

###################################### SETUP ######################################
# Options for each camera
options_picam = {"exposure_mode": "auto", "iso": 1800, "exposure_compensation": 15, "awb_mode": "horizon", "sensor_mode": 0, "CAP_PROP_FRAME_WIDTH ":1920, "CAP_PROP_FRAME_HEIGHT":1080} # define tweak parameters
options_webcam = {"exposure_mode": "auto", "iso": 100, "exposure_compensation": 0, "awb_mode": "sun", "sensor_mode": 0, "CAP_PROP_FRAME_WIDTH ":1920, "CAP_PROP_FRAME_HEIGHT":1080, "CAP_PROP_AUTOFOCUS": 'True'} # define tweak parameters

# Define list of streams
# Needed to create a new stream everytime record is pressed, otherwise
# issues arise with streams auto-closing if the button isn't pressed
# quickly enough between uses
video_streams = []

# Create an initial set of streams to both test connections and do initial setup
try:
    video_streams.append(VideoGear(source=2, resolution=(1280,720), **options_picam).start())
except:
    errorOut.write(1, "PiCamera not Detected")
try:
    video_streams.append(VideoGear(source=0, resolution=(1920,1080), **options_webcam).start())
except:
    errorOut.write(2, "Web Cam not Detected")

stream1 = video_streams[len(video_streams) - 2]
stream2 = video_streams[len(video_streams) - 1]

output_params1 = {"-vcodec":"libx264", "-preset":"slow", "-bitrate":2000000, "-input_framerate":stream1.framerate}
output_params2 = {"-input_framerate":stream2.framerate}

writer1 = WriteGear(output_filename = "blank.mkv", **output_params1) #Define writer
writer2 = WriteGear(output_filename = "blank.mkv", **output_params2) #Define writer

# Closing extra streams
stream1.stop()
stream2.stop()

fileNameList = []

compute = processing.Processing()

startTime = 0
endTime = 0
##################################### END SETUP #######################################


##################################### CHANGE LED ######################################
# This function calls led.py to change the color with given requirements
def change_LED(r, g, b):
    os.system('sudo python3 led.py -r' + str(r) + ' -g' + str(g) + ' -b' + str(b))
################################## END CHANGE LED #####################################

###################################### RECORDING ######################################
def beginRecording(button):

    global fileNameList
    global writer1
    global writer2
    global video_streams

    # start streams
    stream1 = video_streams[len(video_streams) - 2] # penultimate stream
    stream2 = video_streams[len(video_streams) - 1] # ultimate stream
    stream1.start()
    stream2.start()

    fileNameList = compute.getNewFileNames()
    print(fileNameList)
    writer1 = WriteGear(output_filename = fileNameList[0], **output_params1)
    writer2 = WriteGear(output_filename = fileNameList[1], **output_params2)

    change_LED(255,0,0) # Red LED to indicate recording

    while True:

        frameA = stream1.read()
        # read frames from stream1

        frameB = stream2.read()
        # read frames from stream2
        print("stream1.framerate:" + str(stream1.framerate))
        print("stream2.framerate:" + str(stream2.framerate))

        # check if any of two frame is None
        if frameA is None or frameB is None:
            #if True break the infinite loop
            break

        #cv2.imshow("Output Frame1", frameA)
        #cv2.imshow("Output Frame2", frameB)
        # Show output window of stream1 and stream 2 seperately

        writer1.write(frameA)
        writer2.write(frameB)

        # If button is pressed, exit recording
        if button.is_pressed:
            time.sleep(0.5)
            print("Stop Recording!")
            change_LED(255,165,0)
            global endTime
            endTime = time.time()
            break

    #cv2.destroyAllWindows()
    # close output window
################################### END START RECORDING ####################################

###################################### STOP RECORDING ######################################
def stopRecording():
    # safely close both video streams
    global video_streams
    stream1 = video_streams[len(video_streams) - 2]
    stream2 = video_streams[len(video_streams) - 1]
    stream1.stop()
    stream2.stop()

    # safely close both writers
    global writer1
    global writer2
    writer1.close()
    writer2.close()
################################### END STOP RECORDING #################################

###################################### PROCESSING ######################################
def processingVideo():

    change_LED(0,0,255) # Change LED to blue for processing

    # Will merge video file 1 and 2 into a merged file and move all three files into partitioned side of SD
    print(startTime)
    print(endTime)
    compute.mergeFiles(fileNameList[0],fileNameList[1], endTime - startTime, errorOut)

    change_LED(0,255,0) # setup is done, turn on green LED
    return 0 # return state to initial state
#################################### END PROCESSING #####################################

###################################### SHUT DOWN ########################################
def shutDown(button, firstTime):
    # check for second button press
    pressed = False
    while time.time() - firstTime < 2:
        if button.is_pressed:
            time.sleep(0.5)
            secondTime = time.time() # records the time for the second button press
            pressed = True
            break
    if not pressed:
        return pressed

    # check for third button press
    pressed = False
    while time.time() - secondTime < 2:
        if button.is_pressed:
            time.sleep(0.5)
            thirdTime = time.time() # records the time for the third button press
            pressed = True
            break
    if not pressed:
        return pressed

    # check for fourth button press
    pressed = False
    while time.time() - thirdTime < 2:
        if button.is_pressed:
            time.sleep(0.5)
            fourthTime = time.time() # records the time for the fourth button press
            pressed = True
            break
    if not pressed:
        return pressed

    # check for fourth button press
    pressed = False
    while time.time() - fourthTime < 2:
        if button.is_pressed:
            time.sleep(0.5)
            pressed = True
            return pressed
    if not pressed:
        return pressed
###################################### END SHUT DOWN ########################################

#################################### BUTTON INTEGRATION #####################################
button = Button(27) # connect button to GND (pin 39) and pin 13
state = 0 # Determine the state of the recording. 0 is the initial state.
change_LED(0,255,0) # Change LED to green, setup is complete

try:
    while True: # Run forever
            if button.is_pressed:
                time.sleep(0.5) #delay

                firstTime = time.time()

                #check for 5 button presses
                if shutDown(button, firstTime):
                    #os.system("sudo shutdown -h now") #shutdown
                    print("shutdown") # test
                    change_LED(0,0,0)
                    os.system('sudo shutdown now')
                    break # test

                # Recording Stage
                if state == 0:
                    state = state + 1 # go to the next state
                    print("Now Recording!")
                    startTime = time.time()

                    # initiate streams
                    # define and start the stream on first source ( For e.g #0 index Picamera)
                    try:
                        video_streams.append(VideoGear(source=2, resolution=(1280,720), **options_picam).start())
                    except:
                        errorOut.write(1, "PiCamera not Detected")
                    # define and start the stream on second source ( For e.g #1 index Picamera)
                    try:
                        video_streams.append(VideoGear(source=0, resolution=(1920,1080), **options_webcam).start())
                    except:
                        errorOut.write(2, "Web Cam not Detected")

                    beginRecording(button)
                    stopRecording()
                    state = processingVideo() # state resets back to initial state

                # Processing Stage
                else:
                    print("Now Processing!")
#turn off LED when interrupted
except KeyboardInterrupt:
    print("interrupt in main")
    change_LED(0,0,0)
