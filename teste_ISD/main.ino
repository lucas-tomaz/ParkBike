const int sensorHall = 2;  // Pino do sensor (usa interrupção INT0)
volatile unsigned long ultimaDeteccao = 0;  // Guarda o tempo do último pulso
volatile float rpmInst = 0;  // RPM instantâneo

const int numValores = 4;  // Número de amostras para média móvel
float valores[numValores] = {0};  // Array de armazenagem
int indice = 0;  // Índice do array
float soma = 0;  // Soma dos valores para média móvel

void setup() {
  Serial.begin(9600);
  pinMode(sensorHall, INPUT_PULLUP);  // Usa pull-up interno

  // Configura interrupção no pino 2 para detectar borda de descida
  attachInterrupt(digitalPinToInterrupt(sensorHall), calcularRPM, FALLING);
}

void loop() {
  // Calcula média móvel do RPM
  float mediaRPM = soma / numValores;

  // Exibe os valores no monitor serial
  Serial.print("RPM Instantâneo: ");
  Serial.print(rpmInst);
  Serial.print(" | RPM Médio: ");
  Serial.println(mediaRPM);

  delay(500);  // Pequeno atraso para visualização
}

// Função chamada pela interrupção (detecção do ímã)
void calcularRPM() {
  unsigned long tempoAgora = millis();  // Obtém o tempo atual

  if (ultimaDeteccao > 0) {  // Garante que não é a primeira leitura
    unsigned long deltaT = tempoAgora - ultimaDeteccao;  // Diferença de tempo entre pulsos
    rpmInst = (60000.0 / deltaT);  // Converte para RPM (60s * 1000ms)

    // Atualiza a média móvel
    soma = soma - valores[indice] + rpmInst;
    valores[indice] = rpmInst;
    indice = (indice + 1) % numValores;  // Atualiza índice circularmente
  }

  ultimaDeteccao = tempoAgora;  // Atualiza o tempo da última detecção
}
