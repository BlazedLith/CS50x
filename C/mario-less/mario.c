#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Ask for height of pyramid
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    for (int i = 1; i <= n; i++)
    {
        // For printing spaces
        for (int j = 1; j <= n - i; j++)
        {
            printf(" ");
        }
        // For printing hashes
        for (int k = 1; k <= i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
