#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_PN532.h>
#include "mbedtls/md.h"

#define PN532_SDA 21
#define PN532_SCL 22

Adafruit_PN532 nfc(PN532_SDA, PN532_SCL);

// WLAN (Client-Modus, ESP verbindet sich zu deinem AP)
const char* WIFI_SSID = "esptest";
const char* WIFI_PASS = "419g55#P";

// Python-Server (z.B. dein Laptop), der unter http://192.168.4.2:5000/ läuft
const char* SERVER_HOST = "192.168.137.1";
const uint16_t SERVER_PORT = 5000;

// Muss zum Python-SECRET passen
const char* SHARED_SECRET = "my_shared_secret_123";

bool calcHmacSha256(const String& msg, uint8_t* out, size_t outLen) {
  if (outLen < 32) return false;

  mbedtls_md_context_t ctx;
  mbedtls_md_type_t md_type = MBEDTLS_MD_SHA256;

  mbedtls_md_init(&ctx);
  const mbedtls_md_info_t* md_info = mbedtls_md_info_from_type(md_type);
  if (!md_info) {
    mbedtls_md_free(&ctx);
    return false;
  }
  if (mbedtls_md_setup(&ctx, md_info, 1) != 0) {
    mbedtls_md_free(&ctx);
    return false;
  }

  mbedtls_md_hmac_starts(&ctx,
                          (const unsigned char*)SHARED_SECRET,
                          strlen(SHARED_SECRET));
  mbedtls_md_hmac_update(&ctx,
                          (const unsigned char*)msg.c_str(),
                          msg.length());
  mbedtls_md_hmac_finish(&ctx, out);
  mbedtls_md_free(&ctx);
  return true;
}

String bytesToHex(const uint8_t* data, size_t len) {
  String s;
  for (size_t i = 0; i < len; i++) {
    if (data[i] < 0x10) s += "0";
    s += String(data[i], HEX);
  }
  s.toLowerCase();
  return s;
}

String uidToString(const uint8_t* uid, uint8_t uidLength) {
  String s;
  for (uint8_t i = 0; i < uidLength; i++) {
    if (uid[i] >= 32 && uid[i] <= 126) {
      s += (char)uid[i];
    } else {
      // nicht druckbare Bytes z.B. als '.' oder Hex anhängen
      s += '.';
    }
  }
  return s;
}


String urlencode(const String& s) {
  String out;
  const char *hex = "0123456789ABCDEF";
  for (size_t i = 0; i < s.length(); i++) {
    char c = s[i];
    if (isalnum((unsigned char)c) || c == '-' || c == '_' || c == '.' || c == '~') {
      out += c;
    } else {
      out += '%';
      out += hex[(c >> 4) & 0x0F];
      out += hex[c & 0x0F];
    }
  }
  return out;
}

void sendUidToServer(const String& token, const String& hashHex) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi nicht verbunden, sende nicht");
    return;
  }

  HTTPClient http;
  String url = "http://" + String(SERVER_HOST) + ":" + String(SERVER_PORT) +
               "/?token=" + urlencode(token) + "&hash=" + hashHex;

  Serial.print("Request: ");
  Serial.println(url);

  http.begin(url);
  int code = http.GET();
  if (code > 0) {
    Serial.print("HTTP Code: ");
    Serial.println(code);
    String payload = http.getString();
    Serial.print("Antwort: ");
    Serial.println(payload);
  } else {
    Serial.print("HTTP Fehler: ");
    Serial.println(code);
  }
  http.end();
}


void setupNFC() {
  Wire.begin(PN532_SDA, PN532_SCL);
  delay(100);
  nfc.begin();
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (!versiondata) {
    Serial.println("PN532 nicht gefunden!");
    while (1) delay(100);
  }
  nfc.SAMConfig();
  Serial.println("PN532 bereit, halte eine Karte an den Reader...");
}

void setupWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Verbinde mit WLAN ");
  Serial.println(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("WLAN verbunden, IP: ");
  Serial.println(WiFi.localIP());
}

void processCard() {
  uint8_t uid[7];
  uint8_t uidLength;
  uint8_t keya[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };

  uint8_t success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 200);
  if (!success) {
    static unsigned long lastPrint = 0;
    if (millis() - lastPrint > 3000) {
      Serial.println("Scanne nach Karten...");
      lastPrint = millis();
    }
    return;
  }

  Serial.println();
  Serial.println("Karte erkannt!");

  Serial.print("UID Hex: ");
  for (uint8_t i = 0; i < uidLength; i++) {
    if (uid[i] < 0x10) Serial.print("0");
    Serial.print(uid[i], HEX);
    Serial.print(" ");
  }
  Serial.println();

  String token = uidToString(uid, uidLength);
  Serial.print("UID als Token-String: ");
  Serial.println(token);

  uint8_t hmac[32];
  if (!calcHmacSha256(token, hmac, sizeof(hmac))) {
    Serial.println("HMAC Berechnung fehlgeschlagen");
    return;
  }
  String hashHex = bytesToHex(hmac, sizeof(hmac));
  Serial.print("HMAC SHA-256: ");
  Serial.println(hashHex);

  sendUidToServer(token, hashHex);

  if (uidLength == 4) {
    uint8_t data[16];
    uint8_t blockNumber = 4;
    success = nfc.mifareclassic_AuthenticateBlock(uid, uidLength, blockNumber, 0, keya);
    if (success) {
      success = nfc.mifareclassic_ReadDataBlock(blockNumber, data);
      if (success) {
        Serial.print("Block "); Serial.print(blockNumber); Serial.println(" Inhalt:");
        Serial.print("HEX: ");
        for (uint8_t i = 0; i < 16; i++) {
          if (data[i] < 0x10) Serial.print("0");
          Serial.print(data[i], HEX);
          Serial.print(" ");
        }
        Serial.println();
        Serial.print("CHAR: ");
        for (uint8_t i = 0; i < 16; i++) {
          if (data[i] >= 32 && data[i] <= 126) {
            Serial.print((char)data[i]);
          } else {
            Serial.print(".");
          }
        }
        Serial.println();
      } else {
        Serial.println("Konnte Block nicht lesen");
      }
    } else {
      Serial.println("Authentifizierung fehlgeschlagen - Standard Key?");
    }
  }

  Serial.println("-------------------------------------");
  delay(3000);
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  setupWiFi();
  setupNFC();
}

void loop() {
  processCard();
  delay(100);
}
