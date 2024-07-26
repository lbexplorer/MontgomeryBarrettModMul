import unittest
import gmpy2
from gmpy2 import mpz

from Montgomery.montgomery_code import MontMul


class TestMontMul(unittest.TestCase):
    def setUp(self):
        """初始化测试环境，设置常用的参数"""
        self.bit_width = 128
        self.N = mpz('104729')  # 使用一个较小的素数作为模数进行测试
        self.mont_mul = MontMul(self.bit_width, self.N)

    def test_egcd(self):
        """测试扩展欧几里得算法"""
        a, b = 123456, 789012
        g, x, y = MontMul.egcd(a, b)
        self.assertEqual(g, gmpy2.gcd(a, b))

    def test_modinv(self):
        """测试模逆函数"""
        a = mpz(56)
        m = self.N
        inv_a = MontMul.modinv(a, m)
        self.assertEqual((a * inv_a) % m, 1)

    def test_REDC(self):
        """测试REDC函数的正确性"""
        T = mpz('123456789123456789123456789')
        reduced = self.mont_mul.REDC(T)
        # 手动计算 REDC
        m = (T * self.mont_mul.N_inv_neg) & ((1 << self.mont_mul.logR) - 1)
        t = (T + m * self.mont_mul.N) >> self.mont_mul.logR
        if t >= self.mont_mul.N:
            t -= self.mont_mul.N
        self.assertEqual(reduced, t)

    def test_ModMul(self):
        """测试蒙哥马利模乘法的正确性"""
        a = mpz(12345)
        b = mpz(67890)
        result = self.mont_mul.ModMul(a, b)
        expected = (a * b) % self.mont_mul.N
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
