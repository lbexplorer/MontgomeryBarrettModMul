# 项目介绍
    本项目旨在比较蒙哥马利大数模乘（Montgomery Multiplication）和巴雷特大数模乘（Barrett Multiplication）两种算法在不同位宽（如64bit、128bit、256bit、4096bit）下的性能表现。通过实现并测试这两种算法，收集了执行时间、CPU使用率和内存使用情况的数据，并分析了它们在不同应用场景下的适用性和优势。

# 目录结构描述
    ├── ReadMe.md           // 帮助文档
    
    ├──Montgomery  // 蒙哥马利大数模乘算法实现
    
    ├── Barrett             // 巴雷特大数模乘算法实现
    
    ├── TestClaa        //单元测试
# 环境要求
Python 3.12
安装以下Python库：
gmpy2
psutil
memory_profiler
tqdm
numpy
pandas
matplotlib
seaborn

# 代码概述
## BarrettMul 类
用于实现巴雷特大数模乘算法。
__init__(self, N, bit_width=None): 初始化模数N和位宽k。
multiply(self, x, y): 执行模乘操作。

## MontMul 类
用于实现蒙哥马利大数模乘算法。
__init__(self, bit_width, N): 初始化模数N、位宽和预计算常量。
REDC(self, T): 执行蒙哥马利约简操作。
modmul(self, a, b): 执行模乘操作。


## 性能测试函数
generate_random_number(bit_width, N): 生成随机数。
generate_valid_N(bit_width): 生成有效的模数N。
measure_performance(bit_width, n_tests=100): 测量每个位宽下的执行时间、CPU使用率和内存使用情况。

    
 

 
 

 
 
