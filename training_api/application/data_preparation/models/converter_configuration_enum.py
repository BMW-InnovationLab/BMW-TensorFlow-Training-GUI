from enum import Enum


class ConverterConfigurationEnum(Enum):
    """
        A class Enum used to get supported labels type  and corresponding format
    """
    xml: str = "pascal"
    json: str = "json"

    @classmethod
    def is_name_valid(cls, requested_format_name: str) -> bool:
        format_name: bool = any(requested_format_name.lower().strip() == formats.value
                                for formats in cls)
        return format_name
