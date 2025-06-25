#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

// Define constants for JPEG signature bytes
const uint8_t jpeg_signature[] = {0xff, 0xd8, 0xff, 0xe0};

int main(int argc, char *argv[])
{
    // Check for correct command-line argument count
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <forensic_image>\n", argv[0]);
        return 1;
    }

    // Open the forensic image file
    FILE *forensic_file = fopen(argv[1], "r");
    if (forensic_file == NULL)
    {
        fprintf(stderr, "Could not open the forensic image file.\n");
        return 1;
    }

    // Initialize variables
    uint8_t buffer[BLOCK_SIZE];
    int file_counter = 0;
    FILE *output_file = NULL;

    // Create a filename buffer to store the output filename
    char filename[8];

    while (fread(buffer, 1, BLOCK_SIZE, forensic_file) == BLOCK_SIZE)
    {
        // Check for the start of a new JPEG
        if (buffer[0] == jpeg_signature[0] && buffer[1] == jpeg_signature[1] && buffer[2] == jpeg_signature[2] &&
            (buffer[3] & 0xf0) == jpeg_signature[3])
        {
            // Close the previous output file, if open
            if (output_file != NULL)
            {
                fclose(output_file);
            }

            // Create a new JPEG filename
            sprintf(filename, "%03d.jpg", file_counter++);

            // Open the new output file
            output_file = fopen(filename, "w");
            if (output_file == NULL)
            {
                fprintf(stderr, "Could not create a new JPEG file.\n");
                return 1;
            }
        }

        // Write data to the output file
        if (output_file != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, output_file);
        }
    }

    // Close any open files
    if (output_file != NULL)
    {
        fclose(output_file);
    }

    // Close the forensic image file
    fclose(forensic_file);

    return 0;
}