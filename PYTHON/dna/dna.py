import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Get the filenames from command-line arguments
    database_filename = sys.argv[1]
    sequence_filename = sys.argv[2]

    # Read database file into a variable
    database = read_csv(database_filename)

    # Read DNA sequence file into a variable
    dna_sequence = read_sequence(sequence_filename)

    # Find longest match of each STR in DNA sequence
    str_matches = {}
    for key in database[0].keys():
        if key != "name":
            str_matches[key] = longest_match(dna_sequence, key)

    # Check database for matching profiles
    matching_profile = find_matching_profile(database, str_matches)

    if matching_profile:
        print(matching_profile["name"])
    else:
        print("No match")


def read_csv(filename):
    """Read a CSV file and return its contents as a list of dictionaries."""
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def read_sequence(filename):
    """Read a DNA sequence from a text file and return it as a string."""
    with open(filename, "r") as file:
        return file.read()


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


def find_matching_profile(database, str_matches):
    """Find a matching profile in the database based on STR counts."""
    for profile in database:
        match = True
        for key, value in str_matches.items():
            if int(profile[key]) != value:
                match = False
                break
        if match:
            return profile
    return None


main()
