from unittest import TestCase


class IODTestCase(TestCase):
    def assert_np_ndarray(self, array1, array2):
        shape1 = array1.shape
        shape2 = array2.shape

        self.assertEqual(len(shape1), len(shape2))
        for i, j in zip(shape1, shape2):
            self.assertEqual(i, j)

        if len(shape1) == 1:
            for i in range(shape1[0]):
                self.assertEqual(array1[i], array2[i])
            return

        for i in range(shape1[0]):
            self.assert_np_ndarray(array1[i], array2[i])

    def assert_np_matrix(self, matrix1, matrix2):
        shape1 = matrix1.shape
        shape2 = matrix2.shape

        self.assertEqual(shape1[0], shape2[0])
        self.assertEqual(shape1[1], shape2[1])

        maxi, maxj = shape1
        for i in range(maxi):
            for j in range(maxj):
                self.assertEqual(matrix1[i, j], matrix2[i, j])
