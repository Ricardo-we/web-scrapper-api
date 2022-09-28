import re


def get_float_from_currency_format(money_formatted_value="$400.0"):
    return float(re.sub("[^0-9\.]", "", money_formatted_value))
