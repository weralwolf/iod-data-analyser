from os.path import basename
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.settings.checks import NACS_TEST_FILES_DUPLICATES
from commands.artifacts.base_filtering.deduplicated_files import deduplicated_files


def test_deduplicated_files() -> None:
    files_list = deduplicated_files(DE2_SOURCE_NACS)
    files_list = list(map(basename, files_list))

    for a, b in NACS_TEST_FILES_DUPLICATES:
        assert (a in files_list and b not in files_list) or (a not in files_list and b in files_list)
