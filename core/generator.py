import random
import string


def generate_password(
    length: int,
    use_uppercase: bool,
    use_lowercase: bool,
    use_numbers: bool,
    use_symbols: bool
) -> str:
    characters = ""

    if use_uppercase:
        characters += string.ascii_uppercase

    if use_lowercase:
        characters += string.ascii_lowercase

    if use_numbers:
        characters += string.digits

    if use_symbols:
        characters += "!@#$%^&*()-_=+[]{};:,.?/"

    if not characters:
        raise ValueError("At least one character type must be selected.")

    password = "".join(random.choice(characters) for _ in range(length))

    return password


def password_strength(password: str) -> str:
    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in "!@#$%^&*()-_=+[]{};:,.?/" for c in password):
        score += 1

    if score <= 2:
        return "Weak"

    if score <= 4:
        return "Medium"

    return "Strong"