"""
[3주차] Long/Wide 변환(melt/pivot) + 패널 데이터 처리(Lag/Rolling)
통계학과 학생에게 가장 중요한 주차 중 하나
"""
import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 1. Wide -> Long (melt)
# ------------------------------------------------------------
wide = pd.DataFrame({
    "country": ["Korea", "Japan"],
    "GDP_2022": [100, 200],
    "GDP_2023": [105, 205],
    "GDP_2024": [110, 208],
})
print("[Wide]"); print(wide)

long = wide.melt(id_vars="country", var_name="year", value_name="GDP")
long["year"] = long["year"].str.extract(r"(\d{4})").astype(int)
long = long.sort_values(["country", "year"]).reset_index(drop=True)
print("\n[Long]"); print(long)

# ------------------------------------------------------------
# 2. Long -> Wide (pivot)
# ------------------------------------------------------------
wide_again = long.pivot(index="country", columns="year", values="GDP")
print("\n[다시 Wide]"); print(wide_again)

# ------------------------------------------------------------
# 3. 패널 데이터에서 Lag / 변화율 / Rolling
#    핵심: 반드시 groupby 후에 shift/rolling 을 적용해야 함!
# ------------------------------------------------------------
long["GDP_lag1"] = long.groupby("country")["GDP"].shift(1)
long["GDP_diff"] = long.groupby("country")["GDP"].diff()
long["GDP_growth"] = long.groupby("country")["GDP"].pct_change() * 100
long["GDP_ma2"] = (long.groupby("country")["GDP"]
                       .rolling(2).mean()
                       .reset_index(level=0, drop=True))
print("\n[패널 변수 생성]"); print(long)

# ------------------------------------------------------------
# 4. 흔한 실수 시연: groupby 없이 shift 하면?
# ------------------------------------------------------------
wrong = long.copy()
wrong["GDP_lag_wrong"] = wrong["GDP"].shift(1)   # Japan 첫 행에 Korea 값이 들어감!
print("\n[잘못된 lag: 국가 경계를 넘어감]")
print(wrong[["country", "year", "GDP", "GDP_lag_wrong"]])
