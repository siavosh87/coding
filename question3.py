from math import sqrt
import sys

def robot_moves(instructions):
    """
    This is our main function
    """
    if type(instructions) != list:
        raise ValueError("Input needs to be a list")
    
    if instructions[0].upper() != 'BEGIN':
        raise ValueError("Robot needs a BEGIN statement")

    position = [0, 0]

    for command in instructions:
        # First remove trailing whitespace
        command = command.strip()
        # Deals with first command
        if command.upper() == 'BEGIN':
            continue
        # Checking to see if instructed to stop
        if command.upper() == 'STOP':
            return calculate_distance(position)

        update_position(position, command)

    # If there is no STOP command at all, then alert user
    return "Robot has not been given a STOP command"

def calculate_distance(position):
    """
    This function will calculate distance using pythagoras thm
    distance = sqrt(x^2 + y^2)
    """
    x_final = position[0]
    y_final = position[1]
    distance_squared = (x_final ** 2) + (y_final ** 2)
    distance = sqrt(distance_squared)
    return round(distance, 2)

def update_position(position, command):
    """
    This function will update the position of the robot depending
    on the command. 
    x coordinate will be first element of position array
    y coordinate will be second element of position array
    We obtain direction by splitting on whitespace.
    The direction will be the first element after splitting.
    The number of steps will be the second element after splitting.
    """
    command = command.split()
    direction = command[0].upper()
    step_count = int(command[1])
    if direction == 'UP':
        position[1] += step_count
    elif direction == 'DOWN':
        position[1] -= step_count
    elif direction == 'LEFT':
        position[0] -= step_count
    elif direction == 'RIGHT':
        position[0] += step_count
    else:
        return "You have not given a valid command"
    return position

def main():
    """
    Checks to see if arguments have been passed in via command-line.
    If so, then convert arguments into a list of commands.
    If not, then will request input from user.
    """
    if len(sys.argv) >= 2:
        instructions = sys.argv[1].split(',')
        instructions = [x.strip() for x in instructions]
    else:
        user_input = input("Enter Robot instructions"+"\n"+
                        "Don't use brackets or quotations"+"\n"+
                        "Separate instructions by comma"+"\n")
        instructions = user_input.split(',')
    print(f"Distance from origin is {robot_moves(instructions)}")

main()











