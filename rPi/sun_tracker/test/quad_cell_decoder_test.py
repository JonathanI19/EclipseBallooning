# @file: quad_cell_decoder_test.py
#
# @brief: Unit tests for the QuadCellDecoder module. 
#

# imports
import pytest
from util.quad_cell_decoder import QuadCellDecoder
from util.stepper_controller import StepperController
from util.stepper_controller import STEPPER_DIRECTION

class TestQuadCellDecoder:
    """ Test class for QuadCellDecoder.

    Unit testing for QuadCellDecoder.
    """

    def test_set_intensity_values_nominal(self):
        """ Verify normal functionality of set_intensity_values.

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (102, 405, 34, 8)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)

        # verify output
        test_output = quad_cell_decoder_UUT.get_quadrant_intensities()
        for i in range(0, 3):
            assert test_output[i] == test_intensities[i]

        # cleanup
        quad_cell_decoder_UUT.__stepper_controller.cleanup()

    def test_set_intensity_values_wrong_type(self):
        """ Verify exception raised when wrong type provided.

        @return    None
        """

        # expect the exception to be rasied
        with pytest.raises(Exception) as e:

            # instantiate the UUT
            quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

            # create the test input (list instead of tuple)
            test_intensities = [102, 405, 34, 8]

            # call the function under test
            quad_cell_decoder_UUT.set_intensity_values(test_intensities)

        # check exception message
        assert str(e.value) == "[ERROR] Invalid type <class 'list'> provided."

    def test_set_intensity_values_wrong_size(self):
        """ Verify exception raised when wrong sized tuple provided.

        @return    None
        """

        # expect the exception to be rasied
        with pytest.raises(Exception) as e:

            # instantiate the UUT
            quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

            # create the test input (too large)
            test_intensities = (102, 405, 34, 8, 5)

            # call the function under test
            quad_cell_decoder_UUT.set_intensity_values(test_intensities)

        # check exception message
        assert str(e.value) == "[ERROR] Invalid tuple of size 5 provided."

    def test_compute_quadrant_variance_pos(self):
        """ Verify variance calculation on positive numbers
        performed by compute_quadrant_variance.

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (102, 405, 34, 8)

        # call the functions under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()

        # verify output
        assert round(quad_cell_decoder_UUT.get_quadrant_variance(), 5) == 33432.91667
    
    def test_compute_quadrant_variance_neg(self):
        """ Verify variance calculation on positive or
        negative numbers performed by compute_quadrant_variance.

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (65, -405, -123455, 554321)

        # call the functions under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()

        # verify output
        assert round(quad_cell_decoder_UUT.get_quadrant_variance(), 4) == 92058305715.6667

    def test_locate_brightest_quadrant_0(self):
        """ Verify that locate_brightest_quadrant produces
        the correct boolean tuple (test case 0).

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        # - note that the brightest quadrant is Q2 with intensity 405
        # - the standard deviation of this set is 182.8476
        # - thus, the threshold value is 405 - 182.8476 = 222.1533
        # - thus, the brightest quadrant(s) is Q2
        test_intensities = (102, 405, 34, 8)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()

        # verify output
        golden_output = [False, True, False, False]
        test_output = quad_cell_decoder_UUT.get_brightest_quadrants()
        for i in range(0, 3):
            assert test_output[i] == golden_output[i]
        
    def test_locate_brightest_quadrant_1(self):
        """ Verify that locate_brightest_quadrant produces
        the correct boolean tuple (test case 1).

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        # - note that the brightest quadrant is Q4 with intensity 1000
        # - the standard deviation of this set is 417.7599
        # - thus, the threshold value is 1000 - 417.7599 = 582.2401
        # - thus, the brightest quadrant(s) are Q2 and Q4
        test_intensities = (43, 789, 456, 1000)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()

        # verify output
        golden_output = [False, True, False, True]
        test_output = quad_cell_decoder_UUT.get_brightest_quadrants()
        for i in range(0, 3):
            assert test_output[i] == golden_output[i]

    def test_locate_brightest_quadrant_2(self):
        """ Verify that locate_brightest_quadrant produces
        the correct boolean tuple (test case 2).

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        # - the standard deviation of this data is 4594.056
        # - this is 3.7% the maximum value, thus the sun is centered
        test_intensities = (120000, 129300, 123452, 129299)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()

        # verify output
        golden_output = [True, True, True, True]
        test_output = quad_cell_decoder_UUT.get_brightest_quadrants()
        for i in range(0, 3):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_0000(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 0000)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (124, 123, 120, 126)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.STOP]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_0001(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 0001)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (36788, 456, 12358, 129299)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_RIGHT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_0010(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 0010)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (36788, 456, 129299, 12358)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_LEFT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_0011(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 0011)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (36788, 456, 129299, 135000)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.STOP]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_0100(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 0100)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (36788, 129299, 456, 12358)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_LEFT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_0101(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 0101)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (36788, 129299, 456, 135000)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.STOP]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_0110(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 0110)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (36788, 129299, 135000, 456)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_LEFT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_0111(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 0111)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (36788, 129299, 135000, 120000)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_LEFT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_1000(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 1000)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (129299, 36788, 456, 36788)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_RIGHT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_1001(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 1001)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (129299, 36788, 456, 135000)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_RIGHT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_1010(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 1010)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (129299, 36788, 135000, 456)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.STOP]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_1011(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 1011)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (129299, 36788, 120000, 135000)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_RIGHT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_1100(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 1100)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (129299, 120000, 12358, 36788)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.STOP]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_1101(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 1101)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (129299, 120000, 456, 135000)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_RIGHT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_1110(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 1110)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (129299, 120000, 135000, 456)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.PAN_LEFT]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]

    def test_decode_brightness_into_direction_1111(self):
        """ Verify that decode_brightness_into_direction
        properly decodes input (test case: 1111)

        @return    None
        """

        # instantiate the UUT
        quad_cell_decoder_UUT = QuadCellDecoder(StepperController())

        # create test input
        test_intensities = (129299, 120000, 120456, 135000)

        # call the function under test
        quad_cell_decoder_UUT.set_intensity_values(test_intensities)
        quad_cell_decoder_UUT.compute_quadrant_variance()
        quad_cell_decoder_UUT.locate_brightest_quadrants()
        quad_cell_decoder_UUT.decode_brightness_into_direction()

        # verify output
        golden_output = [STEPPER_DIRECTION.STOP]
        test_output = quad_cell_decoder_UUT.get_stepper_controller().view_movement_queue()
        assert len(test_output) == len(golden_output)
        for i in range(0, len(test_output)):
            assert test_output[i] == golden_output[i]
