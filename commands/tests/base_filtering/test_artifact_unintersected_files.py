from os.path import basename
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.settings.checks import NACS_TEST_FILES_INTERSECTED
from commands.artifacts.base_filtering.unintersected_files import unintersected_files


def test_unintersected_files() -> None:
    files_list = unintersected_files(DE2_SOURCE_NACS)
    files_list = list(map(basename, files_list))

    for bad_file in NACS_TEST_FILES_INTERSECTED:
        assert bad_file not in files_list
