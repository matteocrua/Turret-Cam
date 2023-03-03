from app import FRAME_WIDTH, FRAME_HEIGHT

#match case statement added to decide which action is required
def parse_user_input(input_string):
    match input_string:
        case "u":
            print("move up")
        case "d":
            print("move down")
        case "l":
            print("move left")
        case "r":
            print("move right")
        case "snap":
            print("taking snapshot")
        case "rec_on":
            print("taking a recording")
        case "rec_off":
            print("stopping the recording")
        case _:
            raise Exception("functions.parse_user_input():unknown input")

def face_offset(face):
    # face is a tuple of (x,y,w,h)
    # x,y is the top left corner of the face
    # w,h is the width and height of the face
    # the offset is the distance from the center of the frame to the center of the face
    # the offset is a tuple of (x_offset, y_offset)
    x_offset = face[0] + face[2]/2 - FRAME_WIDTH/2
    y_offset = face[1] + face[3]/2 - FRAME_HEIGHT/2
    return (x_offset, y_offset)

def servo_steps_from_face_offset(offsets):
    # the servo steps is the number of steps the servo motor needs to move
    # the deadband is a set value of offset  
    # ignored when calculating the number of servo steps away from the centre
    X_DEADBAND = 5
    Y_DEADBAND = 5 
    x_steps = offsets[0] / 10
    y_steps = offsets[1] / 10

    if abs(x_steps) < X_DEADBAND:
        x_steps = 0
    if abs(y_steps) < Y_DEADBAND:
        y_steps = 0

    return (x_steps, y_steps)

def find_face_closest_to_centre(faces):
    # faces is a list of tuples of (x,y,w,h)
    # the face closest to the centre is the face with the smallest offset
    # the offset is the distance from the center of the frame to the center of the face
    # the offset is a tuple of (x_offset, y_offset)
    # the offset is a constant
    # the offset is in pixels
    # the offset is a constant
    X_OFFSET = FRAME_WIDTH/2
    Y_OFFSET = FRAME_HEIGHT/2
    min_offset = (FRAME_WIDTH, FRAME_HEIGHT)
    min_face = None
    for face in faces:
        offset = face_offset(face)
        if abs(offset[0]) < abs(min_offset[0]) and abs(offset[1]) < abs(min_offset[1]):
            min_offset = offset
            min_face = face
    return min_face
    



