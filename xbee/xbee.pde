/**
   Xbee.pde - Basic mote functionality for Arduino.

   Reads data from a button and reports it to the network.
 */

#include <XBee.h>

const int LED = 13;

XBee xb = XBee();
XBeeResponse response = XBeeResponse();
XBeeAddress64 addr64 = XBeeAddress64(0x13A200, 0x406162A4);
uint8_t payload[] = { 'H', 'i'};
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

void setup(){
  pinMode(LED, OUTPUT);
  xb.begin(9600);
}

void loop(){
  Serial.print("Hi");
  delay(1000);
}
