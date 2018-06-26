from os.path import basename
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.settings.checks import NACS_TEST_FILES_NOT_MONOTONE
from commands.filters.monotone import monotone
from commands.artifacts.not_monotone_files import not_monotone_files


def test_not_monotone_files():
    files_list = not_monotone_files(DE2_SOURCE_NACS)

    assert len(files_list) == len(NACS_TEST_FILES_NOT_MONOTONE)

    for file in files_list:
        assert basename(file) in NACS_TEST_FILES_NOT_MONOTONE
        assert not monotone('ut', file, DE2_SOURCE_NACS)
