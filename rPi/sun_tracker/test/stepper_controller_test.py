# @file: stepper_controller_test.py
#
# @brief: Unit tests for the StepperController module. 
#

# imports
import pytest
from util.stepper_controller import STEPPER_DIRECTION
from util.stepper_controller import StepperController

class TestStepperController:
    """ Test class for StepperController.

    Unit testing for StepperController.
    """

    def test_push_movement_command_nominal(self):
        """ Verify normal functionality of push_movement_command.

        @return    None
        """

        # instantiate the UUT
        stepper_controller_UUT = StepperController()

        # call the function under test
        stepper_controller_UUT.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
        stepper_controller_UUT.push_movement_command(STEPPER_DIRECTION.STOP)

        # verify output
        assert stepper_controller_UUT.view_movement_queue()[0] == STEPPER_DIRECTION.PAN_LEFT
        assert stepper_controller_UUT.view_movement_queue()[1] == STEPPER_DIRECTION.STOP

    def test_push_movement_command_wrong_type(self):
        """ Verify exception raised when wrong type provided.

        @return    None
        """

        # expect the exception to be rasied
        with pytest.raises(Exception) as e:

            # instantiate the UUT
            stepper_controller_UUT = StepperController()

            # create the test input (list instead of STEPPER_DIRECTION)
            stepper_controller_UUT.push_movement_command([102, 405, 34, 8])

        # check exception message
        assert str(e.value) == "[ERROR] Invalid type <class 'list'> provided."
