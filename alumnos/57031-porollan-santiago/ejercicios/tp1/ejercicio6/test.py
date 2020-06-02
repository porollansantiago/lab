import unittest
from ej6 import sort
from parameterized import parameterized


class test_sort(unittest.TestCase):

    @parameterized.expand([
        ([5,77,8,33,6,45,3], [77, 45, 33, 8, 6, 5, 3]),
        ([5,77,8,33,6,45], [77, 45, 33, 8, 6, 5]),
        ([6, 2, 10, 0, 9, 1, 0, 10], [10, 10, 9, 6, 2, 1, 0, 0])
    ])
    def test_1(self, l, expected):
        self.assertEqual(sort(l), expected)


if __name__ == "__main__":
    unittest.main()
