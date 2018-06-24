from commands.utils.local_cache import LocalCache
from commands.parsers.file_parser import FileParser
from commands.utils.resolve_data_source import resolve_data_source


@LocalCache
def parsed_data(source_marker: str, filename: str):
    path, parser_class, selector, features_extractor = resolve_data_source(source_marker)
    return FileParser(parser_class, filename)
