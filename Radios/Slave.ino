// Configuração para esp32 (UPDATE TO STM)
// codigo de test slave
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#define ledRadio 12 // LED controlado pela comunica¸c~ao

RF24 radio(2, 5); // CE = IO2, CSN = IO5

const byte address[6] = "00001";
boolean switchstate = 0;

void setup() {
    pinMode(ledRadio, OUTPUT);
    Serial.begin(115200);
    Serial.println("\nReceiver Circuit");
    SPI.begin(18, 19, 23, 5); // SCK, MISO, MOSI, CSN
    radio.begin();
    radio.openReadingPipe(0, address);
    radio.setPALevel(RF24_PA_MIN);
    radio.startListening();
}
void loop() {
    if (radio.available()) {
        radio.read(&switchstate, sizeof(switchstate));
        Serial.print("Received: ");
        Serial.println(switchstate);
        digitalWrite(ledRadio, switchstate ? HIGH : LOW);
    }
    delay(10);
}