// Configuração para a esp23 (UPDATE TO STM)
// codigo test para o modulo de radio master
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(2, 5);  // CE = IO2, CSN = IO5

const byte address[6] = "00001";
bool switchstate = 0;

void setup() {
    Serial.begin(115200);
    Serial.println("Transmitter Starting");

    SPI.begin(18, 19, 23, 5); // SCK, MISO, MOSI, CSN
    radio.begin();
    radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_LOW);
    radio.stopListening();
}

void loop() {
    switchstate = !switchstate; // alterna HIGH e LOW
    radio.write(&switchstate, sizeof(switchstate));
    Serial.print("Sent: ");
    Serial.println(switchstate ? "HIGH" : "LOW");
    delay(1000);
}