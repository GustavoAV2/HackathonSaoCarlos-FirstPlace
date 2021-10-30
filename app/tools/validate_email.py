import re

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def check(email_string: str) -> bool:
    if re.search(regex, email_string):
        return True
    return False
