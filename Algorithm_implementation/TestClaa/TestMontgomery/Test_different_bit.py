import unittest
from gmpy2 import mpz
import gmpy2

from Algorithm_implementation.Montgomery.montgomery_code import MontMul


class TestMontMul(unittest.TestCase):
    def setUp(self):
        # 使用大质数作为N
        self.N = mpz('170141183460469231731687303715884105727')  # 2^127 - 1 是一个大质数
        self.a = mpz('12345678901234567890')
        self.b = mpz('98765432109876543210')

    def test_modmul_64(self):
        mont = MontMul(64, self.N)
        result = mont.modmul(self.a, self.b)
        expected = (self.a * self.b) % self.N
        self.assertEqual(result, expected)

    def test_modmul_128(self):
        mont = MontMul(128, self.N)
        result = mont.modmul(self.a, self.b)
        expected = (self.a * self.b) % self.N
        self.assertEqual(result, expected)

    def test_modmul_256(self):
        mont = MontMul(256, self.N)
        result = mont.modmul(self.a, self.b)
        expected = (self.a * self.b) % self.N
        self.assertEqual(result, expected)

    def test_modmul_512(self):
        mont = MontMul(512, self.N)
        result = mont.modmul(self.a, self.b)
        expected = (self.a * self.b) % self.N
        self.assertEqual(result, expected)

    def test_modmul_1024(self):
        mont = MontMul(1024, self.N)
        result = mont.modmul(self.a, self.b)
        expected = (self.a * self.b) % self.N
        self.assertEqual(result, expected)

    def test_modmul_large_numbers(self):
        # 确保大数小于 N
        a = gmpy2.next_prime(self.N >> 1)
        b = gmpy2.next_prime(self.N >> 2)
        mont = MontMul(1024, self.N)
        result = mont.modmul(a, b)
        expected = (a * b) % self.N
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
