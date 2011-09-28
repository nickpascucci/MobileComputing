/**
   Xbee.pde - Basic mote functionality for Arduino.

   Reads data from a button and reports it to the network.
 */

#include <XBee.h>

const int LED = 13;

XBee xb = XBee();
XBeeResponse response = XBeeResponse();
XBeeAddress64 addr64 = XBeeAddress64(0x13A200, 0x406162A4);
uint8_t payload[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'};
// uint8_t payload[] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
//                      0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
//                      0x10, 0x11, 0x12, 0x13};
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

void setup(){
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  xb.begin(9600);
  digitalWrite(LED, HIGH);
}

void loop(){
  xb.send(zbTx);
  // Serial.print("Hi");
  delay(1000);
}
