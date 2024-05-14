#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

const char* ssid = "EDC_Faculty";
const char* password = "Automation&9876#";

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const int MQ2Pin = 34; // Analog pin for MQ2 sensor
const int MQ3Pin = 35; // Analog pin for MQ3 sensor

WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int MQ2Value = analogRead(MQ2Pin);
    int MQ3Value = analogRead(MQ3Pin);

    String response = "T:" + String(temperature) + ",H:" + String(humidity) + ",MQ2:" + String(MQ2Value) + ",MQ3:" + String(MQ3Value) + "\n";

    client.print("HTTP/1.1 200 OK\r\n");
    client.print("Content-Type: text/plain\r\n");
    client.print("Connection: close\r\n");
    client.print("Content-Length: ");
    client.print(response.length());
    client.print("\r\n\r\n");
    client.print(response);
    client.stop();
  }
}


