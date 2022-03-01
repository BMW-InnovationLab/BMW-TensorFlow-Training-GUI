from enum import Enum


# noinspection SpellCheckingInspection
class ColumnName(Enum):
    """
        A class Enum used to get column names inside the csv file
    """
    file_name: str = "filename"
    width: str = "width"
    height: str = "height"
    class_name: str = "class"
    xmin: str = "xmin"
    xmax: str = "xmax"
    ymin: str = "ymin"
    ymax: str = "ymax"
