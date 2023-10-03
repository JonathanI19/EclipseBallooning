# @file: quad_cell_decoder
#
# @brief: Decoder module that locates brightest quadrant
#         and instructs servo motor to take action. 
#

# imports
from math import sqrt
from statistics import variance
from servo_controller import SERVO_DIRECTION

class QuadCellDecoder:
    """ The QuadCellDecoder class.

    Decodes inputs to locate brightest quadrant
    and instructs servo motor to take action.
    """

    def __init__(self):
        """ Constructor """

        self.__quadrant_intensities = ()
        self.__quadrant_variance = 0
        self.__brightest_quadrants = ()
        self.__servo_controller = None

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

        # Step 1) Find the highest intensity value, which
        #         corresponds to the brightest quadrant.
        max_intensity = max(self.__quadrant_intensities)

        # Step 2) Find any other intensity values that are
        #         within one standard deviation of the
        #         brightest value.
        std_dev = sqrt(self.__quadrant_variance)
        threshold = max_intensity - std_dev
        self.__brightest_quadrants = (True if val >= threshold else False for val in self.__quadrant_intensities)

    def decode_brightness_into_direction(self):
        """ Determines servo motor inputs based on quadrant brightness.


        @return    None
        """

        # at this point, self.__brightest_quadrants encodes which
        # quadrants we consider the 'brightest'; to improve efficiency,
        # we change from a tuple to an int
        servo_code = 0
        for i, val in enumerate(self.__brightest_quadrants):
            servo_code = servo_code + (pow(2, (4-i-1))*val)

        # decode the binary string
        if servo_code == 0b0000:
            moves = [SERVO_DIRECTION.NO_MOVE]
        elif servo_code == 0b0001:
            moves = [SERVO_DIRECTION.PAN_RIGHT, SERVO_DIRECTION.TILT_DOWN]
        elif servo_code == 0b0010:
            moves = [SERVO_DIRECTION.PAN_LEFT, SERVO_DIRECTION.TILT_DOWN]
        elif servo_code == 0b0011:
            moves = [SERVO_DIRECTION.TILT_DOWN]
        elif servo_code == 0b0100:
            moves = [SERVO_DIRECTION.PAN_LEFT, SERVO_DIRECTION.TILT_UP]
        elif servo_code == 0b0101:
            moves = [SERVO_DIRECTION.NO_MOVE]
        elif servo_code == 0b0110:
            moves = [SERVO_DIRECTION.PAN_LEFT]
        elif servo_code == 0b0111:
            moves = [SERVO_DIRECTION.PAN_LEFT, SERVO_DIRECTION.TILT_DOWN]
        elif servo_code == 0b1000:
            moves = [SERVO_DIRECTION.PAN_RIGHT, SERVO_DIRECTION.TILT_UP]
        elif servo_code == 0b1001:
            moves = [SERVO_DIRECTION.PAN_RIGHT]
        elif servo_code == 0b1010:
            moves = [SERVO_DIRECTION.NO_MOVE]
        elif servo_code == 0b1011:
            moves = [SERVO_DIRECTION.PAN_RIGHT, SERVO_DIRECTION.TILT_DOWN]
        elif servo_code == 0b1100:
            moves = [SERVO_DIRECTION.TILT_UP]
        elif servo_code == 0b1101:
            moves = [SERVO_DIRECTION.PAN_RIGHT, SERVO_DIRECTION.TILT_UP]
        elif servo_code == 0b1110:
            moves = [SERVO_DIRECTION.PAN_LEFT, SERVO_DIRECTION.TILT_UP]
        elif servo_code == 0b1111:
            moves = [SERVO_DIRECTION.NO_MOVE]
