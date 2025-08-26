// Configuração para a esp23 (UPDATE TO STM)
// Codigo de test para usar a esc

const int escPin = 4;
const int freq = 60;
const int escChannel = 0;
const int resolution = 12;

void setup() {
  Serial.begin(115200);
  ledcSetup(escChannel, freq, resolution);
  ledcAttachPin(escPin, escChannel);
}

void loop() {
  // Aciona o motor em um sentido
  ledcWrite(escChannel, 400);  // valor alto (motor gira)
  delay(2000);                 // espera 2 segundos

  // Para o motor
  ledcWrite(escChannel, 245);  // ponto neutro para ESCs comuns
  delay(1000);                 // espera 1 segundo

  // Aciona no outro sentido (se for ESC bidirecional)
  ledcWrite(escChannel, 100);  // valor mais baixo (gira no outro sentido)
  delay(2000);                 // espera 2 segundos

  // Para de novo
  ledcWrite(escChannel, 245);
  delay(1000);
}
