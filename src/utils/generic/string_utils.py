import re

VOCALS = ["a", "e", "i", "o", "u"]

def get_float_from_currency_format(money_formatted_value="$400.0"):
    return float(re.sub("[^0-9\.]", "", money_formatted_value))

def word_ends_with(word: str, word_group: list[str]) -> bool:
    return any(word.lower().endswith(s) for s in word_group)