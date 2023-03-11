#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from PCA9685 import PCA9685
import itertools as it

SERVO_ANGLE_RATIO = 2.234567901234568

try:
    pwm = PCA9685()
    print ("This is an PCA9685 routine")
    pwm.setPWMFreq(50)
    #pwm.setServoPulse(1,500) 
    #pwm.setRotationAngle(0, 0)
    pwm.setRotationAngle(1, 58) # (channel,angle) 1 is up and down: min=0, centre=58, max=80
    pwm.setRotationAngle(0, 90) # (channel,angle) 0 is left to right: min=0, centre=90, max=180
    while True:
        servo = input("servo: ")
        if(servo == "1"):
            Angle = input("enter an angle for servo 1: ")
            Angle = int(Angle)
            if(Angle >= 0 and Angle <= 80):
                pwm.setRotationAngle(1, Angle)
            else:
                print("angle out of range")
        elif(servo == "0"):
            Angle = input("enter an angle for servo 0: ")
            Angle = int(Angle)
            if(Angle >= 0 and Angle <= 180):
                pwm.setRotationAngle(0, Angle)
            else:
                print("angle out of range")
        elif(servo == "cen"):
            pwm.setRotationAngle(1, 58)
            pwm.setRotationAngle(0, 90)
        elif(servo == "ext"):
            pwm.setRotationAngle(1, 0)
            pwm.setRotationAngle(0, 180)
        elif(servo == "sweep"):
            for i in range(181):
                pwm.setRotationAngle(0, i)
                pwm.setRotationAngle(1, round(i/SERVO_ANGLE_RATIO))
                print(i,round(i/SERVO_ANGLE_RATIO))
                time.sleep(0.01)
            for i in reversed(range(181)):
                pwm.setRotationAngle(0, i)
                pwm.setRotationAngle(1, round(i/SERVO_ANGLE_RATIO))
                print(i,round(i/SERVO_ANGLE_RATIO))
                time.sleep(0.01)
        else:
            print("invalid servo")

    

#     while True:
#         # setServoPulse(2,2500)
#         for i in range(10,170,2): 
#             pwm.setRotationAngle(1, i)   
#             #if(i<80):
#                 #pwm.setRotationAngle(0, i)   
#             time.sleep(0.1)
# 
#         for i in range(170,10,-2): 
#             pwm.setRotationAngle(1, i)   
#             #if(i<80):
#                 #pwm.setRotationAngle(0, i)            
#             time.sleep(0.1)

except:
    pwm.exit_PCA9685()
    print ("\nProgram end")
    exit()

