import math
import numpy as np
import matplotlib.pyplot as plt

def maclaurin_ln1p(x, n_terms=10):
    """
    利用 Maclaurin 級數展開計算 ln(1+x)
    ln(1+x) = x - x^2/2 + x^3/3 - x^4/4 + ...，適用於 -1 < x <= 1
    """
    s = 0.0
    for n in range(1, n_terms+1):
        term = ((-1)**(n-1)) * (x**n) / n
        s += term
    return s

def mercator_ln1p(x, n_terms=10):
    """
    利用 Mercator 展開式計算 ln(1+x)
    
    Mercator 展開形式原本是：
      ln(z) = 2 * [ y + y^3/3 + y^5/5 + ... ]，其中 y = (z-1)/(z+1)
    若令 z = 1+x，則：
      y = (1+x - 1)/(1+x+1) = x/(x+2)
    因此 ln(1+x) 可近似為：
      ln(1+x) ≈ 2 * [ y + y^3/3 + y^5/5 + ... ]
    """
    # 先計算 y
    y = x / (x + 2)
    s = 0.0
    for n in range(n_terms):
        power = 2 * n + 1
        s += (y**power) / power
    return 2 * s

# 定義 x 的範圍，注意 ln(1+x) 定義域 x > -1
x_values = np.linspace(-0.9, 1.0, 300)
true_values = np.log(1 + x_values)
# 計算 Maclaurin 與 Mercator 展開的近似值，這裡用較多項數（例如 20 項）以獲得較好的近似
maclaurin_values = np.array([maclaurin_ln1p(x, n_terms=10) for x in x_values])
mercator_values = np.array([mercator_ln1p(x, n_terms=10) for x in x_values])

# 繪圖比較
plt.figure(figsize=(10,6))
plt.plot(x_values, true_values, label='math.log(1+x)', color='black', linewidth=2)
plt.plot(x_values, maclaurin_values, label='Maclaurin Series', linestyle='--')
plt.plot(x_values, mercator_values, label='Mercator Series', linestyle=':')
plt.xlabel('x')
plt.ylabel('ln(1+x)')
plt.title('ln(1+x) 近似展開比較')
plt.legend()
plt.grid(True)
plt.show()
