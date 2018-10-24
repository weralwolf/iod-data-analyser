import logging
from os.path import basename
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.settings.checks import NACS_TEST_FILES_OF_THE_DAY
from commands.artifacts.files_of_the_day import files_of_the_day

logger = logging.getLogger(__file__)


def test_files_of_the_day() -> None:
    days = [
        (1981, 295),
        (1981, 296),
        (1981, 297),
    ]
    for year, day in days:
        files_list = files_of_the_day(DE2_SOURCE_NACS, year, day)
        files_of_this_day = NACS_TEST_FILES_OF_THE_DAY[(year, day)]

        assert len(files_list) == len(files_of_this_day)
        for filename in files_list:
            assert basename(filename) in files_of_this_day
