import unittest

from numpy import ones, array, zeros, matrix

from ionospheredata.tests.iodtc import IODTestCase


class TestIODTestCase(IODTestCase):
    def test_assert_np_ndarray_single(self):
        self.assert_np_ndarray(
            array([1, 1]),
            array([1, 1])
        )
        with self.assertRaises(AssertionError):
            self.assert_np_ndarray(
                zeros((2, )),
                zeros((3, ))
            )
        with self.assertRaises(AssertionError):
            self.assert_np_ndarray(
                zeros((2, )),
                ones((2, ))
            )

    def test_assert_np_ndarray_multy(self):
        self.assert_np_ndarray(
            ones((2, 2, 2)),
            ones((2, 2, 2))
        )
        with self.assertRaises(AssertionError):
            self.assert_np_ndarray(
                ones((2, 2, 2)),
                ones((2, 2, 1))
            )

        with self.assertRaises(AssertionError):
            self.assert_np_ndarray(
                ones((2, 2, 2)),
                zeros((2, 2, 2))
            )

    def test_assert_np_matrix(self):
        self.assert_np_matrix(
            matrix([[1, 1], [1, 1]]),
            matrix([[1, 1], [1, 1]])
        )
        with self.assertRaises(AssertionError):
            self.assert_np_matrix(
                matrix([[1, 1], [1, 1]]),
                matrix([[1, 1, 1], [1, 1, 1]])
            )


if __name__ == '__main__':
    unittest.main()
