#include <Wire.h>
#include <Adafruit_PN532.h>

#define PN532_SDA 21
#define PN532_SCL 22

Adafruit_PN532 nfc(PN532_SDA, PN532_SCL);

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Wire.begin(PN532_SDA, PN532_SCL);
  delay(100);
  
  nfc.begin();
  
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (!versiondata) {
    Serial.println("PN532 nicht gefunden!");
    while (1);
  }
  
  Serial.println("PN532 gefunden!");
  nfc.SAMConfig();
  Serial.println("Halte eine NFC-Karte an den Reader...");
}

void loop() {
  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };
  uint8_t uidLength;
  uint8_t keya[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };
  
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 200);
  
  if (success) {
    Serial.println();
    Serial.println("Karte erkannt!");
    
    Serial.print("UID Hex: ");
    for (uint8_t i = 0; i < uidLength; i++) {
      if(uid[i] < 0x10) Serial.print("0");
      Serial.print(uid[i], HEX); 
      Serial.print(" ");
    }
    Serial.println();
    
    Serial.print("UID als CHAR: ");
    for (uint8_t i = 0; i < uidLength; i++) {
      if (uid[i] >= 32 && uid[i] <= 126) {
        Serial.print((char)uid[i]);
      } else {
        Serial.print(".");
      }
      Serial.print(" ");
    }
    Serial.println();
    
    Serial.print("UID Decimal: ");
    for (uint8_t i = 0; i < uidLength; i++) {
      Serial.print(uid[i]); 
      if(i < uidLength - 1) Serial.print(", ");
    }
    Serial.println();
    
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
            if(data[i] < 0x10) Serial.print("0");
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
          
          Serial.println("Detaillierte CHAR Ansicht:");
          for (uint8_t i = 0; i < 16; i++) {
            Serial.print("Pos "); 
            if(i < 10) Serial.print("0");
            Serial.print(i);
            Serial.print(": ");
            if (data[i] >= 32 && data[i] <= 126) {
              Serial.print("'"); Serial.print((char)data[i]); Serial.print("'");
            } else {
              Serial.print("?? (0x"); 
              if(data[i] < 0x10) Serial.print("0");
              Serial.print(data[i], HEX); 
              Serial.print(")");
            }
            Serial.println();
          }
          
        } else {
          Serial.println("Konnte Block nicht lesen");
        }
      } else {
        Serial.println("Authentifizierung fehlgeschlagen - Standard Key?");
      }
    }
    
    Serial.println("-------------------------------------");
    delay(3000);
  } else {
    static unsigned long lastPrint = 0;
    if (millis() - lastPrint > 3000) {
      Serial.println("⏳ Scanne nach Karten...");
      lastPrint = millis();
    }
  }
  
  delay(100);
}
