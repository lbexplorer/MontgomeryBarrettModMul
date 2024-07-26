import csv
import time
import random
from gmpy2 import mpz, bit_mask, invert  # 添加 invert 导入

# 修正：直接在这里定义bits作为列表，而不是从idlelib.help_about导入
bits = [64, 128, 256, 512, 1024, 2048, 4096]

def generate_random_bits(bit_size):
    """生成指定位宽的随机大数"""
    return mpz(random.getrandbits(bit_size))

def montgomery_multiplication(a, b, n, n_prime, r, bit_size):
    """
    蒙哥马利乘法实现
    参数:
    a, b - 乘数
    n - 模数
    n_prime - n的负模逆
    r - 2的位宽幂
    bit_size - 位宽
    """
    t = a * b
    m = ((t * n_prime) & (r - 1)) * n
    u = (t + m) >> bit_size  # 右移位宽以模拟除以2^bit_size
    if u >= n:
        u -= n
    return u

def barrett_reduction(x, m, mu):
    """
    巴雷特约简
    参数:
    x - 被约简数
    m - 模数
    mu - 预计算的比率
    """
    k = m.bit_length()
    q = (x >> (k - 1)) * mu
    q >>= (k + 1)
    r = x - q * m
    if r >= m:
        r -= m
    return r

def performance_test(bits, trials=100, output_file='performance_data.csv'):
    """
    性能测试并将结果保存到CSV文件
    参数:
    bits - 测试的位宽列表
    trials - 每个位宽的测试次数
    output_file - 输出CSV文件的名称
    """
    results = []
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Bit Size', 'Time Elapsed', 'Memory Usage'])

        for bit_size in bits:
            start_time = time.time()
            n = generate_random_bits(bit_size)
            n_prime = -invert(n, 2**bit_size)  # 修改为正确的模逆计算
            r = bit_mask(bit_size)
            mu = (1 << (2 * bit_size)) // n

            for _ in range(trials):
                a = generate_random_bits(bit_size)
                b = generate_random_bits(bit_size)
                montgomery_multiplication(a, b, n, n_prime, r, bit_size)
                barrett_reduction(a * b, n, mu)

            end_time = time.time()
            time_elapsed = end_time - start_time
            memory_usage = 'N/A'  # 实际内存使用应通过专门工具测量

            writer.writerow([bit_size, time_elapsed, memory_usage])
            results.append({'bit_size': bit_size, 'time_elapsed': time_elapsed, 'memory_usage': memory_usage})

    return results

# 运行性能测试
performance_test(bits, trials=100, output_file='performance_data.csv')
