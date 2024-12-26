# string_utils.py

def reverse_string(s):
    """Return the reverse of the given string."""
    return s[::-1]

def is_palindrome(s):
    """Check if a given string is a palindrome."""
    s = ''.join(filter(str.isalnum, s)).lower()
    return s == s[::-1]

def count_vowels(s):
    """Count the number of vowels in a given string."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)

def capitalize_words(s):
    """Capitalize the first letter of each word in the string."""
    return ' '.join(word.capitalize() for word in s.split())
