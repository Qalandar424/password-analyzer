"""Entropy, estimated cracking time, and password-strength scoring."""

import math


def entropy_bits(sigma, n):
    """H = n * log2(sigma), in bits."""
    if sigma <= 1 or n <= 0:
        return 0.0
    return n * math.log2(sigma)


def cracking_time_avg(space_size, guesses_per_sec):
    """Average search time estimate: |S| / (2r)."""
    if guesses_per_sec <= 0:
        return 0
    return space_size / (2 * guesses_per_sec)


def format_time(seconds):
    if seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    if seconds < 60:
        return f"{seconds:.2f} Seconds"
    if seconds < 3600:
        return f"{seconds / 60:.2f} Minutes"
    if seconds < 86400:
        return f"{seconds / 3600:.2f} Hours"
    if seconds < 31536000:
        return f"{seconds / 86400:.2f} Days"
    if seconds < 31536000 * 1000:
        return f"{seconds / 31536000:.2f} Years"
    return f"{seconds / 31536000:.2e} Years"


def get_strength(entropy):
    """Return strength label, display color, and progress percentage."""
    if entropy < 28:
        return "VERY WEAK", "#e74c3c", 15
    if entropy < 36:
        return "WEAK", "#e67e22", 30
    if entropy < 60:
        return "MEDIUM", "#f39c12", 55
    if entropy < 80:
        return "STRONG", "#2ecc71", 80
    return "VERY STRONG", "#27ae60", 100


def baseline_score(password):
    """Simple rule-based baseline score from 0 to 5."""
    score = 0
    if len(password) >= 8:
        score += 1
    if any(char.islower() for char in password) and any(char.isupper() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(not char.isalnum() for char in password):
        score += 1
    if len(password) >= 12:
        score += 1
    return score
