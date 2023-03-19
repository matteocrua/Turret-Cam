from PCA9685 import PCA9685
from PID import PID

SERVOY_CHANNEL = 1
SERVOX_CHANNEL = 0
# 
servo_angle = [0,0] # array of servo angles
servo_range = [0,0] # array of servo ranges
servo_PID = [0,0] # array of PID controllers

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
    angle = servo_angle[SERVOY_CHANNEL] - servo_PID[SERVOY_CHANNEL].update(steps[SERVOY_CHANNEL]) 
    move_servo(SERVOY_CHANNEL, angle)
    
    angle = servo_angle[SERVOX_CHANNEL] - servo_PID[SERVOX_CHANNEL].update(steps[SERVOX_CHANNEL])
    move_servo(SERVOX_CHANNEL, angle)

# move the servos by the given number of steps
def move_servos_manual(steps):
    # the steps are then added to the current angle 
    # of the servo and moved to the new angle
    global servo_angle

    angle = servo_angle[SERVOY_CHANNEL] + steps[SERVOY_CHANNEL]
    move_servo(SERVOY_CHANNEL, angle)
    
    angle = servo_angle[SERVOX_CHANNEL] + steps[SERVOX_CHANNEL]
    move_servo(SERVOX_CHANNEL, angle)
