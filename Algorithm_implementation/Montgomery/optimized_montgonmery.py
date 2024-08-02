import gmpy2
from gmpy2 import mpz


class OptimizedMontMul:
    def __init__(self, bit_width, N):
        self.N = mpz(N)
        self.bit_width = bit_width
        self.R = mpz(1) << bit_width
        self.logR = bit_width

        if gmpy2.gcd(self.N, self.R) != 1:
            raise ValueError("N和R必须互质")

        self.N_inv = gmpy2.invert(self.N, self.R)
        self.N_inv_neg = self.R - self.N_inv
        self.R2 = (self.R * self.R) % self.N

    def REDC(self, T):
        m = (T * self.N_inv_neg) & ((1 << self.logR) - 1)
        t = (T + m * self.N) >> self.logR
        if t >= self.N:
            t -= self.N
        return t

    def modmul(self, a, b):
        if a >= self.N or b >= self.N:
            raise ValueError('输入的整数必须小于模数 N')
        aR = self.REDC(a * self.R2)
        bR = self.REDC(b * self.R2)
        T = aR * bR
        abR = self.REDC(T)
        return self.REDC(abR)

if __name__ == '__main__':
    try:
        N = mpz(123456789)  # 使用 mpz 类型确保大数处理正确
        inst = OptimizedMontMul(64, N)  # 初始化 MontMul 类，传递位宽和 N

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
