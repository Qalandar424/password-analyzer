"""Detect the character classes used in a password."""

def get_alphabet_info(password):
    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbol = any(not char.isalnum() for char in password)

    alphabet_size = 0
    if has_lower:
        alphabet_size += 26
    if has_upper:
        alphabet_size += 26
    if has_digit:
        alphabet_size += 10
    if has_symbol:
        alphabet_size += 32

    return alphabet_size, has_lower, has_upper, has_digit, has_symbol
