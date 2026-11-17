"""Word-based password generation without GUI dependencies."""

import secrets
import string

SYMBOLS = "!@#$%^&*(){}[]?/=-,.><|\\"
DEFAULT_WORDS = ("funny", "unicorn", "banana", "house", "kitten")
DEFAULT_DIGITS = (7, 11, 67, 222, 1010)


def digit_bank_from_answers(answers):
    """Read all three number answers, while recognizing the older 12-answer save."""
    indices = (3, 4, 5) if len(answers) == 14 else (3,) if len(answers) == 12 else ()
    numbers = tuple(answers[index] for index in indices
                    if answers[index].isascii() and answers[index].isdigit())
    return numbers or DEFAULT_DIGITS


def generate(word_bank, digit_bank=DEFAULT_DIGITS, minimumLength=16,
             needUppercase=True, needDigits=True, needSymbols=True):
    """Meet the minimum length and each selected character requirement.

    Whole words are retained, so the result may exceed the minimum length.
    Choices use the operating system's random source. Strength still depends
    on the size and variety of the user's word bank.
    """
    if isinstance(minimumLength, bool) or not isinstance(minimumLength, int):
        raise ValueError("Minimum length must be a whole number.")
    if not 1 <= minimumLength <= 256:
        raise ValueError("Minimum length must be between 1 and 256.")

    words = tuple(word.strip() for word in word_bank
                  if isinstance(word, str) and word.strip())
    if not words:
        raise ValueError("Complete Set Up before generating a password.")

    digits = tuple(str(digit) for digit in digit_bank)
    if needDigits and (not digits or any(
            not digit or any(char not in string.digits for char in digit)
            for digit in digits)):
        raise ValueError("The number bank must contain non-negative integers.")

    parts = []
    length = 0
    while length < minimumLength:
        word = secrets.choice(words)
        parts.append(word)
        length += len(word)

    if needUppercase and not any(char.isupper() for part in parts for char in part):
        # Prefer capitalizing an existing letter to adding an unrelated one.
        candidates = [(i, j) for i, part in enumerate(parts)
                      for j, char in enumerate(part) if char.upper().isupper()]
        if candidates:
            i, j = secrets.choice(candidates)
            parts[i] = parts[i][:j] + parts[i][j].upper() + parts[i][j + 1:]
        else:
            parts.append(secrets.choice(string.ascii_uppercase))
    if needDigits:
        parts.append(secrets.choice(digits))
    if needSymbols:
        parts.append(secrets.choice(SYMBOLS))

    secrets.SystemRandom().shuffle(parts)
    return "".join(parts)
