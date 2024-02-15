# @file: solar_sensor_decoder.py
#
# @brief: Decoder module that instructs stepper motor to take
#         action if the brightest/darkest photodiode is not
#         aligned with or opposite to the camera.
#

# imports

class SolarSensorDecoder:
    """ The SolarSensorDecoder class.

    Decodes inputs to adjust camera's position if 
    solar sensor is not properly aligned.
    """

    def __init__(self, aligned_quadrant, dark_flag, stepper_controller):
        """Constructor

        Args:
            aligned_quadrant (int) : the diode/quadrant that must be either brightest or darkest
            dark_flag (bool) : if set, the "aligned_quadrant" will be aimed away from the sun
            stepper_controller : reference to the singleton StepperController instance
        """
        pass

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
