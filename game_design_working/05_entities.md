# 게임 엔티티 구조 정의 (Entities Structure)

> **목적**: 게임 내 모든 엔티티의 데이터 구조를 정의하여 Python class 구현의 설계도로 활용

---

## 📋 엔티티 개요

이 문서는 다음 엔티티들을 정의합니다:

1. **Building** - 건물
2. **Tile** - 그리드 타일
3. **Player** - 플레이어 상태
4. **Market** - 시장 상태
5. **Event** - 이벤트
6. **Transaction** - 거래 기록
7. **GameState** - 전체 게임 상태

---

## 1. Building (건물)

### 1.1 속성 (Attributes)

| 속성명 | 타입 | 설명 | 기본값 | 비고 |
|-------|------|------|--------|------|
| `id` | `str` | 건물 고유 ID | - | UUID 또는 "B_001" 형식 |
| `name` | `str` | 건물 이름 | - | 예: "역삼 오피스텔 A동" |
| `type` | `str` | 건물 유형 | - | `"residential"` / `"commercial"` / `"office"` |
| `grade` | `str` | 건물 등급 | `"C"` | `"C"` / `"B"` / `"A"` / `"S"` |
| `position` | `tuple[int, int]` | 그리드 좌표 | - | `(x, y)` 형식 |
| `size` | `tuple[int, int]` | 건물 크기 | `(1, 1)` | 그리드 칸 수 `(width, height)` |
| `current_price` | `int` | 현재 시세 | - | 원 단위 |
| `purchase_price` | `int` | 매입가 | `0` | 플레이어가 산 가격 (소유 시에만) |
| `base_rent` | `int` | 기본 월 임대료 | - | 원 단위 |
| `actual_rent` | `int` | 실제 월 임대료 | - | 플레이어가 설정한 임대료 |
| `condition` | `str` | 건물 상태 | `"normal"` | `"old"` / `"normal"` / `"renovated"` |
| `durability` | `int` | 내구도 | `100` | 0~100, 시간 경과로 감소 |
| `vacancy_rate` | `float` | 공실률 | `0.0` | 0.0~1.0 (0% ~ 100%) |
| `is_for_sale` | `bool` | 매물 여부 | `False` | True면 매수 가능 |
| `owner` | `str` | 소유주 | `"NPC"` | `"player"` / `"NPC"` / `"system"` |
| `is_under_renovation` | `bool` | 리모델링 중 | `False` | True면 임대료 없음 |
| `renovation_end_month` | `int` | 리모델링 종료 월 | `None` | 게임 내 월 수 |
| `landmark` | `bool` | 랜드마크 여부 | `False` | 특수 건물 표시 |

### 1.2 메서드 (Methods)

```python
# 주요 메서드 후보
def calculate_monthly_income() -> int:
    """월 임대료 수입 계산 (공실률, 리모델링 반영)"""
    pass

def apply_depreciation(months: int) -> None:
    """시간 경과에 따른 내구도 감소"""
    pass

def renovate() -> None:
    """리모델링 시작"""
    pass

def complete_renovation() -> None:
    """리모델링 완료 처리"""
    pass

def update_price(new_price: int) -> None:
    """시세 업데이트"""
    pass

def sell() -> int:
    """건물 매도, 매도가 반환"""
    pass
```

### 1.3 연관 관계
- **Player**: 소유주 관계 (`owner == "player"`)
- **Tile**: 위치 관계 (`position` 좌표)
- **Market**: 시세 변동 영향 받음

---

## 2. Tile (그리드 타일)

### 2.1 속성 (Attributes)

| 속성명 | 타입 | 설명 | 기본값 | 비고 |
|-------|------|------|--------|------|
| `position` | `tuple[int, int]` | 좌표 | - | `(x, y)` |
| `terrain_type` | `str` | 지형 타입 | `"empty"` | `"road"` / `"park"` / `"water"` / `"empty"` |
| `building_id` | `str` | 건물 ID | `None` | 이 타일에 있는 건물 (있으면) |
| `overlay` | `str` | 오버레이 | `None` | `"subway"` / `"bus_stop"` 등 |
| `district` | `str` | 소속 지역 | - | 예: "역삼동" |

### 2.2 메서드 (Methods)

```python
def get_building() -> Building:
    """이 타일의 건물 반환"""
    pass

def is_walkable() -> bool:
    """건물이 없는 빈 타일인지"""
    pass
```

---

## 3. Player (플레이어)

### 3.1 속성 (Attributes)

| 속성명 | 타입 | 설명 | 기본값 | 비고 |
|-------|------|------|--------|------|
| `cash` | `int` | 보유 현금 | `500_000_000` | 5억 원 시작 |
| `total_assets` | `int` | 총 자산 | - | 현금 + 건물 평가액 |
| `total_debt` | `int` | 총 부채 | `0` | 대출 원금 합계 |
| `net_worth` | `int` | 순자산 | - | 총 자산 - 총 부채 |
| `owned_buildings` | `list[str]` | 보유 건물 ID 리스트 | `[]` | Building ID 리스트 |
| `monthly_income` | `int` | 월 수입 | `0` | 임대료 합계 |
| `monthly_expense` | `int` | 월 지출 | `0` | 대출 이자 합계 |
| `credit_score` | `int` | 신용 점수 | `100` | 0~100, 대출 금리에 영향 |
| `unpaid_interest_months` | `int` | 이자 연체 월 수 | `0` | 12개월 도달 시 파산 |

### 3.2 메서드 (Methods)

```python
def calculate_total_assets() -> int:
    """총 자산 계산"""
    pass

def calculate_net_worth() -> int:
    """순자산 계산"""
    pass

def buy_building(building: Building) -> bool:
    """건물 매수"""
    pass

def sell_building(building_id: str) -> int:
    """건물 매도"""
    pass

def monthly_settlement() -> None:
    """월별 정산 (임대료 수입, 이자 지출)"""
    pass

def check_bankruptcy() -> bool:
    """파산 여부 확인"""
    pass
```

---

## 4. Market (시장 상태)

### 4.1 속성 (Attributes)

| 속성명 | 타입 | 설명 | 기본값 | 비고 |
|-------|------|------|--------|------|
| `base_interest_rate` | `float` | 기준 금리 | `0.03` | 3% (연 단위) |
| `global_trend` | `float` | 시장 추세 | `0.0` | -1.0 ~ 1.0 (하락 ~ 상승) |
| `ltv_ratio` | `float` | LTV 한도 | `0.7` | 건물 가치의 70% |
| `market_index` | `int` | 시장 지수 | `100` | 초기값 100, 시세 변동 추적 |
| `transaction_tax_rate` | `float` | 취등록세율 | `0.01` | 1% |

### 4.2 메서드 (Methods)

```python
def update_trend(event_impact: float) -> None:
    """시장 추세 업데이트"""
    pass

def calculate_interest_rate(credit_score: int) -> float:
    """플레이어 신용 점수 기반 대출 금리 계산"""
    pass
```

---

## 5. Event (이벤트)

### 5.1 속성 (Attributes)

| 속성명 | 타입 | 설명 | 기본값 | 비고 |
|-------|------|------|--------|------|
| `id` | `str` | 이벤트 ID | - | 예: "E_001" |
| `title` | `str` | 이벤트 제목 | - | 예: "GTX 노선 발표" |
| `description` | `str` | 이벤트 설명 | - | 뉴스 본문 |
| `event_type` | `str` | 이벤트 유형 | - | `"policy"` / `"development"` / `"economy"` / `"building"` |
| `trigger_month` | `int` | 발생 월 | - | 게임 내 몇 번째 월 |
| `impact_type` | `str` | 영향 대상 | - | `"global"` / `"regional"` / `"building"` |
| `choices` | `list[dict]` | 선택지 | `None` | 선택 가능한 옵션들 |
| `auto_apply` | `bool` | 자동 적용 여부 | `True` | False면 플레이어 선택 필요 |

### 5.2 Choice 구조 (선택지)

```python
# choices 리스트의 각 항목 구조
{
    "choice_id": "C_001",
    "text": "규제 완화 지지",
    "success_rate": 0.7,  # 성공 확률
    "success_effect": {"global_trend": +0.2, "ltv_ratio": +0.1},
    "failure_effect": {"global_trend": -0.1}
}
```

### 5.3 메서드 (Methods)

```python
def apply_effect(game_state: GameState, choice_id: str = None) -> None:
    """이벤트 효과 적용"""
    pass

def roll_success(success_rate: float) -> bool:
    """확률 판정"""
    pass
```

---

## 6. Transaction (거래 기록)

### 6.1 속성 (Attributes)

| 속성명 | 타입 | 설명 | 기본값 | 비고 |
|-------|------|------|--------|------|
| `transaction_id` | `str` | 거래 ID | - | 고유 식별자 |
| `month` | `int` | 거래 시점 | - | 게임 내 월 |
| `transaction_type` | `str` | 거래 유형 | - | `"buy"` / `"sell"` / `"rent"` / `"interest"` |
| `building_id` | `str` | 건물 ID | `None` | 해당하는 경우 |
| `amount` | `int` | 금액 | - | 양수: 수입, 음수: 지출 |
| `description` | `str` | 설명 | - | 예: "역삼 오피스텔 A동 매수" |

### 6.2 메서드 (Methods)

```python
def log_transaction(player: Player, transaction_type: str, amount: int, ...) -> None:
    """거래 기록 생성"""
    pass
```

---

## 7. GameState (전체 게임 상태)

### 7.1 속성 (Attributes)

| 속성명 | 타입 | 설명 | 기본값 | 비고 |
|-------|------|------|--------|------|
| `current_month` | `int` | 현재 게임 월 | `0` | 0 = 2004년 1월 |
| `current_year` | `int` | 현재 연도 | `2004` | 계산값 |
| `game_speed` | `int` | 게임 속도 | `1` | 1 / 2 / 4 배속 |
| `is_paused` | `bool` | 일시정지 상태 | `True` | 시작 시 일시정지 |
| `player` | `Player` | 플레이어 객체 | - | - |
| `market` | `Market` | 시장 상태 객체 | - | - |
| `buildings` | `dict[str, Building]` | 모든 건물 | `{}` | Building ID를 key로 |
| `tiles` | `dict[tuple, Tile]` | 모든 타일 | `{}` | (x, y) 좌표를 key로 |
| `events_queue` | `list[Event]` | 예정 이벤트 | `[]` | 시간순 정렬 |
| `transactions_history` | `list[Transaction]` | 거래 내역 | `[]` | 전체 거래 기록 |
| `is_game_over` | `bool` | 게임 종료 여부 | `False` | True면 게임 종료 |
| `final_grade` | `str` | 최종 등급 | `None` | `"S"` ~ `"F"` |

### 7.2 메서드 (Methods)

```python
def advance_month() -> None:
    """1개월 진행"""
    pass

def process_monthly_events() -> None:
    """월별 이벤트 처리"""
    pass

def check_game_over() -> bool:
    """게임 종료 조건 확인"""
    pass

def calculate_final_grade() -> str:
    """최종 등급 계산"""
    pass

def save_game(filepath: str) -> None:
    """게임 저장"""
    pass

def load_game(filepath: str) -> None:
    """게임 불러오기"""
    pass
```

---

## 8. 엔티티 간 관계도

```
GameState
  ├── Player
  │     └── owned_buildings (list[Building ID])
  ├── Market
  ├── buildings (dict)
  │     └── Building (소유주: player/NPC)
  ├── tiles (dict)
  │     └── Tile (건물 참조)
  ├── events_queue (list)
  │     └── Event
  └── transactions_history (list)
        └── Transaction
```

---

## 9. 구현 우선순위

### Phase 1: MVP 필수 엔티티
1. ✅ **Building** - 기본 속성만 (리모델링, 세입자 제외)
2. ✅ **Tile** - 간단한 그리드
3. ✅ **Player** - 현금, 자산, 건물 목록
4. ✅ **Market** - 기준 금리, 추세만
5. ✅ **GameState** - 시간 진행, 월별 정산
6. ⚠️ **Event** - 최소한의 시세 변동 이벤트만
7. ⚠️ **Transaction** - 옵션 (디버깅용)

### Phase 2 이후
- Building: 리모델링, 세입자, 내구도 시스템
- Event: 복잡한 선택지, 정책 개입
- Transaction: 상세 통계 및 차트

---

## 10. 다음 단계

이 엔티티 구조를 바탕으로:
1. **`06_economy_system.md`**: Building 가격, 임대료 수치 정의
2. **`08_price_algorithm.md`**: Market과 Building의 가격 변동 로직
3. **Python 구현**: 각 엔티티를 dataclass 또는 class로 구현

---

## 11. 추가 고려사항

### 11.1 데이터 저장 형식
- **JSON 직렬화 가능하도록 설계** (딕셔너리 변환 메서드 필요)
- Python `dataclass` 또는 `pydantic` 활용 권장

### 11.2 타입 힌팅
- 모든 속성에 타입 힌팅 적용 (`int`, `str`, `list[str]` 등)
- `Optional[type]` 사용으로 None 가능 속성 명시

### 11.3 유효성 검사
- 예: `durability`는 0~100 범위 제한
- 예: `grade`는 "C", "B", "A", "S"만 허용

### 11.4 확장성
- 추후 건물 유형 추가 시 `type` enum화 고려
- 이벤트 시스템 확장 시 상속 구조 검토
