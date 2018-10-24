from commands.settings.de2 import DE2_SOURCE_NACS, DE2_SOURCE_WATS
from commands.settings.checks import NACS_TEST_FILES_ALL, WATS_TEST_FILES_ALL
from commands.utils.resolve_data_source import resolve_data_source


def test_source_nacs_selector() -> None:
    _, _, selector, _ = resolve_data_source(DE2_SOURCE_NACS)
    for filename in NACS_TEST_FILES_ALL:
        assert selector(filename)

    for filename in WATS_TEST_FILES_ALL:
        assert not selector(filename)


def test_source_nacs_features() -> None:
    _, _, _, extractor = resolve_data_source(DE2_SOURCE_NACS)
    for filename in NACS_TEST_FILES_ALL:
        year = filename[:4]
        day = filename[4:7]
        hour = filename[8:10]
        minute = filename[10:12]
        second = filename[12:14]
        features = extractor(filename)
        assert year == features['year']
        assert day == features['day']
        assert hour == features['hour']
        assert minute == features['minute']
        assert second == features['second']


def test_source_wats_selector() -> None:
    _, _, selector, _ = resolve_data_source(DE2_SOURCE_WATS)
    for filename in WATS_TEST_FILES_ALL:
        assert selector(filename)

    for filename in NACS_TEST_FILES_ALL:
        assert not selector(filename)


def test_source_wats_features() -> None:
    _, _, _, extractor = resolve_data_source(DE2_SOURCE_WATS)
    for filename in WATS_TEST_FILES_ALL:
        year = filename[:4]
        day = filename[4:7]
        features = extractor(filename)
        assert year == features['year']
        assert day == features['day']
