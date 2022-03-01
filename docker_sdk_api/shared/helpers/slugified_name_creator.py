import re


def create_slugified_name(name: str)-> str:
    return re.sub('[^A-z0-9 -]', '', name).lower().replace(" ", "_")
