# @file: quad_cell_decoder.py
#
# @brief: Decoder module that locates brightest quadrant
#         and instructs servo motor to take action. 
#

# imports
from math import sqrt
from statistics import variance
from .servo_controller import SERVO_DIRECTION
from .servo_controller import ServoController

class QuadCellDecoder:
    """ The QuadCellDecoder class.

    Decodes inputs to locate brightest quadrant
    and instructs servo motor to take action.
    """

    def __init__(self):
        """ Constructor """

        self.__quadrant_intensities = ()
        self.__quadrant_variance = 0
        self.__brightest_quadrants = []
        self.__servo_controller = ServoController()

        # Coefficient for sensitivity modification
        self.k = 1

        # Assume tuple index corresponds to quadrant number plus 1:
        # ([0], [1], [2], [3])
        #
        #              |
        #        [1]   |   [0]
        #              |
        #      -----------------
        #              |
        #        [2]   |   [3]
        #              |

    def set_intensity_values(self, input_intensities):
        """ Input intensity/brightness levels for each quadrant.

        @param input_intensities    tuple of intensity values

        @return    None
        """

        # check input variable type
        if not type(input_intensities) is tuple:
            raise Exception(f"[ERROR] Invalid type {type(input_intensities)} provided.")

        # check the size of the provided tuple
        if len(input_intensities) != 4:
            raise Exception(f"[ERROR] Invalid tuple of size {len(input_intensities)} provided.")
        
        # clear previous data
        self.__quadrant_intensities = ()
        
        # save the tuple values
        self.__quadrant_intensities = input_intensities

    def compute_quadrant_variance(self):
        """ Computes the variance of given quadrant values.

        @return    None
        """

        self.__quadrant_variance = variance(self.__quadrant_intensities)

    def locate_brightest_quadrants(self):
        """ Determines which quadrants are the brightest.

        @return    None
        """

        # Step 0) Clear previous data
        self.__brightest_quadrants.clear()

        # Step 1) Find the highest intensity value, which
        #         corresponds to the brightest quadrant.
        max_intensity = max(self.__quadrant_intensities)

        # Step 2) Determine if data is "widely dispersed" (i.e.,
        #         the standard deviation is greater than 10% the
        #         the maximum value)
        std_dev = sqrt(self.__quadrant_variance)

        if std_dev/max_intensity < 0.1:

            # if standard deviation is not high, assume no movement is needed
            self.__brightest_quadrants = [True, True, True, True]

        else:
            
            # Step 3) Find any other intensity values that are
            #         within one standard deviation of the
            #         brightest value.
            threshold = max_intensity - (self.k*std_dev)
            self.__brightest_quadrants = [True if val >= threshold else False for val in self.__quadrant_intensities]

    def decode_brightness_into_direction(self):
        """ Determines servo motor inputs based on quadrant brightness.

        @return    None
        """

        # at this point, self.__brightest_quadrants encodes which
        # quadrants we consider the 'brightest'; to improve efficiency,
        # we change from a tuple to an int
        servo_code = 0
        for i, val in enumerate(self.__brightest_quadrants):
            servo_code = servo_code + (val*pow(2, (4-i-1)))

        # decode the binary string
        if servo_code == 0b0000:
            pass
        elif servo_code == 0b0001:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_RIGHT)
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_DOWN)
        elif servo_code == 0b0010:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_LEFT)
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_DOWN)
        elif servo_code == 0b0011:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_DOWN)
        elif servo_code == 0b0100:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_LEFT)
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_UP)
        elif servo_code == 0b0101:
            pass
        elif servo_code == 0b0110:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_LEFT)
            pass
        elif servo_code == 0b0111:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_LEFT)
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_DOWN)
        elif servo_code == 0b1000:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_RIGHT)
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_UP)
        elif servo_code == 0b1001:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_RIGHT)
        elif servo_code == 0b1010:
            pass
        elif servo_code == 0b1011:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_RIGHT)
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_DOWN)
        elif servo_code == 0b1100:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_UP)
        elif servo_code == 0b1101:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_RIGHT)
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_UP)
        elif servo_code == 0b1110:
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.PAN_LEFT)
            self.__servo_controller.push_movement_command(SERVO_DIRECTION.TILT_UP)
        elif servo_code == 0b1111:
            pass

    def get_quadrant_intensities(self):
        """ Gets __quadrant_intensities member variable.

        @return    tuple(double)
        """
        return self.__quadrant_intensities
    
    def get_quadrant_variance(self):
        """ Gets __quadrant_variance member variable.

        @return    double
        """
        return self.__quadrant_variance
    
    def get_brightest_quadrants(self):
        """ Gets __brightest_quadrants member variable.

        @return    tuple(bool)
        """
        return self.__brightest_quadrants
        
    def get_servo_controller(self):
        """ Gets __servo_controller member variable.

        @return    tuple(bool)
        """
        return self.__servo_controller
    