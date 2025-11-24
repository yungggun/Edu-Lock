#include <stdio.h>
#include <string.h>
#include <openssl/hmac.h>
#include <openssl/rand.h>

// -------------------------------------
// Random NFC UID (4- or 7-byte)
// -------------------------------------
void generate_nfc_uid(unsigned char *out, int len) {
    RAND_bytes(out, len);  // Kryptographisch sicher
}

void print_uid(const unsigned char *uid, int len) {
    for (int i = 0; i < len; i++)
        printf("%02X", uid[i]);
    printf("\n");
}

// -------------------------------------
// HMAC-SHA256
// -------------------------------------
void compute_hmac_sha256(
    const unsigned char *key, int key_len,
    const unsigned char *data, int data_len,
    unsigned char *out, unsigned int *out_len)
{
    HMAC(EVP_sha256(),
         key, key_len,
         data, data_len,
         out, out_len);
}

// -------------------------------------
// Main Demo
// -------------------------------------
int main() {
    // Beispielwerte
    const char *secret = "my_shared_secret_123";
    const char *message = "Hello from client!";

    // NFC UIDs
    unsigned char uid4[4];
    unsigned char uid7[7];

    generate_nfc_uid(uid4, 4);
    generate_nfc_uid(uid7, 7);

    printf("Random NFC UID 4-Byte: ");
    print_uid(uid4, 4);

    printf("Random NFC UID 7-Byte: ");
    print_uid(uid7, 7);

    // HMAC Ergebnis
    unsigned char hmac[EVP_MAX_MD_SIZE];
    unsigned int hmac_len = 0;

    compute_hmac_sha256(
        (unsigned char*)secret, strlen(secret),
        (unsigned char*)message, strlen(message),
        hmac, &hmac_len
    );

    printf("\nHMAC-SHA256: ");
    for (unsigned int i = 0; i < hmac_len; i++)
        printf("%02x", hmac[i]);
    printf("\n");

    return 0;
}
