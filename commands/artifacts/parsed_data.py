from typing import ClassVar
from commands.utils.cache import LocalCache
from commands.parsers.file_parser import FileParser


@LocalCache
def parsed_data(row_parser_class: ClassVar, filename: str):
    return FileParser(row_parser_class, filename)
