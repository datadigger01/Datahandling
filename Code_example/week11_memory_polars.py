"""
[11주차] 대용량 데이터 처리 + Memory Optimization + Polars 소개(20~30분 demo)
"""
import numpy as np
import pandas as pd

np.random.seed(7)
n = 1_000_000
df = pd.DataFrame({
    "country": np.random.choice(["Korea", "Japan", "China", "USA"], n),
    "year": np.random.choice([2020, 2021, 2022, 2023, 2024], n).astype("int64"),
    "export": np.random.gamma(5, 100, n),
    "flag": np.random.choice([0, 1], n).astype("int64"),
})

def mem_mb(d):
    return d.memory_usage(deep=True).sum() / 1024**2

# ------------------------------------------------------------
# 1. dtype 최적화로 메모리 줄이기
# ------------------------------------------------------------
print(f"최적화 전: {mem_mb(df):.1f} MB")
opt = df.copy()
opt["country"] = opt["country"].astype("category")
opt["year"] = opt["year"].astype("int16")
opt["export"] = opt["export"].astype("float32")
opt["flag"] = opt["flag"].astype("int8")
print(f"최적화 후: {mem_mb(opt):.1f} MB  (약 {mem_mb(df)/mem_mb(opt):.1f}배 절약)")

# ------------------------------------------------------------
# 2. chunk 단위 처리: 파일이 메모리보다 클 때
# ------------------------------------------------------------
df.to_csv("big.csv", index=False)
total, cnt = 0.0, 0
for chunk in pd.read_csv("big.csv", chunksize=200_000):
    total += chunk["export"].sum()
    cnt += len(chunk)
print(f"\nchunk 처리로 구한 평균 export: {total/cnt:.2f}")

# ------------------------------------------------------------
# 3. Polars demo: "pandas 이외에도 대안이 있다"
# ------------------------------------------------------------
import time
import polars as pl   # 사전 설치: pip install polars pyarrow

start = time.time()
r_pd = df.groupby("country")["export"].mean()
t_pd = time.time() - start

pldf = pl.from_pandas(df)
start = time.time()
r_pl = pldf.group_by("country").agg(pl.col("export").mean())
t_pl = time.time() - start

print(f"\npandas groupby: {t_pd:.3f}초 | polars group_by: {t_pl:.3f}초")
print("\nPolars 문법 예시 (expression 기반):")
print(pldf.filter(pl.col("year") == 2024)
          .group_by("country")
          .agg(pl.col("export").mean().round(1).alias("avg_export"))
          .sort("country"))
# lazy 실행 소개
print("\nLazy 모드 (실행 계획 최적화 후 collect):")
print(pldf.lazy()
      .filter(pl.col("export") > 500)
      .group_by("year").agg(pl.len())
      .sort("year").collect())
