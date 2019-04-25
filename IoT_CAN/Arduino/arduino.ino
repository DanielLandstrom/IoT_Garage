#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>
 
// Libraries needed
// - OneWire
// - DallasTemperature
 
//Pin 5 DS18B20 Onewire
//Pin 6 Distance Echo
//Pin 7 Distance trigger
 
// DS18B20 init
#define DS18B20_ONE_WIRE_BUS 5
OneWire DS18B20_oneWire(DS18B20_ONE_WIRE_BUS);
DallasTemperature DS18B20_sensors(&DS18B20_oneWire);
DeviceAddress DS18B20_Thermometer[10];
int DS18B20_deviceCount = 0;
unsigned long DS18B20_postingIntervalDelay = 1 * 1000; //Read and post the temperature every second second.
unsigned long DS18B20_postingIntervalTimer = 0;
 
// Distance_sensor
#define DISTANCE_echoPin 6
#define DISTANCE_trigPin 7
unsigned long DISTANCE_postingIntervalDelay = 1 * 1000; //Read and post the temperature every second second.
unsigned long DISTANCE_postingIntervalTimer = 0;
 
// Lock Sensor
int hallSensorPin = A5;
int ledPinRed =  A2;
int ledPinGreen = A3;
int state = 0;
 
void DS18B20_setup(void)
{
  DS18B20_sensors.begin();
}
 
void DISTANCE_setup(void)
{
  pinMode(DISTANCE_echoPin, INPUT);
  pinMode(DISTANCE_trigPin, OUTPUT);
}
 
void LOCK_setup(void)
{
  pinMode(ledPinRed, OUTPUT);
  pinMode(ledPinGreen, OUTPUT);
  pinMode(hallSensorPin, INPUT);
}
void DS18B20_loop(void)
{
  DS18B20_deviceCount = DS18B20_sensors.getDeviceCount();
  DS18B20_sensors.requestTemperatures();
  
  for (int i = 0; i < DS18B20_deviceCount; i++)
  {
    DS18B20_sensors.getAddress(DS18B20_Thermometer[i], i);
    //Serial.print((String)"Thermometer[" + i + "] adress ");
    //DS18B20_printAddress(DS18B20_Thermometer[i]);
    //Serial.println((String) "ejacsve/Temp[" + i + "]: " + DS18B20_sensors.getTempC(DS18B20_Thermometer[i]));
    Serial.println((String) "ejacsve/Temp: " + DS18B20_sensors.getTempC(DS18B20_Thermometer[i]));
  }
}
 
void DISTANCE_loop(void)
{
  unsigned long duration;
  float distance;
 
  digitalWrite(DISTANCE_trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(DISTANCE_trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(DISTANCE_trigPin, LOW);
 
  duration = pulseIn(DISTANCE_echoPin, HIGH);
  distance = (duration / 2) / 29.1;
  Serial.println((String) "egebant/Distance: " + distance);
}
 
void LOCK_loop(void)
{
  state = digitalRead(hallSensorPin);
  Serial.print("erohsat/Lock: ");
  Serial.println(!state);
 
  if (state == LOW)
  {
    digitalWrite(ledPinRed, HIGH);
    digitalWrite(ledPinGreen, LOW);
  }
  else
  {
    digitalWrite(ledPinRed, LOW);
    digitalWrite(ledPinGreen, HIGH);
  }
}

void setup(void)
{
  Serial.begin(9600);
  DS18B20_setup();
  DISTANCE_setup();
  LOCK_setup();
  delay(1000);
  Serial.println((String) "setup done");
}
 
void loop(void)
{
  if (millis() - DS18B20_postingIntervalTimer > DS18B20_postingIntervalDelay)
  {
    DS18B20_loop();
    DS18B20_postingIntervalTimer = millis();
  }
 
  if (millis() - DISTANCE_postingIntervalTimer > DISTANCE_postingIntervalDelay)
  {
    //DS18B20_loop();
    DISTANCE_loop();
    LOCK_loop();
    DISTANCE_postingIntervalTimer = millis();
  }
 
}
