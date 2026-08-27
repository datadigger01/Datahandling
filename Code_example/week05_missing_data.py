"""
[5주차] Missing Data: MCAR / MAR / MNAR + Imputation 비교
Simple -> KNN -> Iterative 순으로 결과를 '비교'하는 것이 목표
"""
import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer

np.random.seed(0)
n = 1000

# 완전한 데이터 생성 (소득은 교육연수와 상관)
educ = np.random.normal(12, 3, n)
income = 200 + 30 * educ + np.random.normal(0, 50, n)
df_full = pd.DataFrame({"educ": educ, "income": income})

# ------------------------------------------------------------
# 1. 세 가지 결측 메커니즘 시뮬레이션
# ------------------------------------------------------------
def make_missing(df, mechanism):
    d = df.copy()
    if mechanism == "MCAR":      # 완전 무작위
        mask = np.random.rand(n) < 0.3
    elif mechanism == "MAR":     # 관측된 educ에 의존 (교육수준 낮을수록 무응답)
        p = 1 / (1 + np.exp((d["educ"] - 10)))
        mask = np.random.rand(n) < p
    elif mechanism == "MNAR":    # 결측 여부가 income '자신'에 의존 (고소득 무응답)
        p = 1 / (1 + np.exp(-(d["income"] - d["income"].quantile(0.7)) / 30))
        mask = np.random.rand(n) < p
    d.loc[mask, "income"] = np.nan
    return d

print(f"{'메커니즘':<6} {'결측률':>8} {'관측된 평균':>12} (전체 진짜 평균: {df_full['income'].mean():.1f})")
for m in ["MCAR", "MAR", "MNAR"]:
    d = make_missing(df_full, m)
    print(f"{m:<6} {d['income'].isna().mean():>7.1%} {d['income'].mean():>12.1f}")
# -> MCAR은 평균이 거의 그대로, MAR/MNAR은 편향 발생을 눈으로 확인

# ------------------------------------------------------------
# 2. Imputation 방법 비교 (MAR 데이터 사용)
# ------------------------------------------------------------
d_mar = make_missing(df_full, "MAR")
X = d_mar[["educ", "income"]].values

imputers = {
    "평균 대체 (Simple)": SimpleImputer(strategy="mean"),
    "KNN (k=5)":          KNNImputer(n_neighbors=5),
    "Iterative (MICE형)":  IterativeImputer(random_state=0),
}

true_mean = df_full["income"].mean()
print(f"\n진짜 평균: {true_mean:.1f}")
for name, imp in imputers.items():
    filled = imp.fit_transform(X)
    print(f"{name:<20} 대체 후 평균: {filled[:,1].mean():>7.1f} "
          f"| 표준편차: {filled[:,1].std():>6.1f} (진짜: {df_full['income'].std():.1f})")
# 관찰 포인트: 평균 대체는 분산을 심하게 축소시킨다!
