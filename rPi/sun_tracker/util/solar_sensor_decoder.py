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
            adc_thresh (int) : threshold value used to determine whether we should switch to dark control
        """
        self.__aligned_quadrant = 0
        self.__dark_quadrant = 2
        self.__dark_flag = False
        self.__stepper_control = stepper_controller
        self.__adc_max = 1023
        self.__adc_thresh = int(self.__adc_max * 0.98)
        

    def decode_brightness_into_action(self, input_adc_values):
        """ Input intensity/brightness levels for each quadrant.

        @param input_adc_values    ADC values corresponding to sensor analog voltages

        @return    bool
        """
        return True
    
    def get_stepper_controller(self):
        """ Gets __stepper_controller member variable.

        @return    tuple(bool)
        """
        return self.__stepper_controller
