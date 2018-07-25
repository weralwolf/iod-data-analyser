from typing import List
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.utils.logger import logger
from commands.settings.checks import NACS_TEST_FILES_OF_THE_DAY
from commands.artifacts.sampled_day import make_deltas, sampled_day

from numpy import all


def sampled_dat_continuity_params(source_marker: str, year: int, day: int, sampling: int, *continuity_params: List[str]):
    for chunk in sampled_day(source_marker, year, day, sampling, *continuity_params):
        ut = chunk.get('ut', transposed=True)[0] / 1000
        deltas = make_deltas(ut)
        logger.error(list(deltas))
        assert all(deltas == sampling)


def test_sampled_day_continuity_params_1():
    year, day = list(NACS_TEST_FILES_OF_THE_DAY.keys())[0]
    sampled_dat_continuity_params(DE2_SOURCE_NACS, year, day, 1)


def test_sampled_dat_continuity_params_2():
    year, day = list(NACS_TEST_FILES_OF_THE_DAY.keys())[0]
    sampled_dat_continuity_params(DE2_SOURCE_NACS, year, day, 2)


def test_sampled_dat_continuity_params_3():
    year, day = list(NACS_TEST_FILES_OF_THE_DAY.keys())[0]
    sampled_dat_continuity_params(DE2_SOURCE_NACS, year, day, 3)


def test_sampled_dat_continuity_params_4():
    year, day = list(NACS_TEST_FILES_OF_THE_DAY.keys())[0]
    sampled_dat_continuity_params(DE2_SOURCE_NACS, year, day, 4)
