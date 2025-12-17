"""
Secure Password Generator
=========================

A utility to generate cryptographically strong passwords with customizable
complexity requirements. It avoids ambiguous characters and ensures a mix
of character types.

Features:
- Adjustable length.
- Toggleable inclusion of uppercase, numbers, and symbols.
- Exclusion of similar characters (e.g., l, 1, I, O, 0).
- Bulk generation support.

Author: Ansu Kumar
Version: 1.0.0
Date: 2025-12-17
"""

import secrets
import string
import argparse
import sys

# --- CONFIGURATION ---
DEFAULT_LENGTH = 16
AMBIGUOUS_CHARS = "Il1O0"

def generate_password(length: int, use_upper: bool, use_digits: bool, use_symbols: bool, exclude_ambiguous: bool) -> str:
    """
    Generates a single secure password based on criteria.
    """
    alphabet = string.ascii_lowercase

    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        alphabet += string.punctuation

    if exclude_ambiguous:
        for char in AMBIGUOUS_CHARS:
            alphabet = alphabet.replace(char, "")

    if not alphabet:
        raise ValueError("No characters available to generate password. Enable at least one character set.")

    # Ensure at least one of each selected type resides in the password
    password = []
    if use_upper:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_symbols:
        password.append(secrets.choice(string.punctuation))

    # Fill the rest
    remaining_length = length - len(password)
    if remaining_length > 0:
        for _ in range(remaining_length):
            password.append(secrets.choice(alphabet))

    # Shuffle to avoid predictable patterns at start
    secrets.SystemRandom().shuffle(password)
    
    return "".join(password)

def main():
    parser = argparse.ArgumentParser(description="Generate strong, random passwords.")
    
    parser.add_argument("-l", "--length", type=int, default=DEFAULT_LENGTH, help="Password length (default: 16)")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of passwords to generate")
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true", help="Exclude numbers")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude special symbols")
    parser.add_argument("--ambiguous", action="store_true", help="Allow ambiguous characters like l, 1, O, 0")

    args = parser.parse_args()

    use_upper = not args.no_upper
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols
    exclude_ambiguous = not args.ambiguous

    print(f"🔐 Generating {args.count} password(s) with Length: {args.length}")
    print("-" * 40)

    try:
        for i in range(args.count):
            pwd = generate_password(args.length, use_upper, use_digits, use_symbols, exclude_ambiguous)
            print(f" {i+1}: {pwd}")
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
        
    print("-" * 40)
    print("⚠️  Keep these secure!")

if __name__ == "__main__":
    main()
