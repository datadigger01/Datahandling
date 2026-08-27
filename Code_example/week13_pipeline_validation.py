"""
[13주차] sklearn Pipeline + Data Validation(Pandera) + Data Leakage
핵심: (1) 전처리도 모델의 일부다  (2) test 정보가 train 전처리에 새면 안 된다
"""
import numpy as np
import pandas as pd

np.random.seed(21)
n = 400
df = pd.DataFrame({
    "id": range(1, n + 1),
    "age": np.random.randint(20, 65, n),
    "region": np.random.choice(["Asia", "Europe", "America"], n),
    "income": np.random.gamma(9, 400, n).round(0),
})
df["y"] = (2000 + 80 * df["age"]
           + np.random.normal(0, 800, n)
           + np.where(df["region"] == "Asia", 500, 0))

# ============================================================
# PART 1. Data Validation: 먼저 '사고방식', 그 다음 Pandera
# ============================================================
print("=== 손으로 쓰는 validation rule ===")
print("age 0~120 범위 만족? ", df["age"].between(0, 120).all())
print("id unique?           ", df["id"].is_unique)
print("income 결측률 10%이하?", df["income"].notna().mean() >= 0.9)

import pandera.pandas as pa
schema = pa.DataFrameSchema({
    "id": pa.Column(int, unique=True),
    "age": pa.Column(int, pa.Check.in_range(0, 120)),
    "region": pa.Column(str, pa.Check.isin(["Asia", "Europe", "America"])),
    "income": pa.Column(float, pa.Check.ge(0), nullable=True),
    "y": pa.Column(float),
})
schema.validate(df.astype({"income": float, "y": float}))
print("\nPandera schema 검증 통과!")

# 일부러 규칙 위반 데이터를 넣어 오류 확인
bad = df.copy().astype({"income": float, "y": float})
bad.loc[0, "age"] = 150
try:
    schema.validate(bad)
except pa.errors.SchemaError as e:
    print("검증 실패 예시 ->", str(e).splitlines()[0][:70])

# ============================================================
# PART 2. Data Leakage: 잘못된 방식 vs 올바른 방식
# ============================================================
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

X = df[["age", "income", "region"]]
y = df["y"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

# --- (잘못) 전체 데이터로 scaler를 fit -> test 정보 누수 ---
scaler_wrong = StandardScaler().fit(X[["age", "income"]])       # 전체로 fit!
print("\n[누수] scaler가 본 평균(age):", scaler_wrong.mean_[0].round(2),
      " <- test 정보 포함")

# --- (올바름) train으로만 fit ---
scaler_ok = StandardScaler().fit(X_tr[["age", "income"]])
print("[정상] scaler가 본 평균(age):", scaler_ok.mean_[0].round(2),
      " <- train만 사용")

# ============================================================
# PART 3. ColumnTransformer + Pipeline: 누수를 구조적으로 차단
# ============================================================
numeric_cols = ["age", "income"]
categorical_cols = ["region"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_cols),
    ("cat", OneHotEncoder(drop="first"), categorical_cols),
])

pipe = Pipeline([
    ("prep", preprocessor),      # 전처리도 모델의 일부!
    ("model", LinearRegression()),
])

pipe.fit(X_tr, y_tr)             # fit은 train에만 -> transform 규칙도 train 기준
pred = pipe.predict(X_te)
print(f"\nPipeline test R^2: {r2_score(y_te, pred):.3f}")

# cross_val_score와 함께 쓰면 fold마다 전처리를 다시 fit -> 누수 원천 차단
from sklearn.model_selection import cross_val_score
cv = cross_val_score(pipe, X, y, cv=5, scoring="r2")
print("5-fold CV R^2:", cv.round(3), "| 평균:", cv.mean().round(3))
