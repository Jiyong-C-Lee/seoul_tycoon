# 시간 관리 시스템 (Time Management)

> **목적**: 게임 시간 진행, 월별 정산, 일시정지 메커니즘 정의  
> **시간 설정**: `data/economy_data.json` 참조

---

## 📋 개요

이 문서는 다음을 정의합니다:

1. **시간 진행 메커니즘** - 실시간 vs 게임 시간 변환
2. **월별 정산 프로세스** - 매월 1일 자동 실행 순서
3. **일시정지 시스템** - 자동 정지 조건
4. **게임 속도 조절** - 1x/2x/4x 배속
5. **이벤트 타이밍** - 월별 체크 및 발생

---

## 1. 시간 구조

### 1.1 게임 시간 단위

| 단위 | 설명 | 비고 |
|-----|------|------|
| **1개월** | 게임 내 기본 단위 | 모든 정산의 기준 |
| **1년** | 12개월 | 통계 표시용 |
| **30년** | 360개월 | 게임 총 기간 |

### 1.2 실시간 vs 게임 시간 변환

**기본 시간 흐름**:
```
실시간 1초 = 게임 내 1일
실시간 30초 = 게임 내 1개월 (30일)
실시간 6분 = 게임 내 1년 (12개월)
실시간 180분 = 게임 내 30년 (3시간)
```

데이터 참조: `economy_data.time.real_time_per_game_day_seconds`

### 1.3 게임 속도 옵션

| 속도 | 배율 | 실시간 1개월 | 실시간 30년 |
|-----|------|------------|-----------|
| **1x** (기본) | 1배 | 30초 | 3시간 |
| **2x** | 2배 | 15초 | 1.5시간 |
| **4x** | 4배 | 7.5초 | 45분 |

**MVP**: 1x 속도만 구현, Phase 2+에서 배속 추가

---

## 2. 게임 시작 시퀀스

### 2.1 초기화 순서

게임 시작 시 다음 순서로 초기화:

```
1. 데이터 로딩
   - building_data.json
   - economy_data.json
   - map_data.json

2. GameState 생성
   - current_month = 0 (2004년 1월)
   - current_year = 2004
   - is_paused = True (시작 시 일시정지)

3. Market 초기화
   - global_trend = 0.2
   - market_index = 100
   - base_interest_rate = 0.03

4. Player 초기화
   - cash = 500,000,000
   - debt = 0
   - owned_buildings = []

5. 맵 및 건물 생성
   - map_data.json 기반으로 Tile 생성
   - buildings 리스트 생성
   - Fair Value 계산

6. 플레이어 초기 건물 할당
   - map_data.initial_player_building 참조
   - B_002를 플레이어에게 할당
   - 초기 비용 차감
   - owned_buildings에 추가

7. UI 초기 렌더링
   - 맵 표시
   - 플레이어 정보 표시
   - 일시정지 상태 표시

8. 대기
   - 플레이어가 시간 진행 버튼 클릭 대기
```

### 2.2 초기 화면

게임 시작 시 플레이어가 보는 정보:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  서울 부동산 타이쿤
  
  📅 2004년 1월
  💰 현금: 45,500,000원
  🏢 보유 건물: 1개
  📈 순자산: 495,500,000원
  
  시작하려면 ▶ 버튼을 클릭하세요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 3. 월별 정산 프로세스

### 3.1 정산 실행 타이밍

**매월 1일 0시 (게임 시간)** 자동 실행

실시간 기준으로는 **30초마다** (1x 속도 기준)

### 3.2 정산 순서 (6단계)

매월 1일에 다음 순서로 실행:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1: 시간 증가
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  current_month += 1
  current_year = 2004 + (current_month // 12)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 2: Market 업데이트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  - Global Trend 변동 (랜덤 + 이벤트)
  - Market Index 계산
  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 3: 건물 가격 업데이트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  모든 건물에 대해:
    - Fair Value 업데이트 (안정적)
    - Current Price 업데이트 (변동성)
    - (08_price_algorithm.md 로직 적용)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 4: 임대료 수입 처리
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  플레이어 소유 건물에 대해:
    monthly_rent = calculate_rent(building)
    player.cash += monthly_rent
    
    거래 기록:
      log_transaction("rent", amount=monthly_rent)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 5: 대출 이자 차감 (Phase 2+)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  대출이 있으면:
    monthly_interest = total_debt × (annual_rate / 12)
    player.cash -= monthly_interest
    
    거래 기록:
      log_transaction("interest", amount=-monthly_interest)
    
    현금 부족 시:
      player.unpaid_interest_months += 1
      player.credit_score -= 5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 6: 이벤트 발생 체크
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  - 5% 확률로 랜덤 이벤트 발생
  - 2008년 9월 체크 (금융위기)
  - 이벤트 발생 시 → 게임 일시정지
```

### 3.3 정산 후 처리

```
7. 순자산 재계산
   player.total_assets = cash + Σ(building.current_price)
   player.net_worth = total_assets - total_debt

8. 파산 체크
   if net_worth < -500,000,000:
       → 게임 오버
   
   if unpaid_interest_months >= 12:
       → 게임 오버

9. 게임 종료 체크
   if current_month >= 360:
       → 최종 결산

10. UI 업데이트
    - 시세 차트 갱신
    - 플레이어 정보 갱신
    - 건물 가격 표시 갱신
```

### 3.4 정산 로직 (의사코드)

```python
def monthly_settlement(game_state: GameState):
    """매월 1일 실행되는 정산"""
    
    # Step 1: 시간 증가
    game_state.current_month += 1
    game_state.current_year = 2004 + (game_state.current_month // 12)
    
    # Step 2: Market 업데이트
    update_global_trend(game_state.market)
    game_state.market.market_index = calculate_market_index(game_state)
    
    # Step 3: 건물 가격 업데이트
    for building in game_state.buildings.values():
        update_building_price(building, game_state.market)
    
    # Step 4: 임대료 수입
    monthly_income = 0
    for building_id in game_state.player.owned_buildings:
        building = game_state.buildings[building_id]
        rent = calculate_monthly_rent(building)
        monthly_income += rent
    
    game_state.player.cash += monthly_income
    log_transaction(game_state, "rent", monthly_income)
    
    # Step 5: 대출 이자 (Phase 2+)
    if game_state.player.total_debt > 0:
        interest = calculate_monthly_interest(game_state.player)
        game_state.player.cash -= interest
        log_transaction(game_state, "interest", -interest)
        
        if game_state.player.cash < 0:
            game_state.player.unpaid_interest_months += 1
            game_state.player.credit_score -= 5
    
    # Step 6: 이벤트 체크
    check_and_trigger_events(game_state)
    
    # Step 7~10: 후처리
    update_player_stats(game_state.player)
    check_game_over(game_state)
    update_ui(game_state)
```

---

## 4. 일시정지 시스템

### 4.1 자동 일시정지 조건

게임이 **자동으로 일시정지**되는 경우:

| 조건 | 설명 |
|-----|------|
| **게임 시작** | 플레이어가 준비할 시간 제공 |
| **이벤트 발생** | 뉴스 확인 및 선택지 대응 |
| **매물 발견** | 새 매물이 시장에 나왔을 때 (Phase 2+) |
| **경고 발생** | 현금 부족, 파산 위기 등 |
| **플레이어 수동 정지** | ⏸ 버튼 클릭 |

### 4.2 일시정지 UI

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⏸ 일시정지

  📅 2010년 3월
  
  [이벤트 알림]
  🗞️ 호재: "테헤란로 재개발 확정"
  → 시장 추세 +0.3 (3개월간)
  
  [ 확인하고 계속하기 ]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4.3 플레이어 인터랙션

일시정지 상태에서 플레이어 가능 행동:

```
✅ 가능:
  - 지도 탐색
  - 건물 정보 확인
  - 시세 차트 보기
  - 뉴스 읽기
  - 재정 상태 확인
  - 매수/매도 (거래는 즉시 실행)

❌ 불가능:
  - 시간 흐름 (정지 상태)
  - 임대료 수입 (월 단위)
  - 가격 변동 (월 단위)
```

### 4.4 재개 조건

| 버튼 | 동작 |
|-----|------|
| **▶ 계속하기** | 정상 속도로 재개 |
| **⏩ 빠르게 진행** | 2x 속도 (Phase 2+) |
| **⏭ 다음 달로** | 1개월 즉시 진행 후 정지 (Phase 2+) |

---

## 5. 게임 속도 조절

### 5.1 속도 옵션 (Phase 2+)

| 속도 | 효과 | 사용 시기 |
|-----|------|----------|
| **⏸ 일시정지** | 시간 정지 | 분석 및 의사결정 |
| **▶ 1x** | 기본 속도 | 일반 플레이 |
| **⏩ 2x** | 2배속 | 안정기 |
| **⏭ 4x** | 4배속 | 장기 관망 |

### 5.2 MVP 간소화

**MVP에서는**:
- ⏸ 일시정지 / ▶ 재개 만 구현
- 속도는 1x 고정
- Phase 2에서 배속 추가

---

## 6. 이벤트 타이밍

### 6.1 이벤트 발생 시점

```
매월 정산 시 (Step 6):
  
  1. 랜덤 이벤트 체크
     if random() < 0.05:  # 5% 확률
         event = random_choice(["good_news", "bad_news"])
         trigger_event(event)
         → 게임 일시정지
  
  2. 스크립트 이벤트 체크
     if current_year == 2008 and current_month % 12 == 9:
         trigger_event("financial_crisis")
         → 게임 일시정지
```

### 6.2 이벤트 효과 적용

```
이벤트 발생 시:
  1. Global Trend에 즉시 영향
     market.global_trend += event.impact
  
  2. 지속 기간 설정
     event.end_month = current_month + duration
  
  3. 이벤트 큐에 저장
     game_state.events_queue.append(event)

매월 체크:
  for event in events_queue:
      if current_month >= event.end_month:
          # 효과 종료
          market.global_trend -= event.impact
          events_queue.remove(event)
```

---

## 7. 실시간 루프 구현

### 7.1 메인 게임 루프

```python
def game_loop(game_state: GameState):
    """메인 게임 루프 (프레임 단위)"""
    
    last_settlement_time = time.time()
    
    while not game_state.is_game_over:
        # 현재 시간
        current_time = time.time()
        
        # 일시정지 상태면 대기
        if game_state.is_paused:
            time.sleep(0.1)
            continue
        
        # 1개월 경과 체크 (30초)
        elapsed = current_time - last_settlement_time
        if elapsed >= 30.0:  # 1x 속도 기준
            monthly_settlement(game_state)
            last_settlement_time = current_time
        
        # UI 업데이트 (매 프레임)
        update_ui(game_state)
        
        # 프레임 제한 (60 FPS)
        time.sleep(1/60)
```

### 7.2 시간 표시 업데이트

UI에 표시되는 날짜는 **부드럽게 증가**:

```python
def get_display_date(game_state: GameState, elapsed: float):
    """현재 표시할 날짜 계산"""
    
    base_month = game_state.current_month
    
    # 30초 = 1개월이므로, 경과 시간에 비례
    day_progress = int((elapsed / 30.0) * 30) + 1
    
    year = 2004 + (base_month // 12)
    month = (base_month % 12) + 1
    day = min(day_progress, 30)
    
    return f"{year}년 {month}월 {day}일"
```

---

## 8. 게임 종료

### 8.1 정상 종료 (30년 경과)

```
current_month == 360 도달 시:

1. 게임 일시정지
2. 최종 결산 화면 표시
3. 등급 계산
4. 최종 통계 표시
5. "다시 하기" / "종료" 선택
```

### 8.2 파산 (게임 오버)

```
파산 조건 충족 시:

1. 게임 일시정지
2. 파산 사유 표시
   - "순자산 -5억 이하"
   - "12개월 연속 이자 연체"
3. 파산 경고 화면
4. "다시 하기" / "종료" 선택
```

### 8.3 최종 결산 로직

```python
def calculate_final_grade(game_state: GameState):
    """최종 등급 계산"""
    
    net_worth = game_state.player.net_worth
    
    # economy_data.win_lose_conditions.final_grades 참조
    if net_worth >= 100_000_000_000:
        return "S"
    elif net_worth >= 50_000_000_000:
        return "A"
    elif net_worth >= 10_000_000_000:
        return "B"
    elif net_worth >= 5_000_000_000:
        return "C"
    elif net_worth >= 1_000_000_000:
        return "D"
    elif net_worth >= 100_000_000:
        return "E"
    else:
        return "F"
```

---

## 9. MVP 구현 요약

### 9.1 필수 구현 항목

- [x] 월별 정산 6단계 로직
- [x] 일시정지/재개 기능
- [x] 임대료 수입 자동 처리
- [x] 건물 가격 월별 업데이트
- [x] 게임 시작 시퀀스
- [x] 게임 종료 조건 체크
- [ ] 실시간 루프 구현
- [ ] UI 시간 표시

### 9.2 Phase 2+ 확장

- [ ] 게임 속도 조절 (2x, 4x)
- [ ] 대출 이자 처리
- [ ] 복잡한 이벤트 시스템
- [ ] 저장/불러오기
- [ ] 다음 달로 건너뛰기

---

## 10. 구현 참고 코드

### 10.1 임대료 계산

```python
def calculate_monthly_rent(building: Building, balancing_data: dict):
    """건물의 월 임대료 계산"""
    
    building_type = balancing_data['buildings']['types'][building.type]
    annual_yield = building_type['rental_yield']['annual_average']
    
    # 월 임대료 = 건물 가격 × 연 수익률 / 12
    monthly_rent = int(building.current_price * annual_yield / 12)
    
    # MVP: 공실률 고정 5%
    vacancy_rate = 0.05
    actual_rent = int(monthly_rent * (1 - vacancy_rate))
    
    return actual_rent
```

### 10.2 시간 진행 관리

```python
class TimeManager:
    """시간 진행 관리 클래스"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.last_settlement = time.time()
        self.month_duration = 30.0  # 1x 속도 기준
    
    def update(self):
        """매 프레임 호출"""
        if self.game_state.is_paused:
            return
        
        elapsed = time.time() - self.last_settlement
        
        if elapsed >= self.month_duration:
            self.execute_monthly_settlement()
            self.last_settlement = time.time()
    
    def execute_monthly_settlement(self):
        """월별 정산 실행"""
        monthly_settlement(self.game_state)
```

---

## 11. 다음 단계 연계

이 시간 관리 시스템을 바탕으로:

1. **Python 구현**: TimeManager 클래스 개발
2. **UI 연동**: 시간 표시 및 일시정지 버튼
3. **테스트**: 30초마다 정산 실행 확인
4. **밸런싱**: 임대료/이자 수치 조정

---

## 부록: 타임라인 예시

**게임 시작 후 3분 경과 시**:

```
실시간 0:00 → 게임 2004년 1월 1일
  (플레이어가 ▶ 버튼 클릭)

실시간 0:30 → 게임 2004년 2월 1일
  정산: 임대료 +225만원
  
실시간 1:00 → 게임 2004년 3월 1일
  정산: 임대료 +225만원
  
실시간 1:30 → 게임 2004년 4월 1일
  정산: 임대료 +225만원
  이벤트: "호재 뉴스" 발생 → 일시정지
  
실시간 1:35 → (플레이어가 확인 후 재개)

실시간 2:00 → 게임 2004년 5월 1일
  정산: 임대료 +225만원

실시간 3:00 → 게임 2004년 7월 1일
  누적 수입: 1,350만원
  현금: 5,885만원
```

**설계 의도**: 30초마다 정산이 느껴지지 않을 정도로 자연스러운 흐름
