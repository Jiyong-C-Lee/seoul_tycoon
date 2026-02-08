# 밸런싱 데이터 구조

게임의 모든 밸런싱 수치는 `data/` 폴더의 JSON 파일로 관리됩니다.

## 📁 파일 구조

```
data/
├── building_data.json    # 건물 관련 데이터
└── economy_data.json     # 경제 시스템 데이터
```

---

## 🏢 building_data.json

**건물, 등급, 입지** 관련 모든 데이터

### 포함 내용

| 섹션 | 설명 | 주요 데이터 |
|-----|------|----------|
| `types` | 건물 타입별 속성 | 가격, 수익률, 시장 반응 |
| `grades` | 등급 시스템 | C/B/A/S급 계수 |
| `locations` | 입지 계수 | 역세권, 공원, 일반 |
| `rental` | 임대료 조정 | 공실률 영향 (Phase 2+) |
| `remodeling` | 리모델링 | 비용, 효과 (Phase 2+) |

### 사용 예시

```python
import json

with open('data/building_data.json', 'r', encoding='utf-8') as f:
    BUILDINGS = json.load(f)

# 주거 건물 기본 가격
residential_base = BUILDINGS['types']['residential']['price']['base']

# C급 건물 계수
c_grade_coef = BUILDINGS['grades']['C']['coefficient_avg']

# 역세권 월간 보너스
subway_bonus = BUILDINGS['locations']['subway_nearby']['monthly_bonus']
```

---

## 💰 economy_data.json

**시장, 거래, 대출, 이벤트** 관련 모든 데이터

### 포함 내용

| 섹션 | 설명 | 주요 데이터 |
|-----|------|----------|
| `market` | 시장 파라미터 | Global Trend, 금리, Market Index |
| `price_algorithm` | 가격 변동 로직 | 변동 범위, Fair Value, NPC 매물 |
| `trading` | 거래 비용 및 대출 | 취득세, 할인율, LTV, 금리 |
| `credit_score` | 신용도 시스템 | 점수 변화 규칙 |
| `game_start` | 게임 시작 조건 | 초기 자본, 건물, 연도 |
| `win_lose_conditions` | 승패 조건 | 파산 기준, 등급 기준 |
| `events` | 이벤트 시스템 | 확률, 영향, 예시 |
| `time` | 시간 설정 | 게임 속도, 총 기간 |
| `growth_targets` | 성장 목표 | 5/10/20/30년 목표 곡선 |

### 사용 예시

```python
import json

with open('data/economy_data.json', 'r', encoding='utf-8') as f:
    ECONOMY = json.load(f)

# Global Trend 초기값
initial_trend = ECONOMY['market']['global_trend']['initial_value']

# LTV 기본 비율
ltv = ECONOMY['trading']['loan']['ltv_default']

# 취득세율
tax_rate = ECONOMY['trading']['costs']['acquisition_tax_rate']

# S등급 기준 순자산
s_grade = ECONOMY['win_lose_conditions']['final_grades']['S']
```

---

## 🎯 데이터 접근 패턴

### 건물 가격 계산 예시

```python
# 주거 C급 역세권 건물의 적정 가치 계산
base_price = BUILDINGS['types']['residential']['price']['base']
grade_coef = BUILDINGS['grades']['C']['coefficient_avg']
location_coef = BUILDINGS['locations']['subway_nearby']['price_coefficient_avg']
market_index = ECONOMY['market']['market_index']['initial']

fair_value = base_price * grade_coef * location_coef * (market_index / 100)
# = 8억 × 0.7 × 1.3 × 1.0 = 7.28억
```

### 월별 임대료 계산 예시

```python
building_price = 728000000  # 위에서 계산한 가격
rental_yield = BUILDINGS['types']['residential']['rental_yield']['annual_average']

monthly_rent = building_price * rental_yield / 12
# = 7.28억 × 0.0525 / 12 = 약 319만원
```

### 대출 금리 계산 예시

```python
base_rate = ECONOMY['trading']['loan']['interest_base_rate']
credit_premium = ECONOMY['trading']['loan']['credit_score_premium']['90_100']

total_rate = base_rate + credit_premium
# = 0.03 + 0.005 = 0.035 (3.5%)
```

---

## 🔧 밸런싱 조정 방법

### 1. JSON 파일 직접 수정

가장 간단한 방법. 파일을 열어서 수치만 변경:

```json
"residential": {
  "rental_yield": {
    "annual_min": 0.045,    // 4.5% → 5.0%로 변경 가능
    "annual_max": 0.060,
    "annual_average": 0.0525
  }
}
```

### 2. Git으로 버전 관리

```bash
git diff data/economy_data.json    # 변경 사항 확인
git commit -m "임대 수익률 5% 상향 조정"
```

### 3. 시뮬레이터로 검증

밸런싱 변경 후 Python 시뮬레이터로 30년 성장 테스트

---

## 📌 주의사항

### 1. 데이터 일관성

- 연관된 값들을 함께 조정 (예: LTV 올리면 금리도 조정)
- 계산 결과가 0 또는 음수가 되지 않도록 주의

### 2. 단위 통일

- 금액: 원 단위 (정수)
- 비율: 소수점 (0.01 = 1%)
- 기간: 개월 수

### 3. MVP vs Phase 2+

`mvp_enabled` 플래그 확인:
- `true`: MVP에 포함
- `false`: Phase 2+ 에서 구현

---

## 🔗 기획서 연계

기획서에서는 구체적 수치 대신 **데이터 참조 형태**로 작성:

```markdown
# 기획서 예시
주거 건물의 연 수익률: `building_data.types.residential.rental_yield` 참조
```

이렇게 하면:
- ✅ 기획서는 로직과 구조에 집중
- ✅ 밸런싱 조정은 JSON 파일에서만
- ✅ 기획서 수정 없이 숫자만 빠르게 조정 가능

---

## 📝 변경 이력

| 날짜 | 파일 | 변경 내용 |
|-----|------|----------|
| 2026-02-08 | - | 초기 생성 (v1.0.0) |

---

**마지막 업데이트**: 2026-02-08  
**버전**: 1.0.0
