from app import FRAME_WIDTH, FRAME_HEIGHT
from Turret import *

face_tracking = True

#match case statement added to decide which action is required
def parse_user_input(input_string):
    global face_tracking
    match input_string:
        case "u":
            move_servos_manual((0, -10))
        case "d":
            move_servos_manual((0, 10))
        case "l":
            move_servos_manual((-20, 0))
        case "r":
            move_servos_manual((20, 0))
        case "snap":
            print("taking snapshot")
        case "rec_on":
            print("taking a recording")
        case "rec_off":
            print("stopping the recording")
        case "faceTrack_on":
            face_tracking = True
        case "faceTrack_off":
            face_tracking = False
        case _:
            raise Exception("functions.parse_user_input():unknown input")

def face_offset(face):
    # x,y is the top left corner of the face
    # w,h is the width and height of the face
    # the offset is the distance from the center 
    # of the frame to the center of the face
    x_offset = face[0] + (face[2]/2) - (FRAME_WIDTH/2)
    y_offset = face[1] + (face[3]/2) - (FRAME_HEIGHT/2)
    print(x_offset, y_offset)
    return (x_offset, y_offset)

def servo_steps_from_face_offset(offsets):
    # the servo steps is the number of steps the servo motor needs to move
    # the deadband is a set value of offset  
    # ignored when calculating the number of servo steps away from the centre
    X_DEADBAND = 0
    Y_DEADBAND = 0 
    x_steps = offsets[0] / 20
    y_steps = offsets[1] / 20

    # if the offset is less than the deadband then set the offset to 0
    # this prevents the servo from moving when the face is in the deadband
    if abs(x_steps) < X_DEADBAND:
        x_steps = 0
    if abs(y_steps) < Y_DEADBAND:
        y_steps = 0

    return (x_steps, y_steps)

def find_face_closest_to_centre(faces):
    # the face closest to the centre is the face that will be 
    # used to calculate the servo steps and tracked
    # any other faces will be ignored
    X_OFFSET = FRAME_WIDTH/2
    Y_OFFSET = FRAME_HEIGHT/2
    # set the minimum offset to the maximum possible offset
    min_offset = (FRAME_WIDTH, FRAME_HEIGHT)
    min_face = None 
    # loop through all the faces and find the face closest to the centre
    for face in faces:
        # get the offset of the face
        offset = face_offset(face)
        # if the offset is less than the minimum offset then set the 
        # minimum offset to the face offset
        # and set the minimum face to the face
        if abs(offset[0]) < abs(min_offset[0]) and abs(offset[1]) < abs(min_offset[1]):
            min_offset = offset
            min_face = face
    return (min_face)
    

def track_face(face):
    # get the face offset
    offset = face_offset(face)
    # get the servo steps from the face offset
    servo_steps = servo_steps_from_face_offset(offset)
    # move the servo
    move_servos_relative(servo_steps)


