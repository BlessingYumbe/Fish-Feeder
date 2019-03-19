/*
 * Fish_Feeder.ino
 * Team Fish Food Group Project
 * ENGR 114 - Winter 2019
 * Arduino Code by Jon Golobay
 * Last Edited: 3/11/19
 */

//Declare I/O
#define stp 2
#define dir 3
#define MS1 4
#define MS2 5
#define EN 6
#define green 8
#define yellow 9
#define red 10

//declare and initialize variables
int user_input = 0;
int photoresistor = 0;  
int threshold = 150;  //photoresistor threshold, determined experimentally and may depend on lighting conditions

void setup() {
  //intialize hardware setup with intial states
  Serial.begin(9600); 
  pinMode(green, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(EN, OUTPUT);
  //LEDs are active LOW, write to HIGH to initialize to off
  digitalWrite(red, HIGH);
  digitalWrite(green, HIGH);
  digitalWrite(yellow, HIGH);
  //initialize step motor
  resetMotor();
}

void loop() {
  //delay to slow down serial output
  delay(500);
  //read analog value of voltage change due to photresistor
  photoresistor = analogRead(A0);
  if(photoresistor>threshold) {
    //LED Switch: Red ON and Green/Yellow OFF
    digitalWrite(red, LOW);
    digitalWrite(green, HIGH);
    digitalWrite(yellow, HIGH);
    //output status to serial
    Serial.println("EMPTY");
    //always read serial input to ensure feed requests while feeder is empty are read and disregarded
    //failure to do so will store requests until feeder is ready and run as many times as requested
    while(Serial.available()) {
      user_input = Serial.read();
    }
  }
  
  if(photoresistor<threshold) {   
    //LED Switch: Green ON and Red/Yellow OFF
    digitalWrite(green, LOW);
    digitalWrite(yellow, HIGH);
    digitalWrite(red, HIGH);
    //output status to serial
    Serial.println("READY");
    
    //reads serial input looking for dispense trigger which is byte='1'
    while(Serial.available()) {
      user_input = Serial.read();
      if (user_input =='1') {    
        //LED Switch: Yellow ON and Green OFF
        digitalWrite(green, HIGH);
        digitalWrite(yellow, LOW);
        //Step Motor Enable
        digitalWrite(EN, LOW); 
        //output status to serial
        Serial.println("DISPENSING");
        //loop to run step motor for 800 steps(step number determined experimentally and dependent on dispense mechanism)
        for(int x= 1; x<800; x++) {
          digitalWrite(stp,HIGH); //Trigger one step
          delay(1);
          digitalWrite(stp,LOW); //Pull step pin low so it can be triggered again
          delay(1);
        }
        //output status to serial
        Serial.println("COMPLETE");
        //LED Switch: Yellow ON and Green OFF
        digitalWrite(yellow, HIGH);
        digitalWrite(green, LOW);
        //Step Motor Disable
        digitalWrite(EN, HIGH);
      }
    }      
  }
}

//function to initialze step motor to a default state
void resetMotor() {
  digitalWrite(stp, LOW);
  digitalWrite(dir, LOW); //direction pin LOW to go "forward"
  digitalWrite(MS1, HIGH);
  digitalWrite(MS2, HIGH);
  digitalWrite(EN, HIGH); //enable pin HIGH for disable
}
  
