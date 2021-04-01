#UNIT TESTING CODE FOR A1 - A4
import DeviceInitialization
import Recording
import Processing
import ErrorHandling
import subprocess

# UNIT TEST  : A1
print("UNIT TEST A1 : DEVICE INITIALIZATION")
print("INPUTS : None")
print("EXPECTED OUTPUT :0")
print("\n") 
outputA1 = DeviceInitialization.DeviceInitialization()
print("\n")
print("OUTPUT A1 : ",outputA1)
if(outputA1 == 0):
    print("UNIT TEST A1 DEVICE INITIALIZATION STATUS : PASS")
elif(ouputA1 == -1):
    print("UNIT TEST A1 DEVICE INITIALIZATION STATUS : FAIL")
print("\n")

# UNIT TEST : A2, A3
print("UNIT TEST A2, A3 : RECORDING")
print("INPUTS : None")
print("EXPECTED OUTPUTS : 1. duration (float object) 2. fileNameList (list object)")
print("\n")
# duration, fnl
outputA23_1, outputA23_2 = Recording.Recording()
print("\n")
print("OUTPUTS : ",outputA23_1,outputA23_2)
if((type(outputA23_1) == float) and (type(outputA23_2) == list)):
    print("UNIT TEST A2, A3 RECORDING STATUS : PASS")
else:
    print("UNIT TEST A2, A3 RECORDING STATUS : FAIL")

print("\n")


# UNIT TEST A4
print("UNIT TEST A4 : PROCESSING")
print("INPUTS : 1. fileNameList (list object) 2. duration (float object)")
print("EXPECTED OUTPUT : True")
print("\n")
inputA4_1 = outputA23_2
inputA4_2 = outputA23_1
# declaration of output
outputA4 = ""
if((type(inputA4_1) ==list) and (type(inputA4_2) == float) and (len(inputA4_1) ==2) and (inputA4_2 >=0)):
    outputA4 = Processing.Processing(inputA4_1,inputA4_2)
else:
    print("A4 INPUT CHECK FAILED")

print("\n")
if(outputA4 == True):
    print("UNIT TEST A4 PROCESSING STATUS : PASS")
elif(outputA4 == False):
    print("UNIT TEST A4 PROCESSING STATUS : FAIL")
print("\n")

