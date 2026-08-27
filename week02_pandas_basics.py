"""
[2주차] pandas DataFrame, indexing, filtering, dtype
"""
import pandas as pd
import numpy as np

# 실습용 무역 데이터 생성
np.random.seed(42)
df = pd.DataFrame({
    "country": ["Korea", "Japan", "China", "USA", "Germany"] * 3,
    "year": np.repeat([2022, 2023, 2024], 5),
    "export": np.random.randint(100, 1000, 15).astype(float),
    "import_": np.random.randint(100, 1000, 15).astype(float),
    "region": (["Asia", "Asia", "Asia", "America", "Europe"] * 3),
})

# ------------------------------------------------------------
# 1. 데이터 구조 파악: 분석의 첫 습관
# ------------------------------------------------------------
print(df.head())
print("\nshape:", df.shape)
print("\ndtypes:\n", df.dtypes)
print("\ninfo:"); df.info()

# ------------------------------------------------------------
# 2. Indexing: loc(라벨) vs iloc(위치)
# ------------------------------------------------------------
print("\nloc  예시:\n", df.loc[0:2, ["country", "export"]])
print("\niloc 예시:\n", df.iloc[0:3, 0:3])

# ------------------------------------------------------------
# 3. Filtering (Boolean indexing)
# ------------------------------------------------------------
cond = (df["year"] == 2024) & (df["export"] > 400)
print("\n2024년 수출 400 초과:\n", df[cond])

# query() 방식도 함께
print("\nquery 방식:\n", df.query("year == 2024 and export > 400"))

# ------------------------------------------------------------
# 4. 파생변수 생성과 dtype 관리
# ------------------------------------------------------------
df["trade_balance"] = df["export"] - df["import_"]
df["region"] = df["region"].astype("category")   # 메모리 절약 + 범주형 명시
df["year"] = df["year"].astype("int16")
print("\ndtype 변경 후:\n", df.dtypes)

# ------------------------------------------------------------
# 5. groupby 기초
# ------------------------------------------------------------
print("\n국가별 평균 수출:\n", df.groupby("country", observed=True)["export"].mean())
print("\n지역-연도별 수출 합계:\n",
      df.groupby(["region", "year"], observed=True)["export"].sum())
