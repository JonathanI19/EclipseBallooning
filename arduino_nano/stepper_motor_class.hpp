/* @ file: stepper_motor_class

   @ brief: Implements class for stepper motor control.
            Target board : AtMega-based Arduinos
            Stepper      : 28BYJ-48
            Driver       : ULN2003
*/

#ifndef STEPPER_MOTOR_H
#define STEPPER_MOTOR_H

// DEFINES
#define WINDING_A 0 
#define WINDING_B 2
#define WINDING_C 1
#define WINDING_D 3

/* The StepperMotor class.

Continuously rotates stepper motor using
standard blocking delay functions.
*/
class StepperMotor
{

  public:

  /* Constructor */
  StepperMotor()
  {

    // set PORTB as output
    DDRB = (1<<WINDING_A) | (1<<WINDING_B) | (1<<WINDING_C) | (1<<WINDING_D);
  }

  /* Rotate the motor clockwise one step.
  @return None
  */
  void rotate_cw()
  {
    PORTB = (1<<WINDING_A) | (1<<WINDING_C);
    _delay_ms(5);
    PORTB = (1<<WINDING_A) | (1<<WINDING_D);
    _delay_ms(5);
    PORTB = (1<<WINDING_B) | (1<<WINDING_D);
    _delay_ms(5);
    PORTB = (1<<WINDING_B) | (1<<WINDING_C);
    _delay_ms(5);
  }
  
  /* Rotate the motor clockwise one step.
  @return None
  */
  void rotate_ccw()
  {
    PORTB = (1<<WINDING_B) | (1<<WINDING_C);
    _delay_ms(5);
    PORTB = (1<<WINDING_B) | (1<<WINDING_D);
    _delay_ms(5);
    PORTB = (1<<WINDING_A) | (1<<WINDING_D);
    _delay_ms(5);
    PORTB = (1<<WINDING_A) | (1<<WINDING_C);
    _delay_ms(5);
  }
};

#endif