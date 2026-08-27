"""
[10주차] API + JSON + 공공데이터
World Bank API 예시 (인터넷이 안 되는 환경을 위해 offline fallback 포함)
"""
import json
import pandas as pd

# ------------------------------------------------------------
# 1. API 호출 (수업에서는 실제로 호출)
#    World Bank: 한국의 GDP (NY.GDP.MKTP.CD)
# ------------------------------------------------------------
URL = ("https://api.worldbank.org/v2/country/KOR/indicator/"
       "NY.GDP.MKTP.CD?format=json&date=2019:2023")

raw = None
try:
    import requests
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()
    raw = resp.json()
    print("API 호출 성공!")
except Exception as e:
    print(f"API 호출 실패({type(e).__name__}) -> 저장된 샘플 JSON 사용")
    raw = json.loads("""
    [{"page":1,"pages":1,"per_page":50,"total":5},
     [{"indicator":{"id":"NY.GDP.MKTP.CD","value":"GDP (current US$)"},
       "country":{"id":"KR","value":"Korea, Rep."},
       "date":"2023","value":1712793464725.0},
      {"indicator":{"id":"NY.GDP.MKTP.CD","value":"GDP (current US$)"},
       "country":{"id":"KR","value":"Korea, Rep."},
       "date":"2022","value":1673916213838.0},
      {"indicator":{"id":"NY.GDP.MKTP.CD","value":"GDP (current US$)"},
       "country":{"id":"KR","value":"Korea, Rep."},
       "date":"2021","value":1818432173911.0},
      {"indicator":{"id":"NY.GDP.MKTP.CD","value":"GDP (current US$)"},
       "country":{"id":"KR","value":"Korea, Rep."},
       "date":"2020","value":1644312846908.0},
      {"indicator":{"id":"NY.GDP.MKTP.CD","value":"GDP (current US$)"},
       "country":{"id":"KR","value":"Korea, Rep."},
       "date":"2019","value":1651422932447.0}]]
    """)

# ------------------------------------------------------------
# 2. JSON 구조 탐색 습관: 무작정 DataFrame으로 바꾸지 말 것
# ------------------------------------------------------------
print("\n최상위 타입:", type(raw), "| 길이:", len(raw))
print("raw[0] (메타데이터):", raw[0])
print("raw[1][0] (첫 레코드 키):", list(raw[1][0].keys()))

# ------------------------------------------------------------
# 3. 중첩 JSON -> tidy DataFrame
# ------------------------------------------------------------
records = raw[1]
df = pd.DataFrame({
    "country": [r["country"]["value"] for r in records],
    "year":    [int(r["date"]) for r in records],
    "gdp_usd": [r["value"] for r in records],
}).sort_values("year").reset_index(drop=True)

df["gdp_tril"] = (df["gdp_usd"] / 1e12).round(3)
df["growth_%"] = (df["gdp_usd"].pct_change() * 100).round(2)
print("\n[정리된 데이터]"); print(df[["country", "year", "gdp_tril", "growth_%"]])

# json_normalize 소개
flat = pd.json_normalize(records)
print("\njson_normalize 결과 컬럼:", flat.columns.tolist())
