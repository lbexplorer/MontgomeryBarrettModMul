
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

        属性:
            N (mpz): 模数。
            R (mpz): 与 2^bit_width 最接近的2的幂，用于蒙哥马利运算。
            logR (int): R 的二进制对数，用于位运算。
            N_inv_neg (mpz): N 模 R 的负模逆。
            R2 (mpz): R 的平方模 N，用于转换到蒙哥马利形式。
        """
        self.N = mpz(N)
        self.bit_width = bit_width
        self.R = mpz(1) << bit_width  # 使用 gmpy2 的 mpz 类型处理大数位移
        self.logR = bit_width
        self.N_inv = gmpy2.invert(self.N, self.R)
        self.N_inv_neg = self.R - self.N_inv
        self.R2 = (self.R * self.R) % self.N

    @staticmethod
    def egcd(a, b):
        """扩展欧几里得算法，用于查找 a 和 b 的最大公约数。"""
        if a == 0:
            return (b, mpz(0), mpz(1))
        else:
            g, y, x = MontMul.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    @staticmethod
    def modinv(a, m):
        """计算模 m 下 a 的模逆。"""
        g, x, y = MontMul.egcd(a, m)
        if g != 1:
            raise Exception('模逆不存在')
        else:
            return x % m

    def REDC(self, T):
        """蒙哥马利约减法，用于将大整数 T 约减模 N。"""
        m = (T * self.N_inv_neg) & ((1 << self.logR) - 1)  # m = (T * N_inv_neg) % R
        t = (T + m * self.N) >> self.logR  # t = (T + m * N) / R
        if t >= self.N:
            t -= self.N
        return t

    def ModMul(self, a, b):
        """执行 a 和 b 的蒙哥马利模乘运算。"""
        if a >= self.N or b >= self.N:
            raise Exception('输入的整数必须小于模数 N')
        aR = self.REDC(a * self.R2)  # 将 a 转换为蒙哥马利形式
        bR = self.REDC(b * self.R2)  # 将 b 转换为蒙哥马利形式
        T = aR * bR  # 标准乘法
        abR = self.REDC(T)  # 蒙哥马利约减
        return self.REDC(abR)  # 将 abR 转换为普通整数形式

if __name__ == '__main__':
    N = mpz(123456789)  # 使用 mpz 类型确保大数处理正确
    R = mpz(1) << 64  # 假设我们在64位整数乘法上工作
    g, x, y = MontMul.egcd(N, R)
    if R <= N or g != 1:
        raise Exception('N 必须大于 R 且 gcd(N, R) == 1')

    inst = MontMul(64, N)  # 初始化 MontMul 类，传递位宽和 N

    input1 = mpz(23456789)
    input2 = mpz(12345678)
    mul = inst.ModMul(input1, input2)
    expected = (input1 * input2) % N

    if mul == expected:
        print(f'({input1}*{input2}) % {N} = {mul} (expected {expected})')
    else:
        print(f'Error: ({input1}*{input2}) % {N} should be {expected}, but got {mul}')