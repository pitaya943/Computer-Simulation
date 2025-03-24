# 1. 自製線性同餘隨機數產生器（LCG）
# 常用參數：a = 1103515245, c = 12345, m = 2**31
_seed = 12345  # 初始種子，可自行更改

def lcg():
    global _seed
    a = 1103515245
    c = 12345
    m = 2**31
    _seed = (a * _seed + c) % m
    return _seed / m  # 返回介於 0 和 1 之間的數

# 2. 自製自然對數近似函數
def my_ln(x, iterations=20):
    if x <= 0:
        raise ValueError("x 必須大於 0")
    # 將 x 轉換到適合展開級數的範圍：
    # 利用公式：ln(x) = 2 * [ y + y^3/3 + y^5/5 + ... ]，其中 y = (x-1)/(x+1)
    y = (x - 1) / (x + 1)
    result = 0.0
    y_term = y
    for n in range(iterations):
        result += y_term / (2 * n + 1)
        y_term *= y * y  # 每次乘上 y^2
    return 2 * result

# 3. 利用逆變換法生成指數分布隨機數
def exponential_random(mean):
    u = lcg()  # 取得一個均勻隨機數 u，介於 (0,1)
    # 根據公式 X = -mean * ln(u)
    return -mean * my_ln(u)

# 測試範例：設均值為 2.0
result = exponential_random(2.0)
print(f'生成的指數分布隨機數：{result}')
