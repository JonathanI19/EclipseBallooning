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
    PAN_UP = 0
    PAN_DOWN = 1
    PAN_LEFT = 2
    PAN_RIGHT = 3
    TILT_UP = 4
    TILT_DOWN = 5
    NO_MOVE = 6

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
        for cmd in self.__movement_queue:
            pass

    def push_movement_command(self, new_cmd):

        # check input variable type
        if not type(new_cmd) is SERVO_DIRECTION:
            raise Exception(f"[ERROR] Invalid type {type(new_cmd)} provided.")
        
        # push the command
        self.__movement_queue.append(new_cmd)
