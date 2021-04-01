
# UAS Pilot Data Collection Tool
# CSCE 483 - Texas A&M University
# Spring 2020
# Rahul Rana, Aranpreet Gill, Maria Tyas, Juan Minor, Adolfo Herrera
# This code was created for our senior design project intended for UAS Pilot Researchers

# This file is a module recording imports to merge and sync the video files

# Imports
import os
import time
import datetime
import pathlib
import subprocess
import error

class Processing:
    timestamp = ""

    def get_length(self, filename):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        return float(result.stdout)

    def getNewFileNames(self):

        ts = time.time()
        self.timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

        fileNames = [self.timestamp+'_1.mp4',self.timestamp+'_2.mp4']

        return fileNames

    def saveFiles(self):
        # New folder with timestamp
        newPath = "/media/pi/VIDEOS/" + self.timestamp

        if not os.path.exists(newPath):
            # create folder
            os.makedirs(newPath)

            #move all files to folder
            os.system("mv *.mp4 " + newPath)
        else:
            errorOut.write(1, "Folder with name already exists! Files saved to temp folder")

            errorPath = "/media/pi/VIDEOS/temp"

            if not os.path.exists(errorPath):
                os.makedirs(errorPath)
                os.system("mv *.mp4 " + errorPath)
            else:
                os.system("mv *.mp4 " + errorPath)


    def mergeFiles(self, file1, file2, duration, errorFile):
        mergedFileName = "temp_" + self.timestamp + "_merged.mp4"

        # Get filePath
        filePath = str(pathlib.Path(__file__).parent.absolute())

        # Merge videos side by side - timestamp_merged.mkv
        try:
           os.system("ffmpeg -i " + filePath + "/" + file1 + " -i "+ filePath + "/" + file2 + " -filter_complex \"[0:v:0]pad=iw*2:ih[bg]; [bg][1:v:0]overlay=w\" " + mergedFileName)
        except:
            errorFile.write(5, "Raw Video Files Not Found")

        # Slow down video to final length
        try:
            vidLength = self.get_length(mergedFileName)
        except:
            errorFile.write(6, "Synced Video File Not Found")
        print(vidLength)
        print(duration)
        print(duration - 0.5)
        print(duration/vidLength)

        os.system("ffmpeg -i " + mergedFileName + " -vf setpts=" + str(duration/vidLength) + "*PTS " + mergedFileName[5:])

        # Delete temporary merged file
        os.system("rm " + mergedFileName)

        # Move all files to partitioned drive FUTURE USE
        self.saveFiles()
        return 0

error.py
# UAS Pilot Data Collection Tool
# CSCE 483 - Texas A&M University
# Spring 2020
# Rahul Rana, Aranpreet Gill, Maria Tyas, Juan Minor, Adolfo Herrera
# This code was created for our senior design project intended for UAS Pilot Researchers

# This file is a module recording imports to output errors as well as alter LED colors

# Imports
import os
import sys
import time
import subprocess

class Error():

    def __init__(self, file_name, BOARD_PIN):
        self.__number = 0
        self.__description = ""
        self.__file_name = file_name
        self.__board_pin = BOARD_PIN

    def write(self, number, description):
        ''' API to allow interaction with file '''
        self.__number = number
        self.__description = description

        self.write_to_file()

        # rgb colors for errors
        switcher = {
            0: [0, 0, 0], # default black
            1: [133, 51, 255], # purple           no pi cam
            2: [100, 10, 0],   # orange           no webcam
            3: [0, 255, 255],  # cyan             no USB
            4: [51, 255, 162], # white            usb full
            5: [0, 255, 0],    # flashing green   raw video not found
            6: [0, 0, 255]     # flashing blue    merged video not found
        }

        # select rgb val and change the color
        rgbVal = switcher.get(number, {0, 0, 0})
        self.change_LED(rgbVal[0], rgbVal[1], rgbVal[2], number)


    def write_to_file(self):
        ''' Write to the file '''
        self.__file_obj = open(self.__file_name, 'a+')
        error_str = "Error code: '" + str(self.__number) + "' - Description: " + self.__description + "\r\n"
        self.__file_obj.write(error_str)
        self.__file_obj.close()

    def change_LED(self, r, g, b, number):
        # Change the LED color
        self.__redVal = r
        self.__greVal = g
        self.__bluVal = b

        # Change the LED color or flash it if in the switch case for 60 seconds
        if(number < 5):
            os.system('sudo python3 led.py -r' + str(self.__redVal) + ' -g' + str(self.__greVal) + ' -b' + str(self.__bluVal))
            time.sleep(60)
        else:
            for i in range(60):
                os.system('sudo python3 led.py -r' + str(self.__redVal) + ' -g' + str(self.__greVal) + ' -b' + str(self.__bluVal))
                time.sleep(0.5)
                os.system('sudo python3 led.py -r 0 -g 0 -b 0')
                time.sleep(0.5)

        # Move error file to USB then shutdown
        os.system("mv *.txt /media/pi/VIDEOS")

        # turn off LED
        os.system('sudo python3 led.py -r 0 -g 0 -b 0')

        # Restart code'
        child = subprocess.Popen(['python', 'rerun.py'])
        sys.exit()


    def clear(self):
        self.__file_obj = open(self.__file_name, 'r+')
        self.__file_obj.truncate(0) # clear file for good
        self.__file_obj.close()

''' Main '''
def create(file_name, BOARD_PIN):
    error = Error(file_name, BOARD_PIN)
    return error
