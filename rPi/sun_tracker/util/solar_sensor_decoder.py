# @file: solar_sensor_decoder.py
#
# @brief: Decoder module that instructs stepper motor to take
#         action if the brightest/darkest photodiode is not
#         aligned with or opposite to the camera.
#

# imports
from .stepper_controller import STEPPER_DIRECTION
from .stepper_controller import StepperController

class SolarSensorDecoder:
    """ The SolarSensorDecoder class.

    Decodes inputs to adjust camera's position if 
    solar sensor is not properly aligned.
    """

    def __init__(self, aligned_quadrant, dark_flag, stepper_controller):
        """Constructor

        Args:
            aligned_quadrant (int) : the diode/quadrant that must be brightest
            dark_quadrant (int) : The diode/quadrant that must be darkest
            dark_flag (bool) : if set, the "aligned_quadrant" will be aimed away from the sun
            stepper_controller : reference to the singleton StepperController instance
            adc_max (int) : max value possible to be output by ADC
        """

        self.__aligned_quadrant = 0
        self.__dark_quadrant = 2
        self.__dark_flag = False
        self.__stepper_control = stepper_controller
        self.__adc_max = 1023
        

    def decode_brightness_into_action(self, input_adc_values):
        """Determine movement by evaluating brightest quadrants

        Args:
            input_adc_values tuple(int): ADC values corresponding to sensor analog voltages

        Returns:
            bool: True if aligned_quadrant matches brightest; False if not
        """

        '''
        ORGANIZING THOUGHTS
        ----------------------------------

        

        Q3    |      Q0 *Aligned
              |
        ------|--------
              |
        Q2    |      Q1


        Cases:
            Single Quadrant above bright thresh:
                Q0: Return True
                Q1: Pan Left
                Q2: Pan to brightest of Q1 or Q3
                Q3: Pan Right

            Two Quadrants above bright thresh:
                Q0/Q1: 
                Q0/Q2: 
                Q0/Q3: 
                Q1/Q2: 
                Q1/Q3: 
                Q2/Q3: 
        '''
        pass
    
    def decode_darkness_into_action(self, input_adc_values):
        """Determine movement by evaluating darkest quadrants

        Args:
            input_adc_values tuple(int): ADC values corresponding to sensor analog voltages

        Returns:
            bool: True if aligned_quadrant matches brightest; False if not
        """     

        pass

    
    def get_stepper_controller(self):
        """ Gets __stepper_controller member variable.

        @return    tuple(bool)
        """
        return self.__stepper_controller
