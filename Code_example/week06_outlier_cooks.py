"""
[6주차] Outlier / Leverage / Influential Observation + Cook's Distance
핵심 질문: "이 관측값을 제거하면 회귀계수는 얼마나 달라지는가?"
(Data Processing -> Statistical Consequence)
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

np.random.seed(1)
n = 50
x1 = np.random.normal(5, 1.5, n)
x2 = np.random.normal(3, 1.0, n)
y = 2 + 1.5 * x1 + 0.8 * x2 + np.random.normal(0, 1, n)
df = pd.DataFrame({"y": y, "x1": x1, "x2": x2})

# 세 가지 유형의 특이 관측치를 인위적으로 추가
extra = pd.DataFrame({
    # (a) outlier: x는 평범, y만 이상  (b) high leverage: x가 극단, 회귀선 위
    # (c) influential: x도 극단, y도 회귀선에서 멀리
    "y":  [25.0, 2 + 1.5 * 12 + 0.8 * 3, -10.0],
    "x1": [5.0,  12.0,                    12.0],
    "x2": [3.0,  3.0,                     3.0],
}, index=[50, 51, 52])
df = pd.concat([df, extra])

# ------------------------------------------------------------
# 1. 단순 기준: |z| > 3, IQR
# ------------------------------------------------------------
z = (df["y"] - df["y"].mean()) / df["y"].std()
print("z-score 기준 (|z|>3) 이상치 index:", df.index[np.abs(z) > 3].tolist())

# ------------------------------------------------------------
# 2. 회귀 기반 진단: leverage, Cook's Distance
# ------------------------------------------------------------
model1 = smf.ols("y ~ x1 + x2", data=df).fit()
infl = model1.get_influence()
diag = pd.DataFrame({
    "leverage": infl.hat_matrix_diag,
    "student_resid": infl.resid_studentized_external,
    "cooks_d": infl.cooks_distance[0],
}, index=df.index)

thr = 4 / len(df)   # 흔히 쓰는 기준 4/n
print(f"\nCook's D 상위 5개 (기준 4/n = {thr:.3f}):")
print(diag.sort_values("cooks_d", ascending=False).head())

influential_index = diag.index[diag["cooks_d"] > thr]
print("\n영향점으로 판정된 index:", influential_index.tolist())

# ------------------------------------------------------------
# 3. 영향점 제거 전후 회귀계수 비교
# ------------------------------------------------------------
df2 = df.drop(index=influential_index)
model2 = smf.ols("y ~ x1 + x2", data=df2).fit()

compare = pd.DataFrame({
    "제거 전": model1.params.round(3),
    "제거 후": model2.params.round(3),
})
compare["변화"] = (compare["제거 후"] - compare["제거 전"]).round(3)
print("\n[회귀계수 비교]  (진짜 값: Intercept=2, x1=1.5, x2=0.8)")
print(compare)
# 토론: 세 관측치(50,51,52) 중 어떤 것이 계수를 실제로 움직였는가?
