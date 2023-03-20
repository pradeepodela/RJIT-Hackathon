#include <ESP8266WiFi.h>

const char* ssid = "Name of Hotspot";  // change the SSID
const char* password = "Password";  // change the password

WiFiServer server(80);

void setup() {
  pinMode(16, OUTPUT);
  pinMode(5, OUTPUT);


  digitalWrite(16, LOW);
  digitalWrite(5, LOW);
  Serial.begin(9600);
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("NodeMCU is connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
  delay(3000);
}

void loop() {
  WiFiClient client;
  client = server.available();

 if (client == 1) {
    String request = client.readStringUntil('\n');
    client.flush();
    Serial.println(request);
    if (request.indexOf("ledon") != -1)
      Serial.println("LED is ON");
    {
         for (int i = 0; i < 10; i++) {
        digitalWrite(16, HIGH);
        digitalWrite(5, HIGH);
        delay(1000);
        digitalWrite(16, LOW);
        digitalWrite(5, LOW);
        delay(1000);
        }
    digitalWrite(16, LOW);
    digitalWrite(5, LOW);
    }

    if (request.indexOf("ledoff") != -1)
    { digitalWrite(16, LOW);
      Serial.println("LED is OFF");
    }
 
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println(""); 
  
    client.println("<!DOCTYPE HTML>");
    client.println("<html>");
    client.println("<head>");
    client.println("<title> Controlling LED </title>");
    client.println("</head>");
    client.println("<body align= \"center\" >");
    client.println("<h1> <font size = \"25\" face = \"Cooper\" >  NodeMCU and Wifi Network  </font> </h1> ");
    client.println("<p> <a href=\"/ledon\">  <button style=\"height:60px; background-color: yellow; width:200px; cursor: pointer\"> ON  </button> <a> </font></p> ");
    client.println("<p> <a href=\"/ledoff\"> <button style=\"height:60px; background-color: yellow; width:200px; cursor: pointer\" > OFF </button> <a> </font></p> ");
    client.println("</body>");
    client.println("</html>");

    Serial.println("Client disonnected");
    Serial.println("------------------");
    Serial.println("                  ");
       
  }
}