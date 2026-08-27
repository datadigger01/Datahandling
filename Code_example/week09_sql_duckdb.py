"""
[9주차] SQL + DuckDB
핵심 메시지: "pandas 방식과 SQL 방식은 동일한 데이터 연산을 다른 문법으로 수행한다"
"""
import pandas as pd
import numpy as np
import duckdb

np.random.seed(3)
df = pd.DataFrame({
    "country": np.random.choice(["Korea", "Japan", "China"], 300),
    "year": np.random.choice([2022, 2023, 2024], 300),
    "export": np.random.gamma(5, 100, 300).round(1),
})

# ------------------------------------------------------------
# 1. 같은 연산, 두 가지 문법 — 나란히 비교
# ------------------------------------------------------------
print("[pandas]")
print(df.groupby("country")["export"].mean().round(1))

print("\n[DuckDB SQL] (pandas DataFrame을 바로 쿼리!)")
print(duckdb.sql("""
    SELECT country, ROUND(AVG(export), 1) AS avg_export
    FROM df
    GROUP BY country
    ORDER BY country
""").df())

# ------------------------------------------------------------
# 2. 조건 + 집계 + 정렬 비교
# ------------------------------------------------------------
print("\n[pandas] 2024년 국가별 총수출 상위:")
print(df.query("year == 2024").groupby("country")["export"]
        .sum().sort_values(ascending=False).round(1))

print("\n[SQL] 동일 연산:")
print(duckdb.sql("""
    SELECT country, ROUND(SUM(export), 1) AS total_export
    FROM df
    WHERE year = 2024
    GROUP BY country
    ORDER BY total_export DESC
""").df())

# ------------------------------------------------------------
# 3. JOIN도 SQL로
# ------------------------------------------------------------
region = pd.DataFrame({"country": ["Korea", "Japan", "China"],
                       "region": ["East Asia", "East Asia", "East Asia"]})
print("\n[SQL JOIN]:")
print(duckdb.sql("""
    SELECT d.country, r.region, ROUND(AVG(d.export),1) AS avg_export
    FROM df d
    LEFT JOIN region r USING (country)
    GROUP BY d.country, r.region
""").df())

# ------------------------------------------------------------
# 4. 파일을 직접 쿼리 (대용량 처리의 핵심 장점)
# ------------------------------------------------------------
df.to_csv("trade_sample.csv", index=False)
print("\n[CSV 파일을 메모리에 다 올리지 않고 바로 쿼리]:")
print(duckdb.sql("""
    SELECT year, COUNT(*) AS n, ROUND(AVG(export),1) AS avg_export
    FROM 'trade_sample.csv'
    GROUP BY year ORDER BY year
""").df())
