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
    


def find_intersection_ignore_case(list1, list2):
    list1 = [field.strip().lower() for field in list1]
    list2 = [field.strip().lower() for field in list2]
    common_fields = list(set(list1) & set(list2))
    return common_fields
