# 경제 시스템 (Economy System)

> **목적**: 게임 내 경제 시스템의 구조와 로직을 정의  
> **세부 밸런싱 수치**: `balancing_data.json` 참조

---

## 📋 개요

이 문서는 다음 경제 요소의 **구조와 메커니즘**을 정의합니다:

1. **건물 가격 체계** - 가격 결정 구조
2. **임대료 시스템** - 수익 계산 구조
3. **대출 및 금융** - 대출 메커니즘
4. **거래 비용** - 세금 구조
5. **리모델링 경제** - 효과 시스템
6. **초기 게임 설정** - 시작 조건

---

## 1. 건물 가격 체계

### 1.1 가격 결정 구조

건물 가격은 **5가지 요소의 곱**으로 결정됩니다:

```
최종 가격 = 기본 가격 × 유형 계수 × 등급 계수 × 입지 계수 × 시장 계수
```

| 요소 | 설명 | 데이터 참조 |
|-----|------|-----------|
| **기본 가격** | 건물 유형별 베이스 가격 | `balancing_data.building_prices` |
| **유형 계수** | 주거/상업/오피스 | 기본 1.0 |
| **등급 계수** | C/B/A/S 등급 | `balancing_data.grade_coefficients` |
| **입지 계수** | 역세권/공원/일반 | `balancing_data.location_coefficients` |
| **시장 계수** | 동적 변동 | `Market.market_index / 100` |

### 1.2 건물 유형

게임에는 **3가지 건물 유형**이 존재합니다:

| 유형 | 영문 코드 | 특징 |
|-----|----------|------|
| **주거** | `residential` | 오피스텔, 빌라, 아파트 |
| **상업** | `commercial` | 상가, 음식점, 소매점 |
| **오피스** | `office` | 사무실, 업무용 빌딩 |

구체적인 가격 범위는 `balancing_data.json` 참조

### 1.3 등급 시스템

| 등급 | 설명 | MVP 포함 |
|-----|------|---------|
| **C급** | 노후 건물, 낮은 층수 | ✅ |
| **B급** | 일반 건물, 중간 품질 | ✅ |
| **A급** | 신축, 고급 건물 | ✅ |
| **S급** | 랜드마크, 프리미엄 | ❌ (Phase 4+) |

등급별 계수는 `balancing_data.grade_coefficients` 참조

### 1.4 입지 조건

MVP에서는 각 건물에 **고정 입지 계수** 부여:

| 입지 | 조건 | 효과 |
|-----|------|------|
| **역세권** | 지하철역 200m 이내 | 가격 상승, 월간 보너스 |
| **공원 인접** | 공원/녹지 인접 | 중간 보너스 |
| **일반** | 특별 조건 없음 | 기본값 |

구체적인 계수는 `balancing_data.location_coefficients` 참조

### 1.5 시장 계수 (동적)

- **초기값**: 1.0 (Market Index = 100)
- **변동**: `08_price_algorithm.md`에 정의된 로직에 따라 월별 변동
- **30년 목표**: 시장 평균 4~6배 성장

---

## 2. 임대료 시스템

### 2.1 기본 임대료 공식

```
기본 월 임대료 = 건물 가격 × 연 수익률 ÷ 12개월
```

### 2.2 유형별 수익률

각 건물 유형은 **고유한 연 수익률 범위**를 가집니다:

| 유형 | 특징 | 데이터 참조 |
|-----|------|-----------|
| **주거** | 안정적 수익 | `balancing_data.rental_yields.residential` |
| **상업** | 중간 수익 | `balancing_data.rental_yields.commercial` |
| **오피스** | 낮지만 안정 | `balancing_data.rental_yields.office` |

### 2.3 임대료 조정 (Phase 2+)

플레이어는 기본 임대료 대비 **일정 범위 내에서 조정 가능**:

| 조정 전략 | 영향 |
|---------|------|
| **고임대료** | 수익 증가, 공실률 증가 |
| **적정임대료** | 균형 유지 |
| **저임대료** | 수익 감소, 공실률 감소 |

조정 범위 및 공실률 영향은 `balancing_data.rental_adjustment` 참조

### 2.4 실제 수입 계산

```
실제 월 수입 = 실제 임대료 × (1 - 공실률)
```

**MVP 간소화**: 공실률 고정, 플레이어 조정 불가

---

## 3. 대출 및 금융 시스템

### 3.1 대출 한도 (LTV)

```
대출 가능 한도 = 보유 건물 평가액 합계 × LTV 비율
```

LTV 비율은 `balancing_data.loan_parameters.ltv_ratio` 참조

### 3.2 이자율 구조

```
대출 금리 = 기준 금리 + 가산 금리
```

| 구성 요소 | 결정 요인 | 데이터 참조 |
|---------|----------|-----------|
| **기준 금리** | 시장 상황 (변동) | `balancing_data.market_parameters.base_interest_rate` |
| **가산 금리** | 플레이어 신용도 | `balancing_data.loan_parameters.interest_rate.credit_score_premium` |

### 3.3 이자 계산 및 상환

- **상환 방식**: 원금 만기 일시 상환
- **이자 납부**: 매월 자동 차감

```
월 이자 = 대출 원금 × (연 금리 ÷ 12)
```

### 3.4 신용도 시스템

플레이어 **신용 점수**(0~100)는 다음 상황에서 변동:

| 상황 | 효과 | 데이터 참조 |
|-----|------|-----------|
| 정상 납부 | 변동 없음 | - |
| 이자 연체 | 점수 감소 | `balancing_data.credit_score.changes` |
| 부채 상환 | 점수 증가 | `balancing_data.credit_score.changes` |
| 12개월 연속 연체 | **파산** | - |

---

## 4. 거래 비용 및 세금

### 4.1 매수 시 비용

```
총 매수 비용 = 건물 가격 + 취득세
취득세 = 건물 가격 × 취득세율
```

취득세율은 `balancing_data.trading_costs.acquisition_tax_rate` 참조

### 4.2 매도 시

#### A. 즉시 매도 (시스템 매각)
```
매도 수익 = 현재 시세 × (1 - 즉시 매도 할인율)
```

할인율은 `balancing_data.trading_costs.instant_sale_discount` 참조

#### B. 매물 등록 (Post-MVP)
- 플레이어가 희망가 설정
- 시장 상황에 따라 판매 소요 시간 변동
- Phase 2+ 에서 추가

### 4.3 양도소득세 (MVP 제외)

- **MVP**: 복잡도 감소를 위해 제외
- **Phase 2+**: 추가 검토

---

## 5. 리모델링 경제 (MVP 제외, Phase 2+)

### 5.1 비용 구조

```
리모델링 비용 = 현재 건물 가치 × 비용 비율
```

비용 비율은 `balancing_data.remodeling.cost_ratio` 참조

### 5.2 효과

| 효과 | 설명 | 데이터 참조 |
|-----|------|-----------|
| **내구도 회복** | 100으로 복구 | - |
| **상태 등급 상승** | 2단계 상승 | - |
| **가치 증가** | 건물 시세 상승 | `balancing_data.remodeling.effects.value_increase` |
| **임대료 증가** | 수익 향상 | `balancing_data.remodeling.effects.rent_increase` |
| **공실률 감소** | 품질 개선 | `balancing_data.remodeling.effects.vacancy_decrease` |

### 5.3 제약

- **공사 기간**: 데이터에 정의된 개월 수
- **기간 중 임대료**: 0원 (공실)

공사 기간은 `balancing_data.remodeling.duration_months` 참조

---

## 6. 초기 게임 설정

### 6.1 플레이어 시작 조건

| 항목 | 데이터 참조 |
|-----|-----------|
| 초기 현금 | `balancing_data.initial_settings.player.initial_cash` |
| 초기 건물 수 | `balancing_data.initial_settings.player.initial_buildings` |
| 초기 부채 | `balancing_data.initial_settings.player.initial_debt` |
| 시작 연도 | `balancing_data.initial_settings.player.start_year` |

### 6.2 MVP 고정 설정

개발 편의를 위해 **MVP는 단일 시작 조건**:
- 건물 1개 보유 (상업 C급)
- 일정 현금 잔액

구체적 값은 `balancing_data.initial_settings.mvp_starting_building` 참조

### 6.3 Phase 2+ 확장

- 다양한 초기 건물 선택지
- 난이도별 시작 조건 (보수적/균형/공격적)
- 초기 대출 활용 옵션

---

## 7. 현금 흐름 구조

### 7.1 월별 수입

```
월 총 수입 = Σ(각 건물의 실제 월 임대료)
실제 월 임대료 = 기본 임대료 × (1 - 공실률)
```

### 7.2 월별 지출

```
월 총 지출 = Σ(각 대출의 월 이자)
월 이자 = 대출 원금 × (연 금리 ÷ 12)
```

### 7.3 순 현금 흐름

```
월 순 현금 흐름 = 월 총 수입 - 월 총 지출
```

**안전 마진 권장**: 순 현금 흐름 \u003e 0 유지

---

## 8. 파산 조건

| 조건 | 기준 | 데이터 참조 |
|-----|------|-----------|
| **순자산 기준** | 일정 금액 이하 | `balancing_data.bankruptcy_conditions.net_worth_threshold` |
| **연체 기준** | 연속 연체 개월 수 초과 | `balancing_data.bankruptcy_conditions.consecutive_overdue_months` |

---

## 9. 최종 등급 시스템

30년 후 순자산 기준으로 등급 부여:

| 등급 | 순자산 기준 |
|-----|----------|
| S ~ F | `balancing_data.final_grades` 참조 |

---

## 10. 다음 단계 연계

이 경제 시스템을 바탕으로:

1. **`08_price_algorithm.md`**: 시장 계수의 월별 변동 로직
2. **`10_time_management.md`**: 월별 정산 타이밍 및 프로세스  
3. **`13_map_design.md`**: 역삼동 건물 정의
4. **밸런싱 테스트**: `balancing_data.json` 수정하며 시뮬레이션

---

## 11. 구현 참고사항

### 11.1 데이터 로딩

게임 시작 시 `balancing_data.json` 파일을 읽어 메모리에 로드:

```python
import json

with open('balancing_data.json', 'r', encoding='utf-8') as f:
    BALANCING = json.load(f)

# 사용 예시
base_price = BALANCING['building_prices']['residential']['base_price']
ltv_ratio = BALANCING['loan_parameters']['ltv_ratio']['default']
```

### 11.2 소수점 처리

- 모든 금액은 **정수 (원 단위)** 저장
- 계산 중 소수점 발생 시 `round()` 또는 `int()` 사용

### 11.3 동적 가격 업데이트

- 매월 `Market.global_trend`에 따라 모든 건물 가격 재계산
- `Building.current_price` 및 `Building.fair_value` 업데이트
- 로직은 `08_price_algorithm.md` 참조

---

## 12. MVP 구현 체크리스트

### Phase 1 필수 구현
- [x] 건물 가격 계산 로직
- [x] 임대료 수익률 (고정 공실률)
- [x] 취득세 적용
- [x] 즉시 매도 (할인 적용)
- [x] 초기 설정 로드
- [ ] 월별 정산 로직 (`10_time_management.md` 연계)

### Phase 2 이후
- [ ] 플레이어 임대료 조정 UI
- [ ] 공실률 동적 계산
- [ ] 리모델링 시스템
- [ ] 대출 시스템
- [ ] 신용도 시스템
- [ ] 다양한 초기 건물 선택지

---

## 부록: 설계 의도

**복잡한 세금 제거**: 취득세만 적용, 양도세 제외  
**수익률 상향**: 현실보다 높은 임대 수익률로 빠른 성장 가능  
**전략에 집중**: 타이밍 포착과 레버리지 활용이 핵심

구체적인 비교는 `balancing_data.json` 주석 참조
