import unittest
from ej1 import ej1_func
from parameterized import parameterized


class test_ejercicio1(unittest.TestCase):

    @parameterized.expand([
        (9, 1107),
        (2, 246),
        (0, 0),
        (11, 112233),
        (99, 1010097),
    ])
    def test1(self, number, expected):
        self.assertEqual(ej1_func(number), expected)


if __name__ == "__main__":
    unittest.main()
