import re

def parse_years_of_experience(text):
    match = re.search(r'\d+', text)

    if match:
        number = match.group()

        if number is not None:
            return int(number)
        else:
            return 0
    else:
        return -1