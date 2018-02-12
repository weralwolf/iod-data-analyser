from os.path import abspath
from os.path import dirname
from os.path import join
from unittest import TestCase

from ionospheredata.parser import FileParser
from ionospheredata.parser import NACSRow

TESTDATAPATH = abspath(join(dirname(__file__), 'test_data'))

class TestParserNASC(TestCase):
    def test_simple(self):
        parser = FileParser(NACSRow, join(TESTDATAPATH, '1981361T132320_0_DE2_NACS_1S_V01.ASC'))
        uts = parser.get('ut')
        self.assertEqual(uts.shape, (2, 1))
        self.assertEqual(uts[0][0], 48296224)
        self.assertEqual(uts[1][0], 48297224)
