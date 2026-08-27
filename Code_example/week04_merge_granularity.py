"""
[4주차] Merge/Join + 데이터 단위(Granularity, Unit of Observation)
원칙: "merge() 전에 반드시 각 데이터셋의 observation unit을 말로 정의하라"
"""
import pandas as pd

# 데이터 A: 한 행 = 국가 x 연도
gdp = pd.DataFrame({
    "country": ["Korea", "Korea", "Japan", "Japan"],
    "year":    [2023, 2024, 2023, 2024],
    "GDP":     [105, 110, 205, 208],
})

# 데이터 B: 한 행 = 국가 x 연도 x 산업  (단위가 다르다!)
trade = pd.DataFrame({
    "country":  ["Korea"] * 4 + ["Japan"] * 4,
    "year":     [2023, 2023, 2024, 2024] * 2,
    "industry": ["Semiconductor", "Auto"] * 4,
    "export":   [50, 30, 55, 32, 40, 60, 42, 61],
})

# ------------------------------------------------------------
# 1. merge 전 검증 습관 3종 세트
# ------------------------------------------------------------
key = ["country", "year"]
print("gdp   shape:", gdp.shape)
print("trade shape:", trade.shape)
print("gdp   key 중복 수:", gdp.duplicated(key).sum())      # 0 -> key가 unique
print("trade key 중복 수:", trade.duplicated(key).sum())    # >0 -> 단위가 더 세밀함

# ------------------------------------------------------------
# 2. 1:m merge — 의도된 복제인지 반드시 확인
# ------------------------------------------------------------
merged = trade.merge(gdp, on=key, how="left", validate="m:1")  # validate로 안전장치!
print("\nmerge 후 shape:", merged.shape, "(trade 행 수와 같아야 정상)")
print(merged)

# ------------------------------------------------------------
# 3. 사고 시연: 단위를 무시하고 gdp 기준으로 merge하면?
# ------------------------------------------------------------
bad = gdp.merge(trade, on=key, how="left")
print("\ngdp(4행)에 trade를 붙였더니 shape:", bad.shape, "-> 관측치가 복제됨!")

# validate 옵션이 잘못된 가정을 잡아내는 예
try:
    gdp.merge(trade, on=key, how="left", validate="1:1")
except Exception as e:
    print("\nvalidate='1:1' 오류 발생 (의도된 안전장치):")
    print(" ", type(e).__name__, "-", str(e)[:80])

# ------------------------------------------------------------
# 4. indicator로 매칭 실패 진단
# ------------------------------------------------------------
gdp2 = gdp[gdp["country"] != "Japan"]  # 일부러 Japan 누락
chk = trade.merge(gdp2, on=key, how="left", indicator=True)
print("\n_merge 분포:\n", chk["_merge"].value_counts())
