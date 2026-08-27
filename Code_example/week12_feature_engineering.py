"""
[12주차] Feature Engineering + Design Matrix
"통계분석의 최종 목표물은 결국 design matrix X를 만드는 것"
"""
import numpy as np
import pandas as pd

np.random.seed(11)
n = 12
df = pd.DataFrame({
    "country": np.repeat(["Korea", "Japan", "China"], 4),
    "year": list(range(2021, 2025)) * 3,
    "gdp": np.random.gamma(9, 200, n).round(1),
    "export": np.random.gamma(5, 100, n).round(1),
    "region": np.repeat(["East", "East", "East"], 4),
    "oecd": np.repeat([1, 1, 0], 4),
})
df = df.sort_values(["country", "year"]).reset_index(drop=True)
print("[원본]"); print(df.head())

# ------------------------------------------------------------
# 1. 로그 변환: 왜 log를 취하는가 (분포/해석)
# ------------------------------------------------------------
df["log_gdp"] = np.log(df["gdp"])
df["log_export"] = np.log(df["export"])

# ------------------------------------------------------------
# 2. 표준화 (z-score)
# ------------------------------------------------------------
df["gdp_z"] = (df["gdp"] - df["gdp"].mean()) / df["gdp"].std()

# ------------------------------------------------------------
# 3. 범주형 인코딩: One-hot (기준범주 제외 = 회귀에서의 dummy)
# ------------------------------------------------------------
dummies = pd.get_dummies(df["country"], prefix="cty", drop_first=True, dtype=int)
df = pd.concat([df, dummies], axis=1)

# ------------------------------------------------------------
# 4. 상호작용 변수 & 시차 변수
# ------------------------------------------------------------
df["gdp_x_oecd"] = df["gdp_z"] * df["oecd"]
df["export_lag1"] = df.groupby("country")["export"].shift(1)

# ------------------------------------------------------------
# 5. 완성된 design matrix 확인
# ------------------------------------------------------------
X_cols = ["log_gdp", "gdp_z", "oecd", "gdp_x_oecd", "export_lag1",
          "cty_Japan", "cty_Korea"]
X = df[X_cols].dropna()
print("\n[Design Matrix X]  shape:", X.shape)
print(X.head())

# patsy/statsmodels formula와의 연결
import statsmodels.formula.api as smf
m = smf.ols("log_export ~ log_gdp + C(country) + oecd", data=df).fit()
print("\nformula가 자동 생성한 design matrix 컬럼:")
print(m.model.exog_names)   # C(country)가 dummy로 펼쳐진 것을 확인
