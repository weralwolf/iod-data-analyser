# from os.path import join
# from commands.parsers import FileParser
# from commands.artifacts import wave_decomposition
# from commands.parsers.de2 import SourceNACSRow
# from commands.settings.de2 import DE2_SOURCE_NACS
# from commands.utils.logger import logger
# from commands.artifacts.moving_average import moving_average_sequence
# from commands.utils.resolve_data_source import resolve_data_source
#
# from numpy import abs, max, sum
#
#
# def test_wave_decomposition() -> None:
#     path, _, _, _ = resolve_data_source(DE2_SOURCE_NACS)
#     parser = FileParser(SourceNACSRow, join(path, '1981295T072140_0_DE2_NACS_1S_V01.ASC'))
#     parts = wave_decomposition(parser, 'o_dens')
#     value = parser.get('o_dens', transposed=True)[0]
#     avg = moving_average_sequence(value)
#     logger.error(avg)
#     assert len(parts) > 0
#     for wave, trend, noise in parts:
#         logger.info('-------------------------------------------------')
#         logger.error('value,ma,wave,trend,noise\n' + '\n'.join(['{},{},{},{},{}'.format(value[i], avg[i], wave[i], trend[i], noise[i]) for i in range(len(wave))]))
#
#     assert False
