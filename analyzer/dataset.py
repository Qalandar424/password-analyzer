"""Small demonstration dataset and its analysis."""

from .alphabet import get_alphabet_info
from .counting import rule_of_product, brute_force_check
from .security import entropy_bits, cracking_time_avg, format_time, get_strength


def get_dataset():
    # Demonstration examples only; not a downloaded RockYou/SecLists dataset.
    return [
        "123456", "password", "123456789", "qwerty", "12345678",
        "111111", "12345", "123123", "admin", "letmein",
        "Pass@1234", "Pakistan123", "Hello@123", "Skardu123",
        "Baltistan@2025", "P@kistan2025!", "Xy$9kLm#2pQw",
        "Strong@12345", "MyPass1234", "Qwerty@123"
    ]


def build_dataset_report():
    data = get_dataset()
    result = "DATASET TESTING (20 demonstration passwords):\n\n"
    result += (
        f"{'Password':20} {'n':>3} {'|Sigma|':>7} "
        f"{'Entropy':>8} {'Offline Time':>20} {'Strength':>12}\n"
    )
    result += "-" * 85 + "\n"

    for password in data:
        n = len(password)
        sigma, *_ = get_alphabet_info(password)
        space = rule_of_product(sigma, n)
        entropy = entropy_bits(sigma, n)
        average_time = cracking_time_avg(space, 1_000_000_000)
        strength, _, _ = get_strength(entropy)
        result += (
            f"{password:20} {n:3} {sigma:7} {entropy:7.1f} "
            f"{format_time(average_time):>20} {strength:>12}\n"
        )

    brute_total, formula_total, matches = brute_force_check()
    result += (
        f"\nBrute-Force Check: Sigma={{a,b}}, n=3 -> "
        f"Brute={brute_total}, Formula={formula_total}, Match={matches}\n"
    )
    result += "Proof idea: the rule of product gives |Sigma|^n possibilities.\n"
    return result
