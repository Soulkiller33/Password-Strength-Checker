import re
import argparse
import os
from colorama import Fore, Style, init
init(autoreset=True)

### Example on how to use
example_text = """
Example:
  python PasswordChecker.py --password TEST123 --wordlist YourWordlist.txt
"""

custom_usage = "PasswordChecker.py --password PASSWORD [--wordlist WORDLIST]"


### Loads custom wordlist
def load_common_passwords(wordlist_path):
    if not wordlist_path or not os.path.exists(wordlist_path):
        return set()
    with open(wordlist_path, 'r', encoding='utf-8') as f:
        return set(line.strip().lower() for line in f.readlines())


### Checks password strength
def check_password_strength(password, common_passwords):
    score = 0
    feedback = []

    if password.lower() in common_passwords:
        return Fore.RED + 'Very Weak', ['This password has been found in a common password list']

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append(Fore.YELLOW + 'Use at least 12 characters.')

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append(Fore.YELLOW + 'Add UPPERCASE letters.')

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append(Fore.YELLOW + 'Add LOWERCASE letters.')

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append(Fore.YELLOW + 'Add NUMBERS.')

    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        score += 1
    else:
        feedback.append(Fore.YELLOW + 'Add SPECIAL characters.')

    if score >= 6:
        rating = Fore.GREEN + 'Very Strong'
    elif score >= 4:
        rating = Fore.LIGHTGREEN_EX + 'Strong'
    elif score >= 3:
        rating = Fore.YELLOW + 'Moderate'
    else:
        rating = Fore.RED + 'Weak'

    return rating, feedback


### Main function
### Checks password strength
def main():
    parser = argparse.ArgumentParser(
        description='Checks passwords.',
        usage=custom_usage,
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-p', '--password', required=True, help='Your password')
    parser.add_argument('-w', '--wordlist', help='Path to wordlist')
    args = parser.parse_args()

    common_passwords = load_common_passwords(args.wordlist)
    strength, suggestions = check_password_strength(args.password, common_passwords)

    print(f'\nPassword Strength: {strength}{Style.RESET_ALL}')
    if suggestions:
        print("Suggestions:")
        for suggestion in suggestions:
            print(f'- {Fore.YELLOW}{suggestion}{Style.RESET_ALL}')

if __name__ == '__main__':
    main()
