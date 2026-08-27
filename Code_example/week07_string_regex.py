"""
[7주차] String 처리, Regex, Category dtype
실무에서 '지저분한 텍스트 -> 분석 가능한 변수' 만들기
"""
import pandas as pd

df = pd.DataFrame({
    "raw_country": [" korea (Rep.) ", "JAPAN", "china ", "U.S.A.", "germany"],
    "hs_code": ["HS-8542.31", "HS-8703.23", "HS-8542.31", "HS-2709.00", "HS-8703.23"],
    "amount": ["1,234.5", "2,000", "-", "3,456.7", "980.0"],
})
print("[원본]"); print(df)

# ------------------------------------------------------------
# 1. 기본 문자열 정제: strip / upper / replace
# ------------------------------------------------------------
df["country"] = (df["raw_country"]
                 .str.strip()
                 .str.upper()
                 .str.replace(r"\s*\(.*\)", "", regex=True)   # 괄호 제거
                 .str.replace(".", "", regex=False))
print("\n정제된 국가명:", df["country"].tolist())

# ------------------------------------------------------------
# 2. Regex로 정보 추출: HS코드에서 4자리 품목번호 뽑기
# ------------------------------------------------------------
df["hs4"] = df["hs_code"].str.extract(r"HS-(\d{4})")
print("\nHS 4단위:", df["hs4"].tolist())

# ------------------------------------------------------------
# 3. 숫자처럼 생긴 문자열 -> 진짜 숫자
# ------------------------------------------------------------
df["amount_num"] = pd.to_numeric(
    df["amount"].str.replace(",", ""), errors="coerce")  # "-" 는 NaN 처리
print("\namount dtype:", df["amount_num"].dtype)
print(df[["amount", "amount_num"]])

# ------------------------------------------------------------
# 4. Category dtype: 메모리와 의미
# ------------------------------------------------------------
big = pd.Series(["Asia", "Europe", "America"] * 100_000)
print("\nobject 메모리 :", big.memory_usage(deep=True) // 1024, "KB")
print("category 메모리:", big.astype("category").memory_usage(deep=True) // 1024, "KB")

# 순서가 있는 범주형
grade = pd.Series(["Mid", "Low", "High", "Mid"]).astype(
    pd.CategoricalDtype(["Low", "Mid", "High"], ordered=True))
print("\n순서형 비교 (grade > 'Low'):", (grade > "Low").tolist())
