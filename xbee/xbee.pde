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
  delay(1000);
}
