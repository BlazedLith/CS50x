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

    // For printing the pyramids
    for (int i = 1; i <= n; i++)
    {
        // For printing the spaces before right aligned pyramid
        for (int j = 1; j <= n - i; j++)
        {
            printf(" ");
        }
        // For printing the right aligned pyramid
        for (int k = 1; k <= i; k++)
        {
            printf("#");
        }
        // For printing the spaces after the right aligned pyramid
        printf("  ");
        // For printing the left aligned pyramid
        for (int l = 0; l < i; l++)
        {
            printf("#");
        }
        // For switching to new line
        printf("\n");
    }
}
