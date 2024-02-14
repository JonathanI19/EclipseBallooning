# @file: stepper_controller.py
#
# @brief: Stepper controller module that processes
#         movement commands and controls stepper
#         directions. 
#

# imports
from enum import Enum
import RPi.GPIO as GPIO

class STEPPER_DIRECTION(Enum):
    """The STEPPER_DIRECTION enumeration."""
    STOP = 0
    PAN_LEFT = 1
    PAN_RIGHT = 2

class StepperController:
    """ The StepperController class.

    Processes movement commands and controls
    stepper directions.
    """

    def __init__(self, pan_stepper = None, tilt_stepper = None):
        """ Constructor """

        # initialize class data
        self.__pan_stepper = pan_stepper
        self.__tilt_stepper = tilt_stepper
        self.__movement_queue = []

        # initialize GPIO pins
        self.__PC0 = 19
        self.__PC1 = 26
        self.__TC0 = 20
        self.__TC1 = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__PC0, GPIO.OUT)
        GPIO.setup(self.__PC1, GPIO.OUT)
        GPIO.setup(self.__TC0, GPIO.OUT)
        GPIO.setup(self.__TC1, GPIO.OUT)

    def move_steppers(self):
        """ Move steppers based on commands stored in movement queue.

        @return    None
        """

        # process all commands in the queue
        while len(self.__movement_queue):

            # pop the next command
            cmd = self.__movement_queue.pop(0)

            # send the appropriate byte code to the Arduinos
            if cmd == STEPPER_DIRECTION.PAN_LEFT:
                GPIO.output(self.__PC0, GPIO.HIGH)
                GPIO.output(self.__PC1, GPIO.LOW)
                GPIO.output(self.__TC0, GPIO.LOW)
                GPIO.output(self.__TC1, GPIO.LOW)
            elif cmd == STEPPER_DIRECTION.PAN_RIGHT:
                GPIO.output(self.__PC0, GPIO.LOW)
                GPIO.output(self.__PC1, GPIO.HIGH)
                GPIO.output(self.__TC0, GPIO.LOW)
                GPIO.output(self.__TC1, GPIO.LOW)
            elif cmd == STEPPER_DIRECTION.TILT_UP:
                GPIO.output(self.__PC0, GPIO.LOW)
                GPIO.output(self.__PC1, GPIO.LOW)
                GPIO.output(self.__TC0, GPIO.HIGH)
                GPIO.output(self.__TC1, GPIO.LOW)
            elif cmd == STEPPER_DIRECTION.TILT_DOWN:
                GPIO.output(self.__PC0, GPIO.LOW)
                GPIO.output(self.__PC1, GPIO.LOW)
                GPIO.output(self.__TC0, GPIO.LOW)
                GPIO.output(self.__TC1, GPIO.HIGH)
            elif cmd == STEPPER_DIRECTION.PAN_LEFT_TILT_UP:
                GPIO.output(self.__PC0, GPIO.HIGH)
                GPIO.output(self.__PC1, GPIO.LOW)
                GPIO.output(self.__TC0, GPIO.HIGH)
                GPIO.output(self.__TC1, GPIO.LOW)
            elif cmd == STEPPER_DIRECTION.PAN_LEFT_TILT_DOWN:
                GPIO.output(self.__PC0, GPIO.HIGH)
                GPIO.output(self.__PC1, GPIO.LOW)
                GPIO.output(self.__TC0, GPIO.LOW)
                GPIO.output(self.__TC1, GPIO.HIGH)
            elif cmd == STEPPER_DIRECTION.PAN_RIGHT_TILT_UP:
                GPIO.output(self.__PC0, GPIO.LOW)
                GPIO.output(self.__PC1, GPIO.HIGH)
                GPIO.output(self.__TC0, GPIO.HIGH)
                GPIO.output(self.__TC1, GPIO.LOW)
            elif cmd == STEPPER_DIRECTION.PAN_RIGHT_TILT_DOWN:
                GPIO.output(self.__PC0, GPIO.LOW)
                GPIO.output(self.__PC1, GPIO.HIGH)
                GPIO.output(self.__TC0, GPIO.LOW)
                GPIO.output(self.__TC1, GPIO.HIGH)
            else:
                GPIO.output(self.__PC0, GPIO.LOW)
                GPIO.output(self.__PC1, GPIO.LOW)
                GPIO.output(self.__TC0, GPIO.LOW)
                GPIO.output(self.__TC1, GPIO.LOW)

    def push_movement_command(self, new_cmd):

        # check input variable type
        if not type(new_cmd) is STEPPER_DIRECTION:
            raise Exception(f"[ERROR] Invalid type {type(new_cmd)} provided.")
        
        # push the command
        self.__movement_queue.append(new_cmd)

    def view_movement_queue(self):
        """ Gets the __movement_queue member variable.

        @return    list(STEPPER_DIRECTION)
        """
        return self.__movement_queue
        
    def cleanup(self):
        """ Cleanup GPIO pins.

        @return    None
        """
        GPIO.output(self.__PC0, GPIO.LOW)
        GPIO.output(self.__PC1, GPIO.LOW)
        GPIO.output(self.__TC0, GPIO.LOW)
        GPIO.output(self.__TC1, GPIO.LOW)
        GPIO.cleanup()
    