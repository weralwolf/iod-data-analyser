from os.path import join, abspath, dirname
from unittest import TestCase

from ionospheredata.parser import NACSRow, FileParser

TESTDATAPATH = abspath(join(dirname(__file__), 'test_data'))


class TestParserNASC(TestCase):
    def test_simple(self):
        parser = FileParser(NACSRow, join(TESTDATAPATH, '1981361T132320_0_DE2_NACS_1S_V01.ASC'))

        utsod = parser.get('ut_of_day')
        self.assertEqual(utsod.shape, (2, 1))
        self.assertEqual(utsod[0][0], 48296224)
        self.assertEqual(utsod[1][0], 48297224)

        uts = parser.get('ut')
        self.assertEqual(uts.shape, (2, 1))
        self.assertEqual(uts[0][0], 378393896.224)
        self.assertEqual(uts[1][0], 378393897.224)
