from enum import Enum


class LabelsExtensionEnum(Enum):
    """
        A class Enum used to get supported labels name  and corresponding format
    """
    xml: str = "pascal"
    json: str = "json"
