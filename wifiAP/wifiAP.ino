#include <WiFi.h>
#include <WiFiAP.h>

#define LED 2

const char *ssid = "esp32";
const char *password = "ciNNam0n2412";

void blinking(int);

void setup()
{
  pinMode(LED, OUTPUT);

  blink(1);

  if(!WiFi.softAP(ssid, password))
  {
    log_e("Soft AP creation failed");
    while(1);
  }
  else
  {
    blink(2);
  }

  IPAddress myIP = WiFi.softAPIP();

  blink(3);
}

void loop()
{
}

void blink(int x)
{
  for(int i = 0; i < x; i++)
  {
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    delay(500);
  }
}

