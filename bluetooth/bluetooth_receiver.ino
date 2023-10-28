/* @ file: bluetooth_receiver.ino

   @ brief: Recieves movement commands via Bluetooth
            and moves stepper motor accordingly.
            Target board : Arduino Nano BLE 33
            Stepper      : 28BYJ-48
            Driver       : ULN2003
*/

// INCLUDES
#include <ArduinoBLE.h>
#include <ContinuousStepper.h>

// DEFINES
#define DEBUG
#define RED_PIN 22     // RED = stop     
#define BLUE_PIN 24    // BLUE = ccw     
#define GREEN_PIN 23   // GREEN = cw

// ENUMS
enum STEPPER_DIRECTION {
  STOP = 0x00,
  CCW = 0x01,
  CW = 0x02
};

// GLOBAL VARIABLES (Bluetooth)
BLEService nanoService("13012F00-F8C3-4F4A-A8F4-15CD926DA146"); // BLE Service w/ UUID
BLEByteCharacteristic move_cmd_characteristic(
  "13012F03-F8C3-4F4A-A8F4-15CD926DA146",
  BLEWrite);                                                    // BLE characteristic w/ UUID

// GLOBAL VARIABLES (Stepper)  
ContinuousStepper<FourWireStepper> stepper;                     // stepper controller

void setup() {

  #ifdef DEBUG
    // start the serial monitor
    Serial.begin(9600);
    while(!Serial);
  #endif

  // initialize onboard LEDs
  pinMode(RED_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  digitalWrite(RED_PIN, LOW); // LEDs are active low
  digitalWrite(BLUE_PIN, HIGH); 
  digitalWrite(GREEN_PIN, HIGH);

  // initialize the onboard Bluetooth
  if (!BLE.begin()) {
      Serial.println("Starting BLE failed!");
      while (1);
  }

  // set advertised local name and service UUID
  // this is the name that the RPi will use to discover the Arduino
  BLE.setLocalName("Arduino Nano 33 BLE Sense");
  BLE.setAdvertisedService(nanoService);

  // add the characteristic to the service
  nanoService.addCharacteristic(move_cmd_characteristic);

  // add the service
  BLE.addService(nanoService);

  // set the initial values for the characeristic
  move_cmd_characteristic.writeValue(STOP); // default is to stop

  // start advertising via Bluetooth
  BLE.advertise();
  delay(100);
  Serial.println("ProtoStax Arduino Nano BLE LED Peripheral Service Started");

  // initialize the stepper motor
  stepper.begin(8, 10, 9, 11); // identify coil pins
  stepper.stop();              // stop by default
}

/* Updates variables that determine stepper motor movement.
@param[in]    [bool]    stop boolean
@param[in]    [uint8_t] direction code received via BT
@return       None
*/
void update_stepper_direction(bool & stop, uint8_t curr_dir) {

  // decode the direction code
  switch (curr_dir) {

    case STOP :

      // set onboard LEDs to reflect "stop" state: RED ON
      digitalWrite(RED_PIN, LOW);
      digitalWrite(BLUE_PIN, HIGH);
      digitalWrite(GREEN_PIN, HIGH);

      // stop the stepper
      stepper.stop();
      stop = true;
      break;

    case CCW   :

      // set onboard LEDs to reflect "ccw" state: BLUE ON
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(BLUE_PIN, LOW);
      digitalWrite(GREEN_PIN, HIGH);

      // set stepper speed
      stepper.spin(-200);
      stop = false;
      break;

    case CW   :

      // set onboard LEDs to reflect "cw" state: GREEN ON
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(BLUE_PIN, HIGH);
      digitalWrite(GREEN_PIN, LOW);

      // set stepper spped
      stepper.spin(200);
      stop = false;
      break;

    default   :

      // set onboard LEDs to reflect default ("stop") state: RED ON
      digitalWrite(RED_PIN, LOW);
      digitalWrite(BLUE_PIN, HIGH);
      digitalWrite(GREEN_PIN, HIGH);

      // stop the stepper
      stepper.stop();
      stop = true;
  }
}

void loop() {

  // init local variables
  uint8_t curr_dir = 0;
  bool stop = true;

  // listen for RPi BLE central service to connect:
  BLEDevice central = BLE.central();

  // if connected, proceed
  if (central) {

    Serial.print("Connected to central: ");
    Serial.println(central.address());

    // ensure connection is maintained
    while (central.connected()) {

      // wait for characteristic to be updated (i.e., RPi to send command)
      if (move_cmd_characteristic.written()) {

        // receive the command and update stepper motor direction
        Serial.println(move_cmd_characteristic.value());
        curr_dir = move_cmd_characteristic.value();
        update_stepper_direction(stop, curr_dir);
      }
      else {

        // move the stepper
        if (!stop) {
          stepper.loop();
        }
      }
    }
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
    curr_dir = 0;
    update_stepper_direction(stop, curr_dir);
    stepper.stop();
  }
}
