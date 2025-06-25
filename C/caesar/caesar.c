#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Check for the number of command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Get the key
    string key_string = argv[1];

    // Check for digits
    for (int i = 0, n = strlen(key_string); i < n; i++)
    {
        if (!isdigit(key_string[i]))
        {
            printf("Key must be a non-negative integer.\n");
            return 1;
        }
    }

    // Convert key to integer
    int key = atoi(key_string);

    // Get the plaintext
    string text = get_string("plaintext: ");

    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                text[i] = ((text[i] - 'A' + key) % 26) + 'A';
            }
            else if (islower(text[i]))
            {
                text[i] = ((text[i] - 'a' + key) % 26) + 'a';
            }
        }
    }
    printf("ciphertext: %s\n", text);
}