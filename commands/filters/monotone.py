from typing import ClassVar
from commands.artifacts import parsed_data


def monotone(parameter_name: str, filename: str, row_parser_class: ClassVar) -> bool:
    data = parsed_data(row_parser_class, filename)
    uts = data.get(parameter_name, transposed=True)[0]
    for idx in range(1, len(uts)):
        if uts[idx] <= uts[idx - 1]:
            return False
    return True
