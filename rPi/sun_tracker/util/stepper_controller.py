# @file: stepper_controller.py
#
# @brief: Stepper controller module that processes
#         movement commands and controls stepper
#         directions. 
#

# imports
from enum import Enum

class STEPPER_DIRECTION(Enum):
    """The STEPPER_DIRECTION enumeration."""
    STOP = 0
    PAN_LEFT = 1
    PAN_RIGHT = 2
    TILT_UP = 3
    TILT_DOWN = 4
    PAN_LEFT_TILT_UP = 5
    PAN_LEFT_TILT_DOWN = 6
    PAN_RIGHT_TILT_UP = 7
    PAN_RIGHT_TILT_DOWN = 8

class StepperController:
    """ The StepperController class.

    Processes movement commands and controls
    stepper directions.
    """

    def __init__(self, pan_stepper = None, tilt_stepper = None, is_rpi = False):
        """ Constructor """

        # initialize class data
        self.__pan_stepper = pan_stepper
        self.__tilt_stepper = tilt_stepper
        self.__movement_queue = []
        self.__is_rpi = is_rpi

        # initialize GPIO pins
        if (is_rpi):
            import RPi.GPIO as GPIO
            self.__PC0 = 25
            self.__PC1 = 8
            self.__TC0 = 23
            self.__TC1 = 24
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

            if (self.__is_rpi):
                import RPi.GPIO as GPIO
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
            print(cmd)

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
        if (self.__is_rpi):
            import RPi.GPIO as GPIO
            GPIO.output(self.__PC0, GPIO.LOW)
            GPIO.output(self.__PC1, GPIO.LOW)
            GPIO.output(self.__TC0, GPIO.LOW)
            GPIO.output(self.__TC1, GPIO.LOW)
            #GPIO.cleanup()
    
