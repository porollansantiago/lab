import unittest
from ej3 import histogram
from parameterized import parameterized

class test_histogram(unittest.TestCase):

    @parameterized.expand([
        ([1, 2, 3, 4], ["#", "##", "###", "####"]),
        ([5, 0, 2, 1], ["#####", "", "##", "#"]),
        ([0, 0, 0, 0], ["", "", "", ""])
    ])
    def test_h1(self, l, expected):
        self.assertEqual(list(map(histogram, l)), expected)


if __name__ == "__main__":
    unittest.main()
