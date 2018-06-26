from os.path import basename
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.settings.checks import NACS_TEST_FILES_NOT_MONOTONE
from commands.filters.monotone import monotone
from commands.artifacts.monotone_files import monotone_files


def test_monotone_files():
    files_list = monotone_files(DE2_SOURCE_NACS)

    for file in files_list:
        assert basename(file) not in NACS_TEST_FILES_NOT_MONOTONE
        assert monotone('ut', file, DE2_SOURCE_NACS)
