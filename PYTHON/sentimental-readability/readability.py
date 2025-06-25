import string


def main():
    # Getting text, letters, words, and sentences
    text = input("Text: ")
    L = count_letters(text)
    W = count_words(text)
    S = count_sentences(text)

    # Calculating averages
    L_avg = (L / W) * 100
    S_avg = (S / W) * 100

    # Applying Coleman-Liau index
    level = 0.0588 * L_avg - 0.296 * S_avg - 15.8
    X = round(level)

    # Printing grade level according to X
    if X > 16:
        print("Grade 16+")
    elif X < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {X}")


def count_letters(text):
    # Keeping track of letters
    letters = 0
    # Counting the number of letters
    for char in text:
        if char.isalpha():
            letters += 1
    return letters


def count_words(text):
    # Keeping track of words
    words = 0
    # Counting the number of words
    for char in text:
        if char.isspace():
            words += 1
    words += 1  # Add 1 to account for the last word
    return words


def count_sentences(text):
    # Keeping track of sentences
    sentences = 0
    # Counting the number of sentences
    for char in text:
        if char in [".", "!", "?"]:
            sentences += 1
    return sentences


main()
