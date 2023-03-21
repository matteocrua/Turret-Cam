from PCA9685 import PCA9685
from PID import PID
import time

SERVOY_CHANNEL = 1
SERVOX_CHANNEL = 0
# 
servo_angle = [0,0] # list of servo angles
servo_range = [0,0] # list of servo ranges
servo_PID = [0,0] # list of PID controllers

# set initial servo positions to centre of range
servo_angle[SERVOY_CHANNEL] = 40 # in degrees
servo_angle[SERVOX_CHANNEL] = 90 # in degrees

# set the servo ranges in degrees
servo_range[SERVOY_CHANNEL] = (0,80)
servo_range[SERVOX_CHANNEL] = (0,180)

# set the PID controller values for each servo
# kp, ki, kd
servo_PID[SERVOY_CHANNEL] = PID(1, 0, 1) 
servo_PID[SERVOX_CHANNEL] = PID(1, 0, 1)

# setup the PCA9685 servo controller
servo = PCA9685() # create a servo object
print ("This is an PCA9685 routine")
servo.setPWMFreq(50) # set the frequency to 50Hz

# move the servo to the given absolute angle
# the angle is limited to the range of the servo 
def move_servo(channel, angle):  
    global servo_angle

    # if the angle is greater than the maximum angle,
    # then set the angle to the maximum angle
    if angle > servo_range[channel][1]: 
        angle = servo_range[channel][1]
    
    # if the angle is less than the minimum angle,
    # then set the angle to the minimum angle
    elif angle < servo_range[channel][0]:
        angle = servo_range[channel][0]
    
    # move the servo to the given angle
    servo.setRotationAngle(channel, angle)

    # the angle is stored in the servo_angle array,
    # as it is now the current angle of the servo
    servo_angle[channel] = angle

move_servo(SERVOY_CHANNEL, servo_angle[SERVOY_CHANNEL]) # (channel, centre angle)
move_servo(SERVOX_CHANNEL, servo_angle[SERVOX_CHANNEL]) # (channel, centre angle)

def move_servos_relative(steps):
    # move the servos by the given number of steps
    # the steps are converted to an angle and the servo is moved to the new angle
    global servo_angle  
    # the angle is calculated by subtracting the PID output from the current angle, 
    # the PID updates the number of steps to move every time this function is called
    # LEAVE OUT as it is being called continously in the main loop it will always update the steps to move
    # LEAVE OUT meaning it move iteratively to the target angle rather than moving to the target angle in one go
    angle_y  = servo_angle[SERVOY_CHANNEL] - servo_PID[SERVOY_CHANNEL].update(steps[SERVOY_CHANNEL])
    move_servo(SERVOY_CHANNEL, angle_y)
    
    angle_x = servo_angle[SERVOX_CHANNEL] - servo_PID[SERVOX_CHANNEL].update(steps[SERVOX_CHANNEL])
    move_servo(SERVOX_CHANNEL, angle_x)

# smoothly move the servos to the given target angle
def move_servos_manual(steps):
    global servo_angle

    # get the target angle for the servo
    target_angles = [] 
    # enumerate returns the index and the value of the item in the list
    for channel, step in enumerate(steps): 
        # calculate the target angle for the servo
        target_angle = servo_angle[channel] + step
        # limit the target angle to the range of the servo
        target_angle = max(min(target_angle, servo_range[channel][1]), servo_range[channel][0])
        # add the target angle to the list
        target_angles.append(target_angle)

    # move the servos in increments to the target angle
    finished = False 
    while not finished: 
        finished = True
        for channel, target_angle in enumerate(target_angles):
            # if the current angle minus the target angle is greater than 0.1, move the servo.
            # 0.1 acts as a deadband for the servos this is to prevent the servos 
            # from jittering when they are close to the target angle.
            if abs(servo_angle[channel] - target_angle) > 0.1: 
                # the direction is decided by comparing the current angle and the target angle
                direction = 1 if target_angle > servo_angle[channel] else -1 
                # the new angle is the current angle plus the direction
                angle = servo_angle[channel] + direction
                # limit the angle to the range of the servo
                angle = max(min(angle, servo_range[channel][1]), servo_range[channel][0])
                # move the servo to the new angle
                move_servo(channel, angle)
                # update the current angle of the servo
                servo_angle[channel] = angle
                # the movement is not finished
                finished = False
    # the movement has only finished when the servo is less than 0.1 

        # wait a short time before moving the servos again
        # to give a smoother movement
        time.sleep(0.01)