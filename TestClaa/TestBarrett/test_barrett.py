import unittest
import time
from gmpy2 import mpz
from Barrett.barrett_reduction import BarrettMul

class TestBarrettMul(unittest.TestCase):
    def setUp(self):
        self.N = mpz(1000000007)
        self.bit_widths = [64, 128, 256, 4096]  # 添加更多位宽
        self.barretts = [BarrettMul(self.N, bw) for bw in self.bit_widths]

    def test_multiply_standard(self):
        """测试不同位宽下标准乘法运算结果的正确性"""
        for barrett in self.barretts:
            x = mpz(123456789)
            y = mpz(987654321)
            result = barrett.multiply(x, y)
            expected = (x * y) % self.N
            self.assertEqual(result, expected)

    def test_edge_cases(self):
        """测试不同位宽下的边界条件"""
        for barrett in self.barretts:
            x = self.N - 1
            y = self.N - 1
            result = barrett.multiply(x, y)
            expected = (x * y) % self.N
            self.assertEqual(result, expected)
            x = 0
            y = mpz(987654321)
            result = barrett.multiply(x, y)
            self.assertEqual(result, 0)

    def test_performance(self):
        """在不同位宽下测试性能"""
        for barrett in self.barretts:
            x = mpz(2**512)
            y = mpz(2**513)
            start_time = time.time()
            barrett.multiply(x, y)
            elapsed = time.time() - start_time
            print(f"Performance for bit width {barrett.k}: {elapsed} seconds")

if __name__ == '__main__':
    unittest.main()
