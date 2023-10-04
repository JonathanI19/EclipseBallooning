# @file: servo_controller_test.py
#
# @brief: Unit tests for the ServoController module. 
#

# imports
import pytest
from servo_controller import SERVO_DIRECTION
from servo_controller import ServoController

class TestServoController:
    """ Test class for ServoController.

    Unit testing for ServoController.
    """

    def test_push_movement_command_nominal(self):
        """ Verify normal functionality of push_movement_command.

        @return    None
        """

        # instantiate the UUT
        servo_controller_UUT = ServoController()

        # call the function under test
        servo_controller_UUT.push_movement_command(SERVO_DIRECTION.PAN_LEFT)
        servo_controller_UUT.push_movement_command(SERVO_DIRECTION.TILT_UP)

        # verify output
        assert servo_controller_UUT.view_movement_queue()[0] == SERVO_DIRECTION.PAN_LEFT
        assert servo_controller_UUT.view_movement_queue()[1] == SERVO_DIRECTION.TILT_UP

    def test_push_movement_command_wrong_type(self):
        """ Verify exception raised when wrong type provided.

        @return    None
        """

        # expect the exception to be rasied
        with pytest.raises(Exception) as e:

            # instantiate the UUT
            servo_controller_UUT = ServoController()

            # create the test input (list instead of SERVO_DIRECTION)
            servo_controller_UUT.push_movement_command([102, 405, 34, 8])

        # check exception message
        assert str(e.value) == "[ERROR] Invalid type <class 'list'> provided."
