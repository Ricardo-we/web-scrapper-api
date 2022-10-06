import re

def discard_items_by_regex(regex, items: list,):
    regex = re.compile(regex)
    filtered_items = [single_item for single_item in items if not regex.match(single_item)]
    return filtered_items
