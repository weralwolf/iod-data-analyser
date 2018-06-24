import re
from os import getenv
from fnmatch import fnmatch
from os.path import join, basename
from commands.parsers import de2
from commands.settings.base import ARTIFACTS_DIR

from ionospheredata.configuration import isDir, ensureDir, assertConfig

DE2_SOURCE_NACS = 'DE2_SOURCE_NACS'
DE2_SOURCE_WATS = 'DE2_SOURCE_WATS'
DE2_PARSED_NACS = 'DE2_PARSED_NACS'

sources_map = {
    DE2_SOURCE_NACS: dict(
        path=getenv('DE2SOURCE_NACS_DIR', None),
        parser=de2.SourceNACSRow,
        selector=lambda filename: fnmatch(filename, '*.ASC'),
        features=lambda filename: dict(list(zip(
            ['year', 'day', 'hour', 'minute', 'second'],
            re.match(r'(\d{4})(\d{3})T(\d{2})(\d{2})(\d{2})_.*', basename(filename)).groups()
        ))),
    ),
    DE2_SOURCE_WATS: dict(
        path=getenv('DE2SOURCE_WATS_DIR', None),
        parser=de2.SourceWATSRow,
        selector=lambda filename: fnmatch(filename, '*.asc'),
        features=lambda filename: dict(list(zip(
            ['year', 'day'],
            re.match(r'(\d{4})(\d{3})_de2_wats.*', basename(filename)).groups()
        ))),
    ),
    DE2_PARSED_NACS: dict(
        path=getenv('NACS_DIR', join(ARTIFACTS_DIR, 'nacs')),
        parser=de2.SampledNACSRow,
        selector=lambda filename: fnmatch(filename, '*.asc'),
        features=lambda filename: dict(),
    ),
}


assertConfig(isDir(sources_map[DE2_SOURCE_NACS]['path']), 'One must set `DE2SOURCE_NACS_DIR`.')
assertConfig(isDir(sources_map[DE2_SOURCE_WATS]['path']), 'One must set `DE2SOURCE_WATS_DIR`.')
ensureDir(sources_map[DE2_PARSED_NACS]['path'])
