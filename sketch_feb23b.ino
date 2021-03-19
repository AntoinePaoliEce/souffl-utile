#include <SoftwareSerial.h>
SoftwareSerial BTserial(10, 11); // RX | TX creation of a serial communication on pin 10 and 11
 
const long baudRate = 9600;  //rate of data transmission
//define colors for the RGB diode
const byte COLOR_GREEN = 0b010;
const byte COLOR_BLUE = 0b001;
const byte COLOR_RED = 0b100;

//definition of pin
#define CAP_GND A1 // ground of a sensor , by putting an analogic pin at low level we obtain a ground pin
#define CAP_OUT A2 // analog output of the sensor
#define PIN_LED_VOLT A0 // 5V alimentation of the diode, by putting an analogic pin at high level we obtain a 5V pin
//pin for the RGB diode
#define PIN_LED_R 3
#define PIN_LED_G 6
#define PIN_LED_B 5

 
void setup() 
{
  //I/O definition pin
    pinMode(CAP_GND, OUTPUT);
    pinMode(CAP_OUT,INPUT);
    pinMode(PIN_LED_R, OUTPUT);
    pinMode(PIN_LED_G, OUTPUT);
    pinMode(PIN_LED_B, OUTPUT);
    pinMode(PIN_LED_VOLT, OUTPUT);
 
    
   // create ground pin and analogic pin
    digitalWrite(PIN_LED_VOLT, HIGH);
    digitalWrite(CAP_GND, LOW);
  // diode = green
    displayColor(COLOR_GREEN);
    //set the serial communication
    BTserial.begin(baudRate);  
    Serial.begin(9600);
 
}
 
void loop()
{
  //read analog information of the sensor 
 int val = analogRead(CAP_OUT);
 
 if (val >600) //a breath is detected
 {
  displayColor(COLOR_RED); //diode = red
 }
 else if (val < 400)  // a suck is detected
 {
  displayColor(COLOR_BLUE); //diode = blue
 }
 else //neutral value
 {
   displayColor(COLOR_GREEN); // diode=green
 }
  //send info to the serial port
  BTserial.println(val);
  Serial.println(val); 
  delay(500);

}
/** Create color for the diode */
void displayColor(byte color) {

  // Assigne l'état des broches
  // Version anode commune
  digitalWrite(PIN_LED_R, !bitRead(color, 2));
  digitalWrite(PIN_LED_G, !bitRead(color, 1));
  digitalWrite(PIN_LED_B, !bitRead(color, 0));
}
