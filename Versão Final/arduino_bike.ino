#include <Arduino.h>
#include <ArduinoJson.h>


#define DISTANCE_TOPIC "distance"
#define LED_TOPIC "led"
#define LIST_TOPIC "list"
#define SENSOR_READ_INTERVAL_MS 100

unsigned long previousMillis = 0;
unsigned long current = 0;
unsigned long startTrial = 0;
bool ledState = false;
bool startFlag = false;
int distance = 0;
int rpmMin = 0;
int rpmMax = 0;
int acquisitionTime = 0;
char payload_dist[10];
int count = 0;


const int sensorPin = 2; // Pino do sensor Hall
const int numReadings = 4; // Número de leituras para calcular a média
volatile unsigned long pulseTime[numReadings]; // Array para armazenar os tempos dos pulsos
volatile int pulseIndex = 0; // Índice atual no array
volatile bool pulseDetected = false; // Flag para indicar detecção de pulso
unsigned long lastPulseTime = 0; // Tempo do último pulso
float rpmArray[4] = {0,0,0,0};
float rpm = 0;
unsigned long currentTime = 0;

void handlePulse();



void setup()
{
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(sensorPin, INPUT_PULLUP);
  pulseTime[1] = 0;
  }

void loop()
{
  if (Serial.available() > 0)
  {
    String serialData = Serial.readStringUntil('\n');

    // Fazer o parsing do JSON
    DynamicJsonDocument doc(128);
    DeserializationError error = deserializeJson(doc, serialData);

    // Verificar se o parsing foi bem-sucedido
    if (error)
    {
      Serial.print("Falha ao fazer o parsing do JSON: ");
      Serial.println(error.c_str());
      return;
    }

    // Extrair os dados do JSON e salvar nas variáveis
    rpmMin = doc["min"].as<int>();
    rpmMax = doc["max"].as<int>();
    acquisitionTime = doc["acquisitionTime"].as<int>();
    //Serial.println("Dados recebidos - Distância Início: " + String(rpmMin) + ", Distância Fim: " + String(rpmMax) + ", Tempo de Aquisição: " + String(acquisitionTime));
   }
    currentTime = millis();
    if(acquisitionTime > 0){
      if(!startFlag){
        startTrial = millis();  
        //Serial.println("INICIA");
        //Serial.println(rpmMin);
        //Serial.println(rpmMax);
       //Serial.println(startTrial);
       //Serial.println(startTrial + (acquisitionTime * 60UL * 1000UL));
      }
      startFlag = true;
      attachInterrupt(digitalPinToInterrupt(sensorPin), handlePulse, FALLING);
    }

    if((acquisitionTime > 0)&& ((startTrial + (acquisitionTime * 60UL * 1000UL)) <= currentTime))
    {
      //Serial.println("TERMINOU");
      Serial.println(currentTime);
      detachInterrupt(digitalPinToInterrupt(sensorPin));
      startFlag = false;
      acquisitionTime = 0;
    }
    
   /* Serial.print(startTrial + (acquisitionTime * 60UL * 1000UL));
    Serial.print("    ");
    Serial.println(currentTime);*/

    if (pulseDetected || (currentTime - lastPulseTime >= 5000)) {
    if (!pulseDetected) {
        rpm = 0;
 //       Serial.print(rpm); Serial.print("   ---   "); Serial.print(millis()); Serial.print("   ---   "); Serial.println("\u2191"); //seta para cima
    }

    pulseDetected = false;
    lastPulseTime = currentTime;
}


}


void teste(){
  Serial.println("1, funcionou");
}


void handlePulse() {

  pulseTime[0] = pulseTime[1];
  pulseTime[1] = millis();

  rpmArray[0] = (60000) / (pulseTime[1] - pulseTime[0]);

  //Serial.print(String(rpmArray[0])+","+String(rpmArray[1])+","+String(rpmArray[2])+","+String(rpmArray[3]));

  rpm = (rpmArray[0]+rpmArray[1]+rpmArray[2]+rpmArray[3])/8;
  Serial.print(int(rpm)); Serial.print(","); Serial.print((currentTime - startTrial));
  if(rpm > 0){
      if(rpm < rpmMin){
      //Serial.print(",1"); //seta para cima
        Serial.print(", AUMENTA"); //seta para cima
      }
      if(rpm > rpmMax){
        //Serial.print(",2"); // seta para baixo
        Serial.print(", DIMINUI"); //seta para baixo
      }
      if(rpmMin < rpm  && rpm < rpmMax){
        //Serial.print(",3");  //Velocidade Correta
        Serial.print(", OK"); //seta para cima
      }
      Serial.print("\n");
      rpmArray[3]= rpmArray[2];
      rpmArray[2] = rpmArray[1];
      rpmArray[1] = rpmArray[0];

      pulseDetected = true;
  }
}
