import unittest
from gmpy2 import mpz

from Algorithm_implementation.Barrett.barrett_reduction import BarrettMul


class TestBarrettMul(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            (64, mpz(101)),
            (128, mpz(101)),
            (256, mpz(101)),
            (4096, mpz(101))
        ]

    def test_initialization(self):
        for bit_width, N in self.test_cases:
            barrett_mul = BarrettMul(N, bit_width)
            self.assertEqual(barrett_mul.N, mpz(N))
            self.assertEqual(barrett_mul.k, bit_width)
            self.assertEqual(barrett_mul.R, mpz(2) ** bit_width)

    def test_multiply(self):
        for bit_width, N in self.test_cases:
            barrett_mul = BarrettMul(N, bit_width)
            a = mpz(45)
            b = mpz(75)
            result = barrett_mul.multiply(a, b)
            expected = (a * b) % N
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
