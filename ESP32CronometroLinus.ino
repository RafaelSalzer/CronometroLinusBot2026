#include <WiFi.h>
#include <WebSocketsServer.h>

// ---------------------------------------------------------
// Configurações do Wi-Fi (Modo Access Point) e Pino
// ---------------------------------------------------------
const char* ssid = "ESP32";      // Nome da rede Wi-Fi que o ESP32 vai criar
const char* password = "12345678"; // Senha da rede (deve ter no mínimo 8 caracteres)

const int buttonPin = 4; // Pino do botão

// Variáveis para o Debounce
int buttonState = HIGH;             
int lastButtonState = HIGH;         
unsigned long lastDebounceTime = 0; 
unsigned long debounceDelay = 50;   

// Inicializa o servidor WebSocket na porta 81
WebSocketsServer webSocket = WebSocketsServer(81);

// ---------------------------------------------------------
// Função de Eventos do WebSocket (Debug)
// ---------------------------------------------------------
void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.printf("[%u] Cliente Desconectado!\n", num);
            break;
        case WStype_CONNECTED:
            {
                IPAddress ip = webSocket.remoteIP(num);
                Serial.printf("[%u] Cliente Conectado! IP: %d.%d.%d.%d\n", num, ip[0], ip[1], ip[2], ip[3]);
            }
            break;
        case WStype_TEXT:
            Serial.printf("[%u] Recebeu: %s\n", num, payload);
            break;
    }
}

// ---------------------------------------------------------
// SETUP
// ---------------------------------------------------------
void setup() {
    Serial.begin(115200);
    pinMode(buttonPin, INPUT_PULLUP);

    // Configura o ESP32 para criar sua própria rede Wi-Fi (Modo AP)
    Serial.print("\nCriando a rede Wi-Fi: ");
    Serial.println(ssid);
    
    // Inicia o Access Point
    WiFi.softAP(ssid, password);
    
    // Pega o IP gerado (No modo AP, o padrão costuma ser 192.168.4.1)
    IPAddress IP = WiFi.softAPIP();
    
    Serial.println("Rede criada com sucesso!");
    Serial.print("Conecte o seu computador no Wi-Fi '");
    Serial.print(ssid);
    Serial.println("'");
    Serial.print("Endereço IP do ESP32 para o WebSocket: ");
    Serial.println(IP);

    // Inicia o servidor WebSocket
    webSocket.begin();
    webSocket.onEvent(webSocketEvent);
    Serial.println("Servidor WebSocket rodando na porta 81.");
}

// ---------------------------------------------------------
// LOOP
// ---------------------------------------------------------
void loop() {
    webSocket.loop();

    int reading = digitalRead(buttonPin);

    if (reading != lastButtonState) {
        lastDebounceTime = millis();
    }

    if ((millis() - lastDebounceTime) > debounceDelay) {
        if (reading != buttonState) {
            buttonState = reading;

            if (buttonState == LOW) {
                Serial.println("Botão pressionado! Enviando 'passou'...");
                webSocket.broadcastTXT("Passou");
            }
        }
    }
    
    lastButtonState = reading;
}