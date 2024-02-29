/* @ file: solar_sensor_adc.ino

   @ brief: Reads four analog voltage signals and
            performs some initial processing to
            identify largest voltage.
            Target board : AtMega-based Arduinos
*/

//INCLUDES
#include <stdio.h>

// internal buffer size
#define MEM 10

// analog input pins
#define Q1_IN 0
#define Q2_IN 1
#define Q3_IN 2
#define Q4_IN 3

// enable LED indicators
#define LEDS_ON 1

// digital LED output pins
#define Q1_OU 8
#define Q2_OU 9
#define Q3_OU 10
#define Q4_OU 11

/* The CircularBuffer class.

Implements a circular buffer data
structure for keeping the MEM most
recent results in memory.
*/

class CircularBuffer {

  private:

  unsigned int *buffer;
  unsigned int buff_size;
  unsigned int ind_to_insert;

  public:

  /* Constructor */
  CircularBuffer(unsigned int size) : buff_size(size), ind_to_insert(0) {

    // create the buffer and place it on the heap
    this->buffer = new unsigned int[size];

    // initialize buffer with all zeros
    for (int i = 0; i < size; i++) {
      this->buffer[i] = 1;
    }
  }

  /* Insert new element into buffer.
  @param val    [unsigned int] new value
  @return None
  */
  void insert(unsigned int val) {
    this->buffer[this->ind_to_insert] = val;
    this->ind_to_insert = (this->ind_to_insert + 1) % this->buff_size;
  }

  /* Extract a specific element from buffer.
  @param pst    [unsigned int] offset from current insert index
  @return       [unsigned int] buffer element
  */
  unsigned int get_element(unsigned int pst) {
    unsigned int ind_to_read = (this->buff_size + this->ind_to_insert - pst - 1) % this->ind_to_insert;
    return this->buffer[ind_to_read];
  }

  /* Find the mode of the buffer values.
  @return [unsigned int] mode (i.e., most frequent element)
  */
  unsigned int get_mode() {

    // count the number of times each quadrant value occurs
    unsigned int count[4] = {0, 0, 0, 0};
    for (int i = 0; i < buff_size; i++) {
      if (this->buffer[i] == 1) {
        count[0]++;
      }
      else if (this->buffer[i] == 2) {
        count[1]++;
      }
      else if (this->buffer[i] == 3) {
        count[2]++;
      }
      else {
        count[3]++;
      }
    }

    // return the max quadrant
    unsigned int max = count[0];
    unsigned int qmx = 1;

    // find the maximum quadrant
    for (int i = 1; i < 4; i++) {
      if (count[i] > max) {
          max = count[i];
          qmx = i+1;
      }
    }

    // return the max
    return qmx;
  }
};

// GLOBAL VARIABLES
unsigned int analog_pins[4] = {Q1_IN, Q2_IN, Q3_IN, Q4_IN};
unsigned int led_pins   [4] = {Q1_OU, Q2_OU, Q3_OU, Q4_OU};
//char         *headers   [4] = {"Q1: ", "Q2: ", "Q3: ", "Q4: "};
unsigned int q_vals     [4] = {0, 0, 0, 0};
unsigned int global_max     = 1;
char adc_vals_str[20];

CircularBuffer filter(MEM);

void indicate_bright() {

  // init local variables
  unsigned int max = q_vals[0];
  unsigned int qmx = 1;

  // find the maximum quadrant
  for (int i = 1; i < 4; i++) {
    if (q_vals[i] > max) {
      max = q_vals[i];
      qmx = i+1;
    }
  }

  // insert new max into buffer
  filter.insert(qmx);

  // find the mode of the buffer
  global_max = filter.get_mode();

  // turn on LEDs based on max quadrant
  switch (global_max) {
    case 1 :
      digitalWrite(Q1_OU, HIGH);
      digitalWrite(Q2_OU, LOW);
      digitalWrite(Q3_OU, LOW);
      digitalWrite(Q4_OU, LOW);
      break;
    case 2 :
      digitalWrite(Q1_OU, LOW);
      digitalWrite(Q2_OU, HIGH);
      digitalWrite(Q3_OU, LOW);
      digitalWrite(Q4_OU, LOW);
      break;
    case 3 :
      digitalWrite(Q1_OU, LOW);
      digitalWrite(Q2_OU, LOW);
      digitalWrite(Q3_OU, HIGH);
      digitalWrite(Q4_OU, LOW);
      break;
    default :
      digitalWrite(Q1_OU, LOW);
      digitalWrite(Q2_OU, LOW);
      digitalWrite(Q3_OU, LOW);
      digitalWrite(Q4_OU, HIGH);
  }
}

void setup() {

  // init serial communications
  Serial.begin(9600);

  // setup digital pins for LED indicators
  pinMode(Q1_OU, OUTPUT);
  pinMode(Q2_OU, OUTPUT);
  pinMode(Q3_OU, OUTPUT);
  pinMode(Q4_OU, OUTPUT);
}

void loop() {

  // read in the analog pins
  for (int i = 0; i < 4; i++) {
    q_vals[i] = analogRead(analog_pins[i]);
  }

  // indicate the maximum quadrant
  if (LEDS_ON) {
    indicate_bright();
  }

  // ship ADC values via serial
  sprintf(adc_vals_str, "%d,%d,%d,%d", q_vals[0], q_vals[1], q_vals[2], q_vals[3]);
  Serial.println(adc_vals_str);
  
  // for (int i = 0; i < 4; i++) {
  //   Serial.print(headers[i]);
  //   Serial.println(q_vals[i]);
  // }
}
