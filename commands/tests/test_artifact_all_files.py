from os.path import basename
from commands.settings.de2 import DE2_SOURCE_NACS, DE2_SOURCE_WATS
from commands.settings.checks import NACS_TEST_FILES_ALL, WATS_TEST_FILES_ALL
from commands.artifacts.all_files import all_files


def test_all_nacs_files():
    files_list = all_files(DE2_SOURCE_NACS)
    assert len(files_list) == len(NACS_TEST_FILES_ALL)
    for filename in files_list:
        assert basename(filename) in NACS_TEST_FILES_ALL


def test_all_wats_files():
    files_list = all_files(DE2_SOURCE_WATS)
    assert len(files_list) == len(WATS_TEST_FILES_ALL)
    for filename in files_list:
        assert basename(filename) in WATS_TEST_FILES_ALL
