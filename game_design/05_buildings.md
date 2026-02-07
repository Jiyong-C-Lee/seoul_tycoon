## 문서 정보
- **게임명**: 서울 부동산 타이쿤
- **문서**: 건물 속성과 특징
- **버전**: 1.0

---

## 1. 건물 데이터 구조 (Building)

```python
class Building:
    id: str                # 고유 ID
    name: str              # 건물명
    building_type: str     # 건물 유형 ("아파트", "빌라", "편의점" 등)
    category: str          # 카테고리 ("주거", "상업", "복합")

    # 위치
    x: int                 # 맵 X 좌표
    y: int                 # 맵 Y 좌표
    region: str            # 소속 지역

    # 가격
    base_price: int        # 기준 가격
    current_price: int     # 현재 시세
    purchase_price: int    # 매수 가격 (플레이어가 소유한 경우)

    # 수익성
    rental_yield: float    # 연간 임대 수익률 (예: 0.04 = 4%)

    # 상태
    owner: str             # 소유자 ("player", "npc", "market")
    is_for_sale: bool      # 매물 여부
```

---

## 2. 건물 카테고리

| 카테고리 | 설명 |
|----------|------|
| 주거 | 아파트, 빌라 등 주거용 건물 |
| 상업 | 편의점, 상가 등 상업용 건물 |
| 복합 | 주거 + 상업 복합 건물 |

---

## 3. 건물 유형

| 유형 | 카테고리 | 설명 |
|------|----------|------|
| 아파트 | 주거 | (추후 상세 확정) |
| 빌라 | 주거 | (추후 상세 확정) |
| 편의점 | 상업 | (추후 상세 확정) |
| (추후 확장) | | |

---

## 4. 소유 상태

| 소유자 | 설명 |
|--------|------|
| `player` | 플레이어 소유 |
| `npc` | NPC 소유 (매수 불가) |
| `market` | 시장 매물 (매수 가능) |

---

## 5. 수익성

- **연간 임대 수익률**: 건물별로 설정 (예: 4%)
- **월간 임대 수익**: `현재가 × (연간 수익률 / 12)`

---

## 관련 문서
- 매수/매도 프로세스 → [03_economy_simulation.md](03_economy_simulation.md)
- 시세 변동 → [03_economy_simulation.md](03_economy_simulation.md)
- 소속 지역 정보 → [04_regions.md](04_regions.md)
