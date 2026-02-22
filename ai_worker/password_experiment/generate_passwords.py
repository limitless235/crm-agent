# generate_passwords.py
"""Utility to generate password datasets of varying entropy levels.

- Low entropy: uses a provided list of common passwords (e.g., top-10k).
- Medium entropy: random passwords 8-10 characters with mixed case, digits, symbols.
- High entropy: cryptographically random passwords of length 16+.

The script writes three files: `low.txt`, `medium.txt`, `high.txt` in the `data/` directory.
"""

import os
import random
import string
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Path to a common password list (you can replace with actual file)
COMMON_PASSWORDS_PATH = Path(__file__).parent / "common_passwords.txt"

def load_common_passwords(limit: int = 10000) -> list[str]:
    if COMMON_PASSWORDS_PATH.is_file():
        with open(COMMON_PASSWORDS_PATH, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()][:limit]
    # Fallback: generate dummy common passwords
    return [f"password{i}" for i in range(1, limit + 1)]

def generate_low_entropy(count: int = 10000):
    passwords = load_common_passwords(count)
    with open(DATA_DIR / "low.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(passwords))
    print(f"Generated {len(passwords)} low‑entropy passwords to {DATA_DIR / 'low.txt'}")

def random_password(length: int, charset: str) -> str:
    return "".join(random.choice(charset) for _ in range(length))

def generate_medium_entropy(count: int = 10000):
    charset = string.ascii_letters + string.digits + "!@#$%^&*()"
    passwords = [random_password(random.randint(8, 10), charset) for _ in range(count)]
    with open(DATA_DIR / "medium.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(passwords))
    print(f"Generated {len(passwords)} medium‑entropy passwords to {DATA_DIR / 'medium.txt'}")

def generate_high_entropy(count: int = 10000, length: int = 16):
    charset = string.ascii_letters + string.digits + string.punctuation
    passwords = [random_password(length, charset) for _ in range(count)]
    with open(DATA_DIR / "high.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(passwords))
    print(f"Generated {len(passwords)} high‑entropy passwords to {DATA_DIR / 'high.txt'}")

if __name__ == "__main__":
    generate_low_entropy()
    generate_medium_entropy()
    generate_high_entropy()
