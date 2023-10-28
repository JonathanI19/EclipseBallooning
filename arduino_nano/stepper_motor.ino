/* @ file: stepper_motor

   @ brief: Implements direct control of stepper motor
            using standard delay functions.
            Target board : AtMega-based Arduinos
            Stepper      : 28BYJ-48
            Driver       : ULN2003
*/

// INCLUDES
#include "stepper_motor_class.hpp"

// DEFINES
#define DEGUG
#define PC0 2
#define PC1 3

// ENUMS
enum STEPPER_DIRECTION {
  STOP = 0x00,
  DR0 = 0x01,
  CW = 0x02
};

// GLOBAL VARIABLES
StepperMotor stepper;
volatile uint8_t byte_code;
volatile uint8_t pc0_status;
volatile uint8_t pc1_status;

void setup()
{
  pinMode(PC0, INPUT);
  pinMode(PC1, INPUT);
  attachInterrupt(digitalPinToInterrupt(PC0), update_ISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PC1), update_ISR, CHANGE);
}

void loop()
{
  switch (byte_code)
  {
    case (CCW):
      stepper.rotate_ccw();
      break;
    case (CW):
      stepper.rotate_cw();
      break;
  }
}

void update_ISR()
{
  pc0_status = digitalRead(PC0);
  pc1_status = digitalRead(PC1);
  if (pc0_status)
  {
    byte_code = CCW;
  }
  else if (pc1_status)
  {
    byte_code = CW;
  }
  else
  {
    byte_code = STOP;
  }
}
