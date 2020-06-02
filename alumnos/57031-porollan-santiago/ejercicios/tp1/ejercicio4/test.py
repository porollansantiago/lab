import unittest
from ej4 import histogram, histogram_from_file
from parameterized import parameterized

class test_histogram(unittest.TestCase):

    @parameterized.expand([
        ([1, 2, 3, 4], ["#", "##", "###", "####"]),
        ([5, 0, 2, 1], ["#####", "", "##", "#"]),
        ([0, 0, 0, 0], ["", "", "", ""])
    ])
    def test_h1(self, l, expected):
        self.assertEqual(list(map(histogram, l)), expected)

    def test_histogram_from_file(self):
        expected = ["####", "#######", "######", "####", "#", 
                    "#########", "##", "", "########", "#######",
                    "######", "###", "#####", "##########"]
        self.assertEqual(histogram_from_file("histogram"), expected)


if __name__ == "__main__":
    unittest.main()
