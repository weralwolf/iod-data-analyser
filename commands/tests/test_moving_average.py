from os.path import join
from commands.parsers import FileParser
from commands.artifacts import moving_average
from commands.parsers.de2 import SourceNACSRow
from commands.settings.de2 import DE2_SOURCE_NACS
from commands.utils.resolve_data_source import resolve_data_source

from numpy import abs

from .average_values import o_dens_avg


def test_moving_average() -> None:
    """
    To produce new test data you may use formula for spreadsheets (for column C2, where data at B2:B1547):
    ```
    =AVERAGE(
        INDIRECT(
            CONCATENATE("R[-", MIN(COUNT(B$2:B2), COUNT(B2:B$1547), 351) - 1, "]C[-1]"), false
        ):INDIRECT(
            CONCATENATE("R[",MIN(COUNT(B$2:B2), COUNT(B2:B$1547), 351) - 1, "]C[-1]"), false
        )
    )
    ```
    """
    path, _, _, _ = resolve_data_source(DE2_SOURCE_NACS)
    parser = FileParser(SourceNACSRow, join(path, '1981295T072140_0_DE2_NACS_1S_V01.ASC'))
    moving_average_result = moving_average(parser, 'o_dens', window_size=701)
    assert len(moving_average_result) == 1
    assert len(moving_average_result[0]) == len(o_dens_avg)
    assert all(abs([moving_average_result[0][i] - o_dens_avg[i] for i in range(len(o_dens_avg))]) < 10**-2)
