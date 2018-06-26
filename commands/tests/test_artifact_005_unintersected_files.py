from os.path import basename
from commands.artifacts import unintersected_files
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.settings.checks import NACS_TEST_FILES_INTERSECTED


def test_unintersected_files():
    files_list = unintersected_files(DE2_SOURCE_NACS)
    files_list = list(map(basename, files_list))

    for bad_file in NACS_TEST_FILES_INTERSECTED:
        assert bad_file not in files_list
