from os.path import join
from commands.parsers import FileParser
from commands.parsers.de2 import SourceNACSRow
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.utils.resolve_data_source import resolve_data_source


def test_simple_nacs_parse() -> None:
    path, _, _, _ = resolve_data_source(DE2_SOURCE_NACS)
    parser = FileParser(SourceNACSRow, join(path, '1981295T072140_0_DE2_NACS_1S_V01.ASC'))
    utsod = parser.get('ut', 'o_dens')
    assert utsod.shape == (1546, 2)

    assert utsod[0][0] == 26573128
    assert utsod[1][0] == 26574128

    assert utsod[0][1] == 7.940923E+07
    assert utsod[1][1] == 8.019976E+07
