import gmpy2
from gmpy2 import mpz

class MontMul:
    """蒙哥马利乘法类，用于高效地执行任意位宽的模乘运算。"""

    def __init__(self, bit_width, N):
        """
        初始化蒙哥马利乘法器，支持动态位宽设置。

        参数:
            bit_width (int): 计算位宽。
            N (int): 模运算的模数。
        """
        self.N = mpz(N)
        self.bit_width = bit_width
        self.R = mpz(1) << bit_width  # R = 2^bit_width
        self.logR = bit_width
        if gmpy2.gcd(self.N, self.R) != 1:
            raise ValueError("N和R必须互质")

        self.N_inv = gmpy2.invert(self.N, self.R)
        self.N_inv_neg = self.R - self.N_inv
        self.R2 = (self.R * self.R) % self.N

    def REDC(self, T):
        """蒙哥马利约减法，用于将大整数 T 约减模 N。"""
        m = (T * self.N_inv_neg) & ((1 << self.logR) - 1)  # m = (T * N_inv_neg) % R
        t = (T + m * self.N) >> self.logR  # t = (T + m * N) / R
        if t >= self.N:
            t -= self.N
        return t

    def modmul(self, a, b):
        """执行 a 和 b 的蒙哥马利模乘运算。"""
        if a >= self.N or b >= self.N:
            raise ValueError('输入的整数必须小于模数 N')
        aR = self.REDC(a * self.R2)  # 将 a 转换为蒙哥马利形式
        bR = self.REDC(b * self.R2)  # 将 b 转换为蒙哥马利形式
        T = aR * bR  # 标准乘法
        abR = self.REDC(T)  # 蒙哥马利约减
        return self.REDC(abR)  # 将 abR 转换为普通整数形式

if __name__ == '__main__':
    try:
        N = mpz(123456789)  # 使用 mpz 类型确保大数处理正确
        inst = MontMul(64, N)  # 初始化 MontMul 类，传递位宽和 N

        test_cases = [
            (mpz(23456789), mpz(12345678)),
            (mpz(98765432), mpz(87654321)),
            (mpz(11111111), mpz(22222222)),
            (mpz(33333333), mpz(44444444)),
        ]

        for input1, input2 in test_cases:
            mul = inst.modmul(input1, input2)
            expected = (input1 * input2) % N

            if mul == expected:
                print(f'({input1}*{input2}) % {N} = {mul} (expected {expected})')
            else:
                print(f'Error: ({input1}*{input2}) % {N} should be {expected}, but got {mul}')

    except Exception as e:
        print(f"An error occurred: {e}")
