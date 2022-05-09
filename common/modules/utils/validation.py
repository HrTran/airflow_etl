import re


def remove_special_characters(s: str):
    return re.sub('[^a-zA-Z0-9 \n\.]', '', s)
