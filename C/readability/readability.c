#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_scentences(string text);

int main(void)
{
    // Getting text, letters, words and scentences
    string text = get_string("Text: ");
    int L = count_letters(text);
    int W = count_words(text);
    int S = count_scentences(text);

    // Calculating Averages
    float L_avg = (L / (float) W) * (float) 100;
    float S_avg = (S / (float) W) * (float) 100;

    // Applying Coleman-Liau index
    float level = 0.0588 * L_avg - 0.296 * S_avg - 15.8;
    int X = round(level);

    // Printing Grade level according to X
    if (X > 16)
    {
        printf("Grade 16+\n");
    }
    else if (X < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", X);
    }
}

int count_letters(string text)
{
    // Keeping track of letters
    int letters = 0;
    // Counting the number of letters
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isalpha(text[i]))
        {
            letters = letters + 1;
        }
    }
    return letters;
}

int count_words(string text)
{
    // Keeping track of words
    int words = 0;
    // Counting the number of words
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isblank(text[i]))
        {
            words = words + 1;
        }
    }
    words = words + 1;
    return words;
}

int count_scentences(string text)
{
    // Keeping track of scentences
    int scentences = 0;
    // Counting the number of scentences
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] == '!' || text[i] == '?' || text[i] == '.')
        {
            scentences = scentences + 1;
        }
    }
    return scentences;
}