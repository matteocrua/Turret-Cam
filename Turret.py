#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from PCA9685 import PCA9685
import itertools as it
from PID import PID
#from functions import face_offset, servo_steps_from_face_offset, find_face_closest_to_centre

SERVO_ANGLE_RATIO = 2.234567901234568 #

SERVOY_CHANNEL = 1
SERVOX_CHANNEL = 0

servo_angle = [0,0] # array of servo angles
servo_range = [0,0] # array of servo ranges
servo_PID = [0,0] # array of PID controllers

# set initial servo positions to centre of range
servo_angle[SERVOY_CHANNEL] = 40 # in degrees
servo_angle[SERVOX_CHANNEL] = 90 # in degrees

# set the servo ranges in degrees
servo_range[SERVOY_CHANNEL] = (0,80)
servo_range[SERVOX_CHANNEL] = (0,180)

servo_PID[SERVOY_CHANNEL] = PID(0.5, 0, 0) 
servo_PID[SERVOX_CHANNEL] = PID(0.5, 0, 0.5)

pwm = PCA9685()
print ("This is an PCA9685 routine")
pwm.setPWMFreq(50)

def move_servo(channel, angle):
    # move the servo to the given absolute angle
    # the angle is limited to the range of the servo 
    # the angle is converted to a pulse width and sent to the servo
    # the angle is stored in the servo_angle array
    global servo_angle
    if angle > servo_range[channel][1]:
        angle = servo_range[channel][1]
    elif angle < servo_range[channel][0]:
        angle = servo_range[channel][0]
    pwm.setRotationAngle(channel, angle)
    servo_angle[channel] = angle

move_servo(SERVOY_CHANNEL, servo_angle[SERVOY_CHANNEL]) # (channel,angle) 1 is up and down: min=0, centre=40, max=80
move_servo(SERVOX_CHANNEL, servo_angle[SERVOX_CHANNEL])# (channel,angle) 0 is left to right: min=0, centre=90, max=180

def move_servos_relative(steps):
    # move the servos by the given number of steps
    # the steps are converted to an angle and the servo is moved to the new angle
    global servo_angle
    #angle = servo_angle[SERVOX_CHANNEL] + (steps[SERVOX_CHANNEL] * SERVO_ANGLE_RATIO)
    angle = servo_angle[SERVOY_CHANNEL] - servo_PID[SERVOY_CHANNEL].update(steps[SERVOY_CHANNEL])
    move_servo(SERVOY_CHANNEL, angle)
    
    #angle = servo_angle[SERVOY_CHANNEL] + (steps[SERVOY_CHANNEL] * SERVO_ANGLE_RATIO)
    angle = servo_angle[SERVOX_CHANNEL] - servo_PID[SERVOX_CHANNEL].update(steps[SERVOX_CHANNEL])
    move_servo(SERVOX_CHANNEL, angle)

#move servo 1 up a step over a given set of steps from its starting angle
def move_y(steps):
    global servo_angle
    initial_pos = servoY_angle
    target_pos = initial_pos + steps
    for i in range(steps):
        pwm.setRotationAngle(1, initial_pos - 1)
        initial_pos -= 1
        time.sleep(0.01)
        print("initial_pos = ", initial_pos)
        i = i + 1
    servoY_angle = target_pos
    print("servoY_angle = ", servoY_angle)


# def move_down(steps):
#     global servoY_angle
#     initial_pos = servoY_angle
#     target_pos = initial_pos + steps
#     for i in range(steps):
#         pwm.setRotationAngle(1, initial_pos + 1)
#         initial_pos += 1
#         time.sleep(0.01)
#         print("initial_pos = ", initial_pos)
#         i = i + 1
#     servoY_angle = target_pos
#     print("servoY_angle = ", servoY_angle)

# def move_left(steps):
#     global servoX_angle
#     initial_pos = servoX_angle
#     target_pos = initial_pos + steps
#     for i in range(steps):
#         pwm.setRotationAngle(1, initial_pos + 1)
#         initial_pos += 1
#         time.sleep(0.01)
#         print("initial_pos = ", initial_pos)
#         i = i + 1
#     servoX_angle = target_pos
#     print("servoX_angle = ", servoX_angle)

# def move_right(steps):
#     global servoX_angle
#     initial_pos = servoX_angle
#     target_pos = initial_pos + steps
#     for i in range(steps):
#         pwm.setRotationAngle(1, initial_pos - 1)
#         initial_pos -= 1
#         time.sleep(0.01)
#         print("initial_pos = ", initial_pos)
#         i = i + 1
#     servoX_angle = target_pos
#     print("servoX_angle = ", servoX_angle)

# while True:
#     servo = input("servo: ")
#     if(servo == "1"):
#         Angle = input("enter an angle for servo 1: ")
#         Angle = int(Angle)
#         if(Angle >= 0 and Angle <= 80):
#             pwm.setRotationAngle(1, Angle)
#         else:
#             print("angle out of range")
#     elif(servo == "0"):
#         Angle = input("enter an angle for servo 0: ")
#         Angle = int(Angle)
#         if(Angle >= 0 and Angle <= 180):
#             pwm.setRotationAngle(0, Angle)
#         else:
#             print("angle out of range")
#     elif(servo == "cen"):
#         pwm.setRotationAngle(1, 58)
#         pwm.setRotationAngle(0, 90)
#     elif(servo == "ext"):
#         pwm.setRotationAngle(1, 0)
#         pwm.setRotationAngle(0, 180)
#     elif(servo == "sweep"):
#         for i in range(181):
#             pwm.setRotationAngle(0, i)
#             pwm.setRotationAngle(1, round(i/SERVO_ANGLE_RATIO))
#             print(i,round(i/SERVO_ANGLE_RATIO))
#             time.sleep(0.01)
#         for i in reversed(range(181)):
#             pwm.setRotationAngle(0, i)
#             pwm.setRotationAngle(1, round(i/SERVO_ANGLE_RATIO))
#             print(i,round(i/SERVO_ANGLE_RATIO))
#             time.sleep(0.01)
#     else:
#         print("invalid servo")

    

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

# except:
#     pwm.exit_PCA9685()
#     print ("\nProgram end")
#     exit()

