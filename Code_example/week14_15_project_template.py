"""
[14~15주차] 최종 프로젝트 골격: Raw -> Clean -> Integration -> Validation -> Codebook
학생 제출물의 구조를 보여주는 템플릿
"""
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# STEP 0. 지저분한 raw 데이터 (실제로는 파일/API에서 수집)
# ------------------------------------------------------------
raw = pd.DataFrame({
    "Country Name": [" korea ", "KOREA", "japan", "Japan ", "china", "China"],
    "YEAR": ["2023", "2024", "2023", "2024", "2023", "2024"],
    "GDP(USD)": ["1,673", "1,712", "4,213", "4,110", "17,794", "-"],
    "pop": [51.7, 51.6, 124.5, 124.0, 1410.0, 1408.0],
})
print("[RAW]"); print(raw)

# ------------------------------------------------------------
# STEP 1. Clean: 이름 표준화, dtype 정리, 결측 처리
# ------------------------------------------------------------
clean = raw.copy()
clean.columns = ["country", "year", "gdp", "pop"]           # 변수명 표준화
clean["country"] = clean["country"].str.strip().str.title()
clean["year"] = clean["year"].astype(int)
clean["gdp"] = pd.to_numeric(clean["gdp"].str.replace(",", ""), errors="coerce")

# 결측 처리 방침을 '명시적으로' 기록 (여기서는 국가별 선형보간 대신 그대로 두고 보고)
print("\n[CLEAN]"); print(clean)
print("결측 현황:\n", clean.isna().sum())

# ------------------------------------------------------------
# STEP 2. Integration: 외부 데이터와 병합 (granularity 검증 포함)
# ------------------------------------------------------------
region = pd.DataFrame({"country": ["Korea", "Japan", "China"],
                       "region": ["East Asia"] * 3})
assert clean.duplicated(["country", "year"]).sum() == 0, "key가 unique하지 않음!"
final = clean.merge(region, on="country", how="left", validate="m:1")
final["gdp_per_capita"] = (final["gdp"] * 1e9 / (final["pop"] * 1e6)).round(1)

# ------------------------------------------------------------
# STEP 3. Validation: 규칙 명시
# ------------------------------------------------------------
import pandera.pandas as pa
schema = pa.DataFrameSchema({
    "country": pa.Column(str, pa.Check.isin(["Korea", "Japan", "China"])),
    "year": pa.Column(int, pa.Check.in_range(2000, 2030)),
    "gdp": pa.Column(float, pa.Check.gt(0), nullable=True),
    "pop": pa.Column(float, pa.Check.gt(0)),
})
schema.validate(final)
print("\n검증 통과! [FINAL]"); print(final)

# ------------------------------------------------------------
# STEP 4. Codebook 자동 생성 (제출 필수!)
# ------------------------------------------------------------
meta = {
    "country": ("국가명(표준화)", "World Bank"),
    "year": ("연도", "World Bank"),
    "gdp": ("GDP, 십억 USD", "World Bank"),
    "pop": ("인구, 백만 명", "World Bank"),
    "region": ("지역 구분", "직접 작성"),
    "gdp_per_capita": ("1인당 GDP, USD (파생변수)", "계산"),
}
codebook = pd.DataFrame({
    "Variable": final.columns,
    "Description": [meta[c][0] for c in final.columns],
    "Type": [str(t) for t in final.dtypes],
    "Source": [meta[c][1] for c in final.columns],
    "Missing(%)": (final.isna().mean() * 100).round(1).values,
})
print("\n[CODEBOOK]"); print(codebook.to_string(index=False))
codebook.to_csv("codebook.csv", index=False)
final.to_csv("final_data.csv", index=False)
print("\ncodebook.csv, final_data.csv 저장 완료")
