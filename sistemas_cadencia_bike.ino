#include <ArduinoJson.h>

// define os pinos de entrada do sensor
const int sensorPin = 2;

// inicializa as variáveis
unsigned int rpm;
unsigned long timeold;
volatile int pulses;

void setup() {
  Serial.begin(9600); // inicia a comunicação serial
  attachInterrupt(digitalPinToInterrupt(sensorPin), rpm_fan, RISING); // configura a interrupção
  timeold = millis(); // inicializa o tempo
}

void loop() {
  // Calcula o intervalo de tempo desde a última medição
  unsigned long timeDelta = millis() - timeold;
  
  // Calcula a velocidade em RPM (rotações por minuto)
  rpm = 30*1000/timeDelta*pulses;

  // Atualiza o tempo e reseta os pulsos
  timeold = millis();

  // Define o status com base no valor de rpm
  String status;
  if (rpm > 50) {
    status = "DIMINUIR";
  } else if (rpm < 40) {
    status = "AUMENTAR";
  } else {
    status = "OK";
  }

  // Cria um objeto JSON
  StaticJsonDocument<200> doc;
  doc["rpm"] = rpm;
  doc["tempo"] = millis();
  doc["status"] = status;

  // Serializa o objeto JSON e envia pela porta serial
  String output;
  serializeJson(doc, output);
  Serial.println(output);
  
  // Espera 1 segundo antes de calcular a velocidade novamente
  pulses = 0;
  delay(1000);
}

void rpm_fan() {
  // Incrementa o contador de pulsos quando o sensor detecta uma rotação completa do pedal
  pulses++;
}
