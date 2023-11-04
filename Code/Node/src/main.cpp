#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h>
#include <pin_def.h>
// #include <time.h>
// #include <WiFi.h>

#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

//======================================================================//
// USER Easy Change Variables
//======================================================================//

int TX_Pwr = 10;
int sync_word = 0x14;
int SPF = 8;
int BW = 125;
int CR = 5;
int Preamble_length = 8;


#define LORA_FREQUENCY  868E6
//======================================================================//
//WiFi Settings
//======================================================================//

// const char* ssid = "Hannah van Rooyen";
// const char* password = "2468Hannah";

// void initWiFi() {
//   WiFi.mode(WIFI_STA);
//   WiFi.begin(ssid, password);
//   Serial.print("Connecting to WiFi ..");
//   while (WiFi.status() != WL_CONNECTED) {
//     Serial.print('.');
//     delay(1000);
//   }
//   Serial.println(WiFi.localIP());
// }
//======================================================================//
// Pin alocation for LoRA
//======================================================================//

#define PIN_LORA_COPI   23
#define PIN_LORA_CIPO   19
#define PIN_LORA_SCK    18
#define PIN_LORA_CS     5
#define PIN_LORA_RST    2
#define PIN_LORA_DIO0   4

//======================================================================//
// Counter Variables
//======================================================================//

// volatile int interruptCounter;  //for counting interrupt
// int totalInterruptCounter;   	//total interrupt counting
// int LED_STATE=LOW;
// hw_timer_t * timer = NULL;      //H/W timer defining (Pointer to the Structure)

// portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;
//======================================================================//

//======================================================================//
// Time Variables
//======================================================================// 
// // NTP server to request epoch time
// const char* ntpServer = "pool.ntp.org";
// // Variable to save current epoch time
// unsigned long epochTime; 
// // Function that gets current epoch time
// unsigned long getTime() {
//   time_t now;
//   struct tm timeinfo;
//   if (!getLocalTime(&timeinfo)) {
//     //Serial.println("Failed to obtain time");
//     return(0);
//   }
//   time(&now);
//   return now;
// }

// int counter = 0;
int incomingByte = 0; // for incoming serial data
String readString;


// put function declarations here:
void LEDSetup();

// void IRAM_ATTR onTimer() {      //Defining Inerrupt function with IRAM_ATTR for faster access
//   portENTER_CRITICAL_ISR(&timerMux);
//   interruptCounter++;
//   portEXIT_CRITICAL_ISR(&timerMux);
// }

void setup() {
  
  LEDSetup();

  Serial.begin (115200);
  while (!Serial);
  delay (1500);
  Serial.println ("UART1 DONE");


  Serial1.begin(9600, SERIAL_8N1, scanner_rx, scanner_tx);
  while (!Serial1);
  Serial.println ("UART2 TEST");
  Serial1.println ("UART2 TEST");

  digitalWrite(Led1Pin, HIGH); // Blue LED on

  delay (1500);
  Serial.println ("LoRa Sender");


  SerialBT.begin("Lora Node"); //Bluetooth device name
  delay (1500);
  Serial.println ("Bluetooth Started");

  LoRa.setPins (PIN_LORA_CS, PIN_LORA_RST, PIN_LORA_DIO0);
  LoRa.setSPIFrequency (20000000);

  LoRa.setSpreadingFactor(SPF);
  LoRa.setSignalBandwidth(BW);
  LoRa.setTxPower (TX_Pwr);
  LoRa.setSyncWord(sync_word);
  LoRa.setPreambleLength(Preamble_length);


  if (!LoRa.begin (LORA_FREQUENCY)) {
    Serial.println ("Starting LoRa failed!");
    while (1);
  }
  else {
    Serial.print ("LoRa initialized with frequency ");
    Serial.println (LORA_FREQUENCY);

  Serial.println("LoRa Initializing OK!");
  digitalWrite(Led2Pin, HIGH); // Red LED on

  // // Timmer setup the
  // timer = timerBegin(0, 80, true);           	// timer 0, prescalar: 80, UP counting
  // timerAttachInterrupt(timer, &onTimer, true); 	// Attach interrupt
  // timerAlarmWrite(timer, 5000000, true);  		// Match value= 1000000 for 1 sec. delay.
  // timerAlarmEnable(timer);           			// Enable Timer with interrupt (Alarm Enable)

  // initWiFi();
  // configTime(0, 0, ntpServer);
}
}
//======================================================================//

void loop() {
  Serial.println("Enter data:");
  while (Serial1.available() == 0) {
    digitalWrite(Led3Pin, LOW); // Green LED off
  }     //wait for data available
  digitalWrite(Led3Pin, HIGH); // Green LED on
  String teststr = Serial1.readString();  //read until timeout
  teststr.trim();                        // remove any \r \n whitespace at the end of the String
  Serial.println(teststr);

  // Bluetooth Send
  SerialBT.println(teststr);

  Serial.print ("Sending packet: ");
  Serial.println (teststr);

  // send packet
  LoRa.beginPacket();
  LoRa.print (teststr);
  LoRa.endPacket();
}

// Test code
// void loop() {
//   // Serial.println("Starting Timmer:");
//   if (interruptCounter > 0) {

//     portENTER_CRITICAL(&timerMux);
//     interruptCounter--;
//     portEXIT_CRITICAL(&timerMux);

//     totalInterruptCounter++;         	//counting total interrupt

//     LED_STATE= !LED_STATE;  				//toggle logic
//     digitalWrite(Led3Pin, LED_STATE); // Green LED on
//     // Serial.print("An interrupt as occurred. Total number: ");
//     // Serial.println(totalInterruptCounter);
//       // Bluetooth Send
//     // SerialBT.println(totalInterruptCounter);

//     Serial.print ("Sending packet: ");
//     Serial.println (totalInterruptCounter);
//     Serial.println (getTime());

//     // send packet
//     LoRa.beginPacket();
//     LoRa.print (getTime());
//     LoRa.endPacket();
// }
  
  // digitalWrite(Led3Pin, LOW); // Green LED off
  // sleep(500);
  // while (Serial1.available() == 0) {
  //   digitalWrite(Led3Pin, LOW); // Green LED off
  // }     //wait for data available
  

  // digitalWrite(Led3Pin, HIGH); // Green LED on
  // String teststr = itoa(counter, snum, 10);  //read until timeout
  // Serial.println(teststr);
  // teststr.trim();                        // remove any \r \n whitespace at the end of the String
  // Serial.println(teststr);
  // counter ++ ; 


// }

//======================================================================//

void LEDSetup(){
  pinMode(Led1Pin,OUTPUT);   // LED
  pinMode(Led2Pin,OUTPUT);   // LED
  pinMode(Led3Pin,OUTPUT);   // LED
}

//======================================================================//

