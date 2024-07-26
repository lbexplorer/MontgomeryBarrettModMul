import unittest

from Barrett.barrett_reduction import BarrettMul
from Montgomery.montgomery_code import MontMul


# 假设这是您的算法所在的模块

class TestModularMultiplicationAlgorithms(unittest.TestCase):
    def setUp(self):
        # 初始化测试所需的参数和实例
        self.bit_width = 256
        self.N = 2**255 - 19  # 使用常见的质数
        self.montmul = MontMul(self.bit_width, self.N)
        self.barrettmul = BarrettMul(self.N, self.bit_width)

    def test_basic_functionality(self):
        # 测试基本的模乘功能
        a = 123456789
        b = 987654321
        expected_result = (a * b) % self.N
        self.assertEqual(self.montmul.ModMul(a, b), expected_result)
        self.assertEqual(self.barrettmul.multiply(a, b), expected_result)

    def test_edge_cases(self):
        # 测试边界条件
        self.assertEqual(self.montmul.ModMul(0, 10), 0)
        self.assertEqual(self.montmul.ModMul(10, 0), 0)
        self.assertEqual(self.barrettmul.multiply(0, 10), 0)
        self.assertEqual(self.barrettmul.multiply(10, 0), 0)

        self.assertEqual(self.montmul.ModMul(1, 1), 1 % self.N)
        self.assertEqual(self.barrettmul.multiply(1, 1), 1 % self.N)

    def test_exception_handling(self):
        # 测试异常处理
        large_value = self.N + 100  # 确保是大于模数的值
        with self.assertRaises(Exception):
            self.montmul.ModMul(large_value, 100)
        with self.assertRaises(Exception):
            self.barrettmul.multiply(large_value, 100)

    def test_large_numbers(self):
        # 测试大数处理能力
        a = (2 ** 1000) % self.N  # 保证 a < N
        b = (2 ** 1000) % self.N  # 保证 b < N
        expected_result = (a * b) % self.N
        self.assertEqual(self.montmul.ModMul(a, b), expected_result)
        self.assertEqual(self.barrettmul.multiply(a, b), expected_result)


if __name__ == '__main__':
    unittest.main()
