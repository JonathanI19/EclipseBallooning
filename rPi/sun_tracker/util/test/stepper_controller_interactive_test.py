from stepper_controller import STEPPER_DIRECTION
from stepper_controller import StepperController

def main():
    
    # create a StepperController object
    my_stepper = StepperController()
    
    # get user input
    try:
        while(True):
            val = input('Enter movement command code: ')
            if (val == '0'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.PAN_LEFT)
            elif (val == '1'):
                my_stepper.push_movement_command(STEPPER_DIRECTION.PAN_RIGHT)
            else:
                my_stepper.push_movement_command(STEPPER_DIRECTION.STOP)
            my_stepper.move_steppers()
    except KeyboardInterrupt:
        my_stepper.cleanup()
        return 0
    
if __name__ == "__main__":
    main()
