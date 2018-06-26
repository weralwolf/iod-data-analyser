from os.path import join
from commands.parsers import FileParser
from commands.parsers.de2 import SourceWATSRow
from commands.settings.de2 import DE2_SOURCE_WATS
from commands.utils.resolve_data_source import resolve_data_source


def test_simple_wats():
    path, _, _, _ = resolve_data_source(DE2_SOURCE_WATS)
    parser = FileParser(SourceWATSRow, join(path, '1982229_de2_wats_2s_v01.asc'))

    utsod = parser.get('ut', 'tn')
    assert utsod.shape == (4826, 2)

    assert utsod[0][0] == 9762724
    assert utsod[1][0] == 9764724

    assert utsod[0][1] == 822.8
    assert utsod[1][1] == 830.5
