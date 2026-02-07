## 문서 정보
- **게임명**: 서울 부동산 타이쿤
- **문서**: 이벤트 인카운터
- **버전**: 1.0

---

## 1. 이벤트 데이터 구조 (Event)

```python
class Event:
    id: str                # 이벤트 ID
    name: str              # 이벤트명
    description: str       # 설명
    event_type: str        # 유형 ("정책", "개발", "경제", "인구")

    # 발생 정보
    trigger_month: int     # 발생 월
    duration: int          # 지속 기간 (개월)

    # 효과
    effects: Dict[str, Any]  # 효과 데이터
    # 예: {"price_change": {"강남구": 1.1, "서초구": 1.05}}

    affected_regions: List[str]  # 영향 받는 지역
    affected_building_types: List[str]  # 영향 받는 건물 유형
```

---

## 2. 이벤트 유형

| 유형 | 설명 |
|------|------|
| 정책 | 정부 부동산 정책 변화 |
| 개발 | 지역 개발/인프라 확충 |
| 경제 | 경기 변동, 금리 변화 등 |
| 인구 | 인구 이동, 수요 변화 |

---

## 3. 이벤트 발생 프로세스

```
[매월 초]
    ↓
[이벤트 시스템]
    - 랜덤 확률 체크 (예: 10%)
    ↓
[이벤트 선택]
    - 현재 게임 상황에 맞는 이벤트 풀에서 선택
    ↓
[이벤트 적용]
    - 효과 계산
    - 건물 시세에 반영
    - UI 알림 표시
    ↓
[히스토리 기록]
    - GameState.events에 추가
```

### 발생 확률
- 매월 초 랜덤 확률 체크 (예: 10%)
- 이벤트 풀에서 현재 상황에 맞는 이벤트 선택

---

## 4. 효과 적용 방식

- **지역 대상**: `affected_regions`에 명시된 지역의 건물에만 적용
- **건물 유형 대상**: `affected_building_types`에 명시된 유형에만 적용
- **지속 기간**: `duration` 개월 동안 효과 유지
- **시세 반영**: `effects.price_change`를 통해 시세 변동에 반영

### 효과 예시
```python
# 강남구 시세 10% 상승, 서초구 시세 5% 상승 이벤트
effects = {
    "price_change": {
        "강남구": 1.1,
        "서초구": 1.05
    }
}
```

---

## 관련 문서
- 시세 변동 로직 → [03_economy_simulation.md](03_economy_simulation.md)
- 지역 정보 → [04_regions.md](04_regions.md)
- 건물 유형 → [05_buildings.md](05_buildings.md)
