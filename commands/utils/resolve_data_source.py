from commands.settings.de2 import sources_map as de2_source_map


def resolve_data_source(source: str):
    if source not in de2_source_map:
        raise ValueError('No data source known with name `{}`'.format(source))
    return (
        de2_source_map[source]['path'],
        de2_source_map[source]['parser'],
        de2_source_map[source]['selector'],
        de2_source_map[source]['features'],
    )
