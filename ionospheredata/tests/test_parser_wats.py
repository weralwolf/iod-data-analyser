from os.path import join, abspath, dirname
from unittest import TestCase

from ionospheredata.parser import FileParser, SourceWATSRow

TESTDATAPATH = abspath(join(dirname(__file__), 'test_data'))


class TestParserWATS(TestCase):
    def test_simple(self):
        parser = FileParser(SourceWATSRow, join(TESTDATAPATH, '1981220_de2_wats_2s_v01.asc'))

        utsod = parser.get('ut_of_day')
        self.assertEqual(utsod.shape, (2, 1))
        self.assertEqual(utsod[0][0], 57240718)
        self.assertEqual(utsod[1][0], 57248718)

        uts = parser.get('ut')
        self.assertEqual(uts.shape, (2, 1))
        self.assertEqual(uts[0][0], 366220440.718)
        self.assertEqual(uts[1][0], 366220448.718)
