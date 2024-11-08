// Definir o pino do sensor Hall
const int sensorPin = 2;  // Alterar conforme o pino que você usar
volatile int pulseCount = 0;  // Contador de pulsos
unsigned long lastTime = 0;  // Último tempo registrado
float rpm = 0;  // Valor de RPM
unsigned long currentTime = 0;  // Tempo atual

// Função para determinar o status com base no valor do RPM
String getStatus(float rpm) {
  if (rpm > 50) {
    return "AUTO";
  } else if (rpm < 40) {
    return "BAIXO";
  } else {
    return "OK";
  }
}

void setup() {
  // Inicialização do pino do sensor como entrada
  pinMode(sensorPin, INPUT);
  
  // Configuração da interrupção para contar os pulsos
  attachInterrupt(digitalPinToInterrupt(sensorPin), countPulse, RISING);  // Conta a subida do sinal
  
  // Configuração da comunicação serial
  Serial.begin(9600);
}

void loop() {
  currentTime = millis();  // Obtém o tempo atual em milissegundos

  // A cada segundo, calcula e exibe o RPM, tempo e status
  if (currentTime - lastTime >= 1000) {  
    lastTime = currentTime;

    // Calcula o RPM
    rpm = (pulseCount * 60.0);  // Como estamos contando pulsos por segundo, multiplicamos por 60 para converter para RPM

    // Obter o status com base no RPM
    String status = getStatus(rpm);

    // Envia os dados para a Serial: RPM, Tempo e Status, separados por vírgulas
    Serial.print(rpm);
    Serial.print(",");
    Serial.print(currentTime);
    Serial.print(",");
    Serial.println(status);

    // Zera o contador de pulsos para o próximo segundo
    pulseCount = 0;
  }
}

// Função que é chamada a cada pulso detectado
void countPulse() {
  pulseCount++;  // Incrementa o contador de pulsos
}
