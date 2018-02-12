from os.path import abspath
from os.path import dirname
from os.path import join
from unittest import TestCase

from ionospheredata.parser import FileParser
from ionospheredata.parser import WATSRow

TESTDATAPATH = abspath(join(dirname(__file__), 'test_data'))

class TestParserWATS(TestCase):
    def test_simple(self):
        parser = FileParser(WATSRow, join(TESTDATAPATH, '1981220_de2_wats_2s_v01.asc'))
        uts = parser.get('ut')
        self.assertEqual(uts.shape, (2, 1))
        self.assertEqual(uts[0][0], 57240718)
        self.assertEqual(uts[1][0], 57248718)
