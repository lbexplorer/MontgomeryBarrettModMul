import gmpy2
from gmpy2 import mpz, random_state
import time
import memory_profiler
import csv
import traceback

from Algorithm_implementation.Barrett.barrett_reduction import BarrettMul
import gmpy2
from gmpy2 import mpz

class MontMul:
    def __init__(self, bit_width, N):
        self.N = mpz(N)
        self.bit_width = bit_width
        self.R = gmpy2.powmod(mpz(2), bit_width, self.N)  # 使用 gmpy2 的大数操作方法
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


# 初始化测试参数
bit_widths = [64, 128, 256, 4096]  # 定义测试使用的不同位宽
num_tests = 100  # 定义每种位宽的测试次数
rand = random_state(42)  # 初始化随机数生成器，固定种子确保结果可复现

# 准备存储性能测试结果的CSV文件
csv_filename = "algorithm_performance.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Bit Width", "Algorithm", "Total Time (s)", "Memory Usage (MB)"])

def perform_tests(multiplier_class, N, bit_width, num_tests):
    """执行性能测试并记录结果。

    参数:
    - multiplier_class: 使用的乘法类（MontMul 或 BarrettMul）
    - N: 模数
    - bit_width: 位宽
    - num_tests: 测试次数

    返回:
    - total_time: 总耗时
    - total_mem_usage: 内存使用量
    """
    try:
        # 初始化乘法算法实例
        multiplier = multiplier_class(bit_width, N)
        start_time = time.time()
        mem_usage_start = memory_profiler.memory_usage()[0]

        # 进行指定次数的随机乘法运算
        for _ in range(num_tests):
            x = gmpy2.mpz_random(rand, mpz(2) ** bit_width)
            y = gmpy2.mpz_random(rand, mpz(2) ** bit_width)
            result = multiplier.modmul(x, y)

        # 计算总耗时和内存使用量
        end_time = time.time()
        mem_usage_end = memory_profiler.memory_usage()[0]
        total_time = end_time - start_time
        total_mem_usage = mem_usage_end - mem_usage_start

        return total_time, total_mem_usage
    except Exception as e:
        print(f"Error during testing at bit width {bit_width}: {str(e)}")
        traceback.print_exc()  # 打印异常的堆栈跟踪
        return None, None  # 在发生错误时返回None

# 将测试结果追加到CSV文件中
with open(csv_filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    for bit_width in bit_widths:
        N = gmpy2.next_prime(mpz(1) << bit_width)  # 选择一个大于2^bit_width的素数作为模数
        print(f"Testing with bit width: {bit_width} bits")

        # 分别测试蒙哥马利乘法和巴雷特乘法
        mont_time, mont_mem = perform_tests(MontMul, N, bit_width, num_tests)
        if mont_time is not None and mont_mem is not None:
            writer.writerow([bit_width, "Montgomery Multiplication", mont_time, mont_mem])
            print(f"Montgomery Multiplication: Time = {mont_time:.2f}s, Memory Usage = {mont_mem:.2f} MB")

        barrett_time, barrett_mem = perform_tests(BarrettMul, N, bit_width, num_tests)
        if barrett_time is not None and barrett_mem is not None:
            writer.writerow([bit_width, "Barrett Multiplication", barrett_time, barrett_mem])
            print(f"Barrett Multiplication: Time = {barrett_time:.2f}s, Memory Usage = {barrett_mem:.2f} MB")
