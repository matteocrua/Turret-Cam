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
    servo.setRotationAngle(channel, angle)
    servo_angle[channel] = angle

move_servo(SERVOY_CHANNEL, servo_angle[SERVOY_CHANNEL]) # (channel,angle) 1 is up and down: min=0, centre=40, max=80
move_servo(SERVOX_CHANNEL, servo_angle[SERVOX_CHANNEL])# (channel,angle) 0 is left to right: min=0, centre=90, max=180

def move_servos_relative(steps):
    # move the servos by the given number of steps
    # the steps are converted to an angle and the servo is moved to the new angle
    global servo_angle

    angle = servo_angle[SERVOY_CHANNEL] - servo_PID[SERVOY_CHANNEL].update(steps[SERVOY_CHANNEL])
    move_servo(SERVOY_CHANNEL, angle)
    
    angle = servo_angle[SERVOX_CHANNEL] - servo_PID[SERVOX_CHANNEL].update(steps[SERVOX_CHANNEL])
    move_servo(SERVOX_CHANNEL, angle)

def move_servos_manual(steps):
    # move the servos by the given number of steps
    # the steps are converted to an angle and the servo is moved to the new angle
    global servo_angle

    angle = servo_angle[SERVOY_CHANNEL] + steps[SERVOY_CHANNEL]
    move_servo(SERVOY_CHANNEL, angle)
    
    angle = servo_angle[SERVOX_CHANNEL] + steps[SERVOX_CHANNEL]
    move_servo(SERVOX_CHANNEL, angle)
