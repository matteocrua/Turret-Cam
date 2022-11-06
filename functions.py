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
        case _:
            raise Exception("functions.parse_user_input():unkown input") 