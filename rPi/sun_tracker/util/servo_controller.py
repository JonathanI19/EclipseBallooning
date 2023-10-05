# @file: servo_controller.py
#
# @brief: Servo controller module that processes
#         movement commands and controls servo
#         directions. 
#

# imports
from enum import Enum

class SERVO_DIRECTION(Enum):
    """The SERVO_DIRECTION enumeration."""
    PAN_LEFT = 1
    PAN_RIGHT = 2
    TILT_UP = 3
    TILT_DOWN = 4

class ServoController:
    """ The ServoController class.

    Processes movement commands and controls
    servo directions.
    """

    def __init__(self, pan_servo = None, tilt_servo = None):
        """ Constructor """

        self.__pan_servo = pan_servo
        self.__tilt_servo = tilt_servo
        self.__movement_queue = []

    def move_servos(self):
        """ Move servos based on commands stored in movement queue.

        @return    None
        """

        # process all commands in the queue
        print("Executing movement commands for input frame ...")
        while len(self.__movement_queue):
            print(self.__movement_queue.pop(0))

    def push_movement_command(self, new_cmd):

        # check input variable type
        if not type(new_cmd) is SERVO_DIRECTION:
            raise Exception(f"[ERROR] Invalid type {type(new_cmd)} provided.")
        
        # push the command
        self.__movement_queue.append(new_cmd)

    def view_movement_queue(self):
        """ Gets the __movement_queue member variable.

        @return    list(SERVO_DIRECTION)
        """
        return self.__movement_queue
    