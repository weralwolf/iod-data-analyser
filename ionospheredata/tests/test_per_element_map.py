from numpy import array
from numpy import matrix
from numpy import ones

from ionospheredata.calc.per_element_map import map_on_array
from ionospheredata.calc.per_element_map import map_on_matrix
from ionospheredata.calc.per_element_map import map_on_ndarray
from ionospheredata.calc.per_element_map import pmap
from ionospheredata.tests.iodtc import IODTestCase


def sqrt(arg):
    return arg ** 2

class TestPerElementMap(IODTestCase):
    def test_map_on_array(self):
        res = array(map_on_array(sqrt, array([1, 2, 3, 4])))
        self.assert_np_ndarray(res, array([1, 4, 9, 16]))

    def test_map_on_matrix(self):
        res = map_on_matrix(sqrt, matrix([[1, 2], [3, 4]]))
        self.assert_np_matrix(res, matrix([[1, 4], [9, 16]]))

    def test_map_on_ndarray(self):
        res = map_on_ndarray(sqrt, ones((2, 2, 1)) * 2)
        self.assert_np_ndarray(ones((2, 2, 1)) * 4, res)

    def test_pmap(self):
        res_array = pmap(sqrt, ones((3, )) * 2)
        self.assert_np_ndarray(res_array, ones((3, )) * 4)

        res_matrix = pmap(sqrt, matrix([[1, 2], [3, 4]]))
        self.assert_np_matrix(res_matrix, matrix([[1, 4], [9, 16]]))

        res_ndarray = pmap(sqrt, ones((3, 2, 1)) * 2)
        self.assert_np_ndarray(res_ndarray, ones((3, 2, 1)) * 4)

if __name__ == '__main__':
    unittest.main()
