#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>

// define os pinos de entrada do sensor
const int sensorPin = 2;

// inicializa as variáveis
unsigned int rpm;
unsigned long timeold;
volatile int pulses;

// configuração do display TFT
#define TFT_CS 10
#define TFT_RST 9
#define TFT_DC 8
Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

void setup() {
  Serial.begin(9600); // inicia a comunicação serial
  attachInterrupt(digitalPinToInterrupt(sensorPin), rpm_fan, RISING); // configura a interrupção
  timeold = millis(); // inicializa o tempo
  
  tft.initR(INITR_BLACKTAB); // inicializa o display
  tft.setRotation(1); // define a orientação do display
  tft.fillScreen(ST7735_BLACK); // preenche a tela de preto
  tft.setTextSize(2); // define o tamanho do texto
}

void loop() {
  // calcula a velocidade em RPM (rotações por minuto)
  rpm = 30*1000/(millis() - timeold)*pulses;
  
  // exibe a velocidade no display TFT
  tft.setCursor(0, 0);
  tft.setTextColor(ST7735_WHITE);
  tft.print("Velocidade:");
  tft.setCursor(0, 20);
  tft.print(rpm);
  tft.print(" RPM");
  
  // espera 1 segundo antes de calcular a velocidade novamente
  delay(1000);
}

void rpm_fan() {
  // incrementa o contador de pulsos quando o sensor detecta uma rotação completa do pedal
  pulses++;
}

