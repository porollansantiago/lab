import unittest
from ej2 import ej2_func
from parameterized import parameterized


class test_ejercicio1(unittest.TestCase):

    @parameterized.expand([
        (9, 3, 1107),
        (2, 3, 246),
        (0, 3, 0),
        (11, 3, 112233),
        (99, 3, 1010097),
        (9, 4, 11106),
        (9, 5, 111105),
        (2, 2, 24),
        (9, 1, 9),
        (9, 2, 108),
    ])
    def test1(self, number, m, expected):
        self.assertEqual(ej2_func(number, m), expected)


if __name__ == "__main__":
    unittest.main()
