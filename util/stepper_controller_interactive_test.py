from stepper_controller import STEPPER_DIRECTION
from stepper_controller import StepperController

def main():
    
    # create a StepperController object
    my_stepper = StepperController(is_rpi = True)
    
    # get user input
    try:
        while(True):
            val = input('Enter movement command code: ')
            if (val == '0'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
            elif (val == '1'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
            elif (val == '2'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.TILT_UP)
            elif (val == '3'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.TILT_DOWN)
            elif (val == '4'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.PAN_LEFT_TILT_UP)
            elif (val == '5'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.PAN_LEFT_TILT_DOWN)
            elif (val == '6'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT_TILT_UP)
            elif (val == '7'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT_TILT_DOWN)
            else:
                my_stepper.push_movement_command(STEPPER_DIRECTION.STOP)
            my_stepper.move_steppers()
    except KeyboardInterrupt:
        my_stepper.cleanup()
        return 0
    
if __name__ == "__main__":
    main()
