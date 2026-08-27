# 데이터처리실무 — 주차별 실습 코드 (통계학과 3학년)

최종 16주 강의안의 실습 주차에 대응하는 실행 가능한 Python 코드입니다.
모든 파일은 외부 데이터 없이 자체 생성 데이터로 즉시 실행됩니다 (Colab/로컬 모두 가능).

## 사전 설치
```bash
pip install numpy pandas statsmodels scikit-learn duckdb polars pyarrow pandera requests
```

## 파일 구성
| 파일 | 주차 | 내용 |
|---|---|---|
| week01_vectorization.py | 1주 | Loop vs Vectorization 실행시간 비교, Broadcasting, Tidy Data |
| week02_pandas_basics.py | 2주 | DataFrame 구조 파악, loc/iloc, Boolean filtering, dtype, groupby |
| week03_reshape_panel.py | 3주 | melt/pivot, groupby+shift/diff/pct_change/rolling, 국가 경계를 넘는 lag 실수 시연 |
| week04_merge_granularity.py | 4주 | merge 전 검증 3종(shape/nunique/duplicated), validate= 옵션, indicator 진단 |
| week05_missing_data.py | 5주 | MCAR/MAR/MNAR 시뮬레이션으로 편향 확인, Simple→KNN→Iterative 비교 |
| week06_outlier_cooks.py | 6주 | Outlier/Leverage/Influential 구분, Cook's D, 제거 전후 회귀계수 비교 |
| week07_string_regex.py | 7주 | strip/replace/extract, 숫자형 변환, category dtype 메모리 비교 |
| week09_sql_duckdb.py | 9주 | 동일 연산의 pandas vs SQL 병렬 비교, DataFrame/CSV 직접 쿼리 |
| week10_api_json.py | 10주 | World Bank API 호출, 중첩 JSON 탐색 습관, json_normalize (오프라인 fallback 포함) |
| week11_memory_polars.py | 11주 | dtype 최적화 메모리 절약, chunk 처리, Polars 20~30분 demo |
| week12_feature_engineering.py | 12주 | log/표준화/더미/상호작용/시차 → Design Matrix, formula와의 연결 |
| week13_pipeline_validation.py | 13주 | 수작업 validation → Pandera, Data Leakage 시연, ColumnTransformer+Pipeline |
| week14_15_project_template.py | 14~15주 | Raw→Clean→Integration→Validation→Codebook 자동 생성 템플릿 |

## 수업 활용 팁
- 각 파일의 "실수 시연" 부분(3주차 lag, 4주차 관측치 복제, 13주차 누수)은
  학생이 직접 결과를 비교하게 한 뒤 토론으로 연결하면 효과적입니다.
- 6주차는 인위적으로 심은 세 관측치(outlier / leverage / influential) 중
  어떤 것이 계수를 실제로 움직였는지 찾게 하는 과제로 확장 가능합니다.
