from commands.artifacts.parsed_data import parsed_data


def monotone(parameter_name: str, filename: str, source_marker: str) -> bool:
    data = parsed_data(source_marker, filename)
    uts = data.get(parameter_name, transposed=True)[0]
    for idx in range(1, len(uts)):
        if uts[idx] <= uts[idx - 1]:
            return False
    return True
