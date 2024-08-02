import unittest
from gmpy2 import mpz

from Algorithm_implementation.Montgomery.montgomery_code import MontMul


class TestMontMul(unittest.TestCase):
    def setUp(self):
        """初始化测试中用到的模数和位宽"""
        self.N = mpz(123456789)
        self.bit_widths = [64, 128, 256, 512, 1024, 2048, 4096]

    def test_basic_modmul(self):
        """基本功能测试"""
        for bit_width in self.bit_widths:
            inst = MontMul(bit_width, self.N)
            a = mpz(23456789)
            b = mpz(12345678)
            expected = (a * b) % self.N
            result = inst.modmul(a, b)
            self.assertEqual(result, expected, f"Failed at bit width {bit_width}")

    def test_edge_cases(self):
        """边界条件测试"""
        for bit_width in self.bit_widths:
            inst = MontMul(bit_width, self.N)
            # 乘数为0的情况
            self.assertEqual(inst.modmul(mpz(0), mpz(12345678)), 0)
            self.assertEqual(inst.modmul(mpz(23456789), mpz(0)), 0)
            # 乘数均为1的情况
            self.assertEqual(inst.modmul(mpz(1), mpz(1)), 1 % self.N)

    def test_exception_handling(self):
        """异常处理测试"""
        for bit_width in self.bit_widths:
            inst = MontMul(bit_width, self.N)
            with self.assertRaises(ValueError):
                inst.modmul(mpz(234567890), mpz(12345678))  # 输入大于模数
            with self.assertRaises(ValueError):
                inst.modmul(mpz(23456789), mpz(123456790))  # 输入大于模数

    def test_large_numbers(self):
        """大数处理能力测试"""
        for bit_width in self.bit_widths:
            inst = MontMul(bit_width, self.N)
            a = mpz("123456789012345678901234567890")
            b = mpz("98765432109876543210987654321")
            a_mod = a % self.N
            b_mod = b % self.N
            expected = (a_mod * b_mod) % self.N
            result = inst.modmul(a_mod, b_mod)
            self.assertEqual(result, expected, f"Failed at bit width {bit_width}")


if __name__ == '__main__':
    unittest.main()
