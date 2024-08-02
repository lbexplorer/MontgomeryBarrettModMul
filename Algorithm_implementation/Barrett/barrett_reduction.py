import gmpy2
from gmpy2 import mpz

class BarrettMul:
    def __init__(self, N, bit_width=None):
        self.N = mpz(N)
        self.k = bit_width if bit_width else 2 * self.N.bit_length()
        self.R = mpz(2) ** self.k
        self.mu = (self.R * self.R) // self.N


    def multiply(self, x, y):
        x = mpz(x)  # 在入口处转换，减少重复转换
        y = mpz(y)
        if x >= self.N or y >= self.N:
            raise Exception('输入的整数必须小于模数 N')
        product = x * y
        q1 = product >> self.k
        q2 = q1 * self.mu
        q3 = q2 >> self.k
        r1 = product & (self.R - 1)  # 使用位与运算获取余数
        r2 = (q3 * self.N) & (self.R - 1)
        r = r1 - r2
        if r < 0:
            r += self.R
        r %= self.N  # 使用模运算替代循环减法
        return r

# 使用示例
if __name__ == "__main__":
    N = 2**255 - 19
    bit_width = 64  # 可以修改这个值来测试不同的位宽性能
    x = 123456789
    y = 987654321
    barrett = BarrettMul(N, bit_width)
    result = barrett.multiply(x, y)
    print(f"Barrett Result: {result} (expected {(x * y) % N})")
