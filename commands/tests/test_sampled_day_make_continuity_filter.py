from os.path import join
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.artifacts.parsed_data import parsed_data
from commands.artifacts.sampled_day import make_continuity_filter
from commands.utils.resolve_data_source import resolve_data_source


def test_make_continuity_filter_empty() -> None:
    path, _, _, _ = resolve_data_source(DE2_SOURCE_NACS)
    data = parsed_data(DE2_SOURCE_NACS, join(path, '1981295T001140_0_DE2_NACS_1S_V01.ASC'))
    is_continuous = make_continuity_filter(data, [])
    assert is_continuous(3 - 3) is True
    assert is_continuous(4 - 3) is True
    assert is_continuous(5 - 3) is True
    assert is_continuous(6 - 3) is True
    assert is_continuous(7 - 3) is True
    assert is_continuous(8 - 3) is True


def test_make_continuity_filter_o_dens() -> None:
    path, _, _, _ = resolve_data_source(DE2_SOURCE_NACS)
    data = parsed_data(DE2_SOURCE_NACS, join(path, '1981295T001140_0_DE2_NACS_1S_V01.ASC'))
    is_continuous = make_continuity_filter(data, ['o_dens'])
    assert is_continuous(3 - 3) is False
    assert is_continuous(4 - 3) is False

    assert is_continuous(1698 - 3) is False
    assert is_continuous(1699 - 3) is True
    assert is_continuous(1700 - 3) is False
    assert is_continuous(1701 - 3) is False
    assert is_continuous(1702 - 3) is True
    assert is_continuous(1703 - 3) is False
    assert is_continuous(1704 - 3) is False


def test_make_continuity_filter_o_dens_he_dens() -> None:
    path, _, _, _ = resolve_data_source(DE2_SOURCE_NACS)
    data = parsed_data(DE2_SOURCE_NACS, join(path, '1981295T001140_0_DE2_NACS_1S_V01.ASC'))
    is_continuous = make_continuity_filter(data, ['o_dens', 'he_dens'])
    assert is_continuous(1698 - 3) is False
    assert is_continuous(1699 - 3) is True
    assert is_continuous(1700 - 3) is False
    assert is_continuous(1701 - 3) is False
    assert is_continuous(1702 - 3) is True
    assert is_continuous(1703 - 3) is False
    assert is_continuous(1704 - 3) is False


def test_make_continuity_filter_o_dens_he_dens_ar_dens_1() -> None:
    path, _, _, _ = resolve_data_source(DE2_SOURCE_NACS)
    data = parsed_data(DE2_SOURCE_NACS, join(path, '1981295T001140_0_DE2_NACS_1S_V01.ASC'))
    is_continuous = make_continuity_filter(data, ['o_dens', 'he_dens', 'ar_dens'])
    assert is_continuous(1698 - 3) is False
    assert is_continuous(1699 - 3) is False
    assert is_continuous(1700 - 3) is False
    assert is_continuous(1701 - 3) is False
    assert is_continuous(1702 - 3) is False
    assert is_continuous(1703 - 3) is False
    assert is_continuous(1704 - 3) is False


def test_make_continuity_filter_o_dens_he_dens_ar_dens_2() -> None:
    path, _, _, _ = resolve_data_source(DE2_SOURCE_NACS)
    data = parsed_data(DE2_SOURCE_NACS, join(path, '1981295T001140_0_DE2_NACS_1S_V01.ASC'))
    is_continuous = make_continuity_filter(data, ['o_dens', 'he_dens', 'ar_dens'])
    assert is_continuous(3094 - 3) is False
    assert is_continuous(3095 - 3) is True
    assert is_continuous(3096 - 3) is False
    assert is_continuous(3097 - 3) is False
    assert is_continuous(3098 - 3) is False
    assert is_continuous(3099 - 3) is False
    assert is_continuous(3100 - 3) is False
