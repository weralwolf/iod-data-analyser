from io import StringIO
from os import unlink
from tempfile import NamedTemporaryFile
from commands.parsers import FileParser, FileWriter
from commands.parsers.de2 import SampledNACSRow

from numpy import array

# 'ut', 'o_dens', 'o_err', 'n2_dens', 'n2_err', 'he_dens', 'he_err', 'n_dens', 'n_err', 'ar_dens',
# 'ar_err', 'orbit', 'alt', 'lat', 'lon', 'lst', 'lmt', 'l_sh', 'inv_lat', 'sza'
NACS_SAMPLED_DATA = array([[
    367133148.16, 746701.1, 23.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 233.0, 862.77, 21.56,
    111.85, 12.8, 12.8, 1.11, 18.54, 14.6
], [
    367133155.16, 751773.0, 24.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 233.0, 860.76, 21.97,
    111.82, 12.8, 12.8, 1.12, 18.84, 14.8
], [
    367133157.16, 771628.7, 26.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 233.0, 860.18, 22.09,
    111.81, 12.8, 12.8, 1.12, 18.93, 14.9
]])


def test_writer_nacs():
    datafile = StringIO()
    fw = FileWriter(SampledNACSRow, NACS_SAMPLED_DATA)
    fw.reflect(datafile)
    data_result = '  367133148.160     746701.100  23.500          0.000   0.000          0.000   0.000          0.000   0.000         0.000   0.000    233  862.770   21.560  111.850 12.800 12.800    1.110   18.540  14.600\n  367133155.160     751773.000  24.000          0.000   0.000          0.000   0.000          0.000   0.000         0.000   0.000    233  860.760   21.970  111.820 12.800 12.800    1.120   18.840  14.800\n  367133157.160     771628.700  26.500          0.000   0.000          0.000   0.000          0.000   0.000         0.000   0.000    233  860.180   22.090  111.810 12.800 12.800    1.120   18.930  14.900\n'  # noqa: E501
    assert datafile.getvalue() == data_result


def test_write_read():
    tmp_file = NamedTemporaryFile(mode='w', delete=False)
    tmp_file_name = tmp_file.name

    fw = FileWriter(SampledNACSRow, NACS_SAMPLED_DATA)
    fw.reflect(tmp_file)

    tmp_file.close()

    fp = FileParser(SampledNACSRow, tmp_file_name)
    ut = fp.get('ut')
    assert ut[0] == 367133148.16
    assert ut[1] == 367133155.16
    assert ut[2] == 367133157.16
    unlink(tmp_file_name)
