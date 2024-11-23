#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <TinyGPS++.h>

TinyGPSPlus gps;
SoftwareSerial SerialGPS(4, 5); 
const char* ssid = "vivo V27";
const char* password = "bhotu1008";

float Latitude, Longitude;
int year, month, date, hour, minute, second;
String DateString, TimeString, LatitudeString, LongitudeString;

WiFiServer server(80);

void setup() {
  Serial.begin(9600);         
  SerialGPS.begin(9600);      
  Serial.println();


  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();             
  Serial.println("Server started");
}

void loop() {
  
  while (SerialGPS.available() > 0) {
    if (gps.encode(SerialGPS.read())) {
     
      if (gps.location.isValid()) {
        Latitude = gps.location.lat();
        Longitude = gps.location.lng();
        LatitudeString = String(Latitude, 6);
        LongitudeString = String(Longitude, 6);
      }

    ]
      if (gps.date.isValid()) {
        DateString = "";
        date = gps.date.day();
        month = gps.date.month();
        year = gps.date.year();

        if (date < 10) DateString += '0';
        DateString += String(date) + " / ";

        if (month < 10) DateString += '0';
        DateString += String(month) + " / ";

        DateString += String(year);
      }

     
      if (gps.time.isValid()) {
        TimeString = "";
        hour = gps.time.hour() + 5; 
        minute = gps.time.minute();
        second = gps.time.second();

        if (hour < 10) TimeString += '0';
        TimeString += String(hour) + " : ";

        if (minute < 10) TimeString += '0';
        TimeString += String(minute) + " : ";

        if (second < 10) TimeString += '0';
        TimeString += String(second);
      }
    }
  }


  WiFiClient client = server.available();
  if (!client) return;  

  String response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
  response += "<!DOCTYPE html><html><head><title>NEO-6M GPS Readings</title><style>";
  response += "table, th, td {border: 1px solid blue;}</style></head><body>";
  response += "<h1 style='font-size:300%; text-align:center;'>NEO-6M GPS Readings</h1>";
  response += "<p style='font-size:150%; text-align:center;'><b>Location Details</b></p>";
  response += "<table align='center' style='width:50%;'><tr><th>Latitude</th><td align='center'>";
  response += LatitudeString + "</td></tr><tr><th>Longitude</th><td align='center'>";
  response += LongitudeString + "</td></tr><tr><th>Date</th><td align='center'>";
  response += DateString + "</td></tr><tr><th>Time</th><td align='center'>";
  response += TimeString + "</td></tr></table>";

 
  if (gps.location.isValid()) {
    response += "<p align='center'><a style='color:red; font-size:125%;' href='http://maps.google.com/maps?&z=15&mrt=yp&t=k&q=";
    response += LatitudeString + "+" + LongitudeString;
    response += "' target='_top'>Click here</a> to open the location in Google Maps.</p>";
  }

  response += "</body></html>\n";

 
  client.print(response);
  delay(100);  
}