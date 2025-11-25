#include <stdio.h>
#include <openssl/rand.h>
#include <openssl/sha.h>

// -------------------------------------
// Random NFC UID (4- or 7-byte)
// -------------------------------------
void generate_nfc_uid(unsigned char *out, int len) {
    RAND_bytes(out, len);  // Kryptographisch sicher
}

// -------------------------------------
// SHA-256 Hash
// -------------------------------------
void hash_uid(const unsigned char *uid, int uid_len, unsigned char *out_hash) {
    SHA256(uid, uid_len, out_hash);
}

// -------------------------------------
// Hilfsfunktion zum Drucken als Hex
// -------------------------------------
void print_hex(const unsigned char *data, int len) {
    for (int i = 0; i < len; i++)
        printf("%02X", data[i]);
    printf("\n");
}

// -------------------------------------
// Main Demo
// -------------------------------------
int main() {
    // NFC UIDs
    unsigned char uid4[4];
    unsigned char uid7[7];

    generate_nfc_uid(uid4, 4);
    generate_nfc_uid(uid7, 7);

    printf("Random NFC UID 4-Byte: ");
    print_hex(uid4, 4);

    printf("Random NFC UID 7-Byte: ");
    print_hex(uid7, 7);

    // SHA-256 Hash der UIDs
    unsigned char uid4_hash[SHA256_DIGEST_LENGTH];
    unsigned char uid7_hash[SHA256_DIGEST_LENGTH];

    hash_uid(uid4, 4, uid4_hash);
    hash_uid(uid7, 7, uid7_hash);

    printf("SHA-256 Hash der UID 4-Byte: ");
    print_hex(uid4_hash, SHA256_DIGEST_LENGTH);

    printf("SHA-256 Hash der UID 7-Byte: ");
    print_hex(uid7_hash, SHA256_DIGEST_LENGTH);

    return 0;
}
