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
        self.__stepper_controller = stepper_controller
        self.__adc_max = 1023
        

    def decode_brightness_into_action(self, input_adc_values, isBright):
        """Determine movement by evaluating brightest quadrants

        Args:
            input_adc_values list(int): ADC values corresponding to sensor analog voltages
            isBright list(bool): Separated by quadrant; True if above brightness threshold, otherwise false

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
                Q1: Pan Right
                Q2: Pan Left if Q3 > Q1; Pan Right if Q1 > Q3
                Q3: Pan Left

            Two Quadrants above bright thresh:
                Q0/Q1: Return True if Q0 Brightest; Else Pan Right
                Q0/Q2: Return True if Q0 Brightest; Else, Pan Left if Q3 > Q1; Pan Right if Q1 > Q3
                Q0/Q3: Return True if Q0 Brightest; Else Pan Left
                Q1/Q2: Pan Right
                Q1/Q3: Pan Left if Q3 > Q1; Pan Right if Q1 > Q3
                Q2/Q3: Pan Left
        '''
        
        if (input_adc_values == [0,0,0,0]):
            return True
        # self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
        # self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.STOP)
        # self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)

        
        # Q0: Return True
        if (isBright == [True, False, False, False]):
            return True
        
        # Q1: Pan Right
        elif (isBright == [False, True, False, False]):
            self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
            return False
            
        # Q2: Pan Left if Q3 > Q1; Pan Right if Q1 > Q3
        elif (isBright == [False, False, True, False]):
            if (input_adc_values[1] > input_adc_values[3]):
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
            elif (input_adc_values[3] > input_adc_values[1]):
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
                
                
            ########################## IMPORTANT ##########################
            # Backup in case Q1 and Q3 are equal; Pan in direction; Potential for error here
            else:
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.STOP)
                
            return False
        
        # Q3: Pan Left
        elif (isBright == [False, False, False, True]):
            self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
            return False
        
        # Q0/Q1: Return True if Q0 Brightest; Else Pan Right
        elif (isBright == [True, True, False, False]):
            if (input_adc_values[0] > input_adc_values[1]):
                return True
            else:
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
                return False
        
        # Q0/Q2: Return True if Q0 Brightest; Else, Pan Left if Q3 > Q1; Pan Right if Q1 > Q3
        elif (isBright == [True, False, True, False]):
            if (input_adc_values[0] > input_adc_values[2]):
                return True
            
            else:
                if (input_adc_values[1] > input_adc_values[3]):
                    self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
                elif (input_adc_values[3] > input_adc_values[1]):
                    self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
               
                ########################## IMPORTANT ##########################
                # Backup in case Q1 and Q3 are equal; Pan in direction; Potential for error here
                else:
                    self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.STOP)
                    
                return False
        
        # Q0/Q3: Return True if Q0 Brightest; Else Pan Left
        elif (isBright == [True, False, False, True]):
            if (input_adc_values[0] > input_adc_values[3]):
                return True
            else:
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
                return False
            
        # Q1/Q2: Pan Right
        elif (isBright == [False, True, True, False]):
            self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
            return False
        
        # Q1/Q3: Pan Left if Q3 > Q1; Pan Right if Q1 > Q3
        elif (isBright == [False, True, False, True]):
            if (input_adc_values[1] > input_adc_values[3]):
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
            elif (input_adc_values[3] > input_adc_values[1]):
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
               
            ########################## IMPORTANT ##########################
            # Backup in case Q1 and Q3 are equal; Pan in direction; Potential for error here
            else:
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.STOP)
                
            return False
        
        # Q2/Q3: Pan Left
        elif (isBright == [False, False, True, True]):
            self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
            return False
        
    
    def decode_darkness_into_action(self, input_adc_values, isDark):
        """Determine movement by evaluating darkest quadrants

        Args:
            input_adc_values list(int): ADC values corresponding to sensor analog voltages
            isDark list(bool): Separated by quadrant; True if below darkness threshold, otherwise false

        Returns:
            bool: True if aligned_quadrant matches brightest; False if not
        """  
        
        '''
        ORGANIZING THOUGHTS
        ----------------------------------

        

        Q3          |      Q0 
                    |
              ------|--------
                    |
        Q2 *Dark    |      Q1


        Cases:
            Single Quadrant below dark thresh:
                Q0: Pan Left if Q1 < Q3; Pan Right if Q3 < Q1
                Q1: Pan Left
                Q2: Return True
                Q3: Pan Right

            Two Quadrants above dark thresh:
                Q0/Q1: Pan Left
                Q0/Q2: If Q2 darkest, Return True; Else, Pan Left if Q1 < Q3; Pan Right if Q3 < Q1
                Q0/Q3: Pan Right
                Q1/Q2: Return True if Q2 Darkest; Else pan Left
                Q1/Q3: Pan Left if Q1 < Q3; Pan Right if Q3 < Q1
                Q2/Q3: Return True if Q2 Darkest; Else Pan Right
        '''   
        
        print("DARK MODE ENGAGED")
        
        # Q0: Pan Left if Q1 < Q3; Pan Right if Q3 < Q1
        if (isDark == [True, False, False, False]):
            if (input_adc_values[1] < input_adc_values[3]):
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
            elif (input_adc_values[3] < input_adc_values[1]):
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
            
            ########################## IMPORTANT ##########################
            # Backup in case Q1 and Q3 are equal; Pan in direction; Potential for error here
            else:
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.STOP)
                
            return False
            

        # Q1: Pan Left
        elif (isDark == [False, True, False, False]):
            self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
            return False

        # Q2: Return True
        elif (isDark == [False, False, True, False]):
            return True
        
        # Q3: Pan Right
        elif (isDark == [False, False, False, True]):
            self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
            return False
        
        # Q0/Q1: Pan Left
        elif (isDark == [True, True, False, False]):
            self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
            return False
        
        # QQ0/Q2: If Q2 darkest, Return True; Else, Pan Left if Q1 < Q3; Pan Right if Q3 < Q1
        elif (isDark == [True, False, True, False]):
            if (input_adc_values[2] < input_adc_values[0]):
                return True
            else:
                if (input_adc_values[1] < input_adc_values[3]):
                    self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
                elif (input_adc_values[3] < input_adc_values[1]):
                    self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
                
                ########################## IMPORTANT ##########################
                # Backup in case Q1 and Q3 are equal; Pan in direction; Potential for error here
                else:
                    self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.STOP)
                    
                return False
        
        
        # Q0/Q3: Pan Right
        elif (isDark == [True, False, False, True]):
            self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
            return False
        
        # Q1/Q2: Return True if Q2 Darkest; Else pan Left
        elif (isDark == [False, True, True, False]):
            if (input_adc_values[2] < input_adc_values[1]):
                return True
            else:
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
                return False
        
        # Q1/Q3: Pan Left if Q1 < Q3; Pan Right if Q3 < Q1
        elif (isDark == [False, True, False, True]):
            if (input_adc_values[1] < input_adc_values[3]):
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
            elif (input_adc_values[3] < input_adc_values[1]):
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
                
            ########################## IMPORTANT ##########################
            # Backup in case Q1 and Q3 are equal; Pan in direction; Potential for error here
            else:
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.STOP)    
        
            return False
        
        # Q2/Q3: Return True if Q2 Darkest; Else Pan Right
        elif (isDark == [False, False, True, True]):
            if (input_adc_values[2] < input_adc_values[3]):
                return True
            else:
                self.__stepper_controller.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
                return False
        
        # If no other condtions met, switch to camera tracking
        else:
            return True
        
    def get_stepper_controller(self):
        """ Gets __stepper_controller member variable.

        @return    tuple(bool)
        """
        return self.__stepper_controller
