"""
[1주차] Python/Colab 기초 + NumPy Vectorization + Tidy Data
목표: "Python을 배우는 것"이 아니라 "Python으로 데이터를 처리하는 사고방식" 익히기
"""
import time
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# 1. Loop vs Vectorization : 실행시간 직접 비교
# ------------------------------------------------------------
data = np.random.rand(5_000_000)

# (1) Python loop 방식
start = time.time()
result_loop = []
for x in data:
    result_loop.append(x * 2)
t_loop = time.time() - start

# (2) Vectorized 방식
start = time.time()
result_vec = data * 2
t_vec = time.time() - start

print(f"loop 방식      : {t_loop:.3f}초")
print(f"vectorized 방식: {t_vec:.4f}초")
print(f"속도 차이      : 약 {t_loop / t_vec:.0f}배")

# ------------------------------------------------------------
# 2. Broadcasting 맛보기
# ------------------------------------------------------------
gdp = np.array([100, 200, 300])        # 단위: 십억 달러
growth = 1.03
print("\n내년 GDP 예상:", gdp * growth)  # 스칼라가 배열 전체에 적용됨

# ------------------------------------------------------------
# 3. Tidy Data 개념: "한 행 = 한 관측치, 한 열 = 한 변수"
# ------------------------------------------------------------
# 나쁜 예 (변수가 열 이름에 숨어 있음)
messy = pd.DataFrame({
    "country": ["Korea", "Japan"],
    "GDP_2022": [100, 200],
    "GDP_2023": [105, 205],
})
print("\n[messy data]"); print(messy)

# 좋은 예 (tidy)
tidy = messy.melt(id_vars="country", var_name="year", value_name="GDP")
tidy["year"] = tidy["year"].str.replace("GDP_", "").astype(int)
print("\n[tidy data]"); print(tidy)
