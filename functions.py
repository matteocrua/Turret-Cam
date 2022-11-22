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
            raise Exception("functions.parse_user_input():unkown input") 