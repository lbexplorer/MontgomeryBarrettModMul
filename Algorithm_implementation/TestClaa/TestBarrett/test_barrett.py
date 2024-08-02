import unittest
from gmpy2 import mpz

from Algorithm_implementation.Barrett.barrett_reduction import BarrettMul


class TestBarrettMul(unittest.TestCase):

    def setUp(self):
        self.N = mpz(101)
        self.bit_width = 128
        self.barrett_mul = BarrettMul(self.N, self.bit_width)

    def test_initialization(self):
        self.assertEqual(self.barrett_mul.N, mpz(self.N))
        self.assertEqual(self.barrett_mul.k, self.bit_width)
        self.assertEqual(self.barrett_mul.R, mpz(2) ** self.bit_width)

    def test_multiply(self):
        a = mpz(45)
        b = mpz(75)
        result = self.barrett_mul.multiply(a, b)
        expected = (a * b) % self.N
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
