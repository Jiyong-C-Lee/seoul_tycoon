## 문서 정보
- **게임명**: 서울 부동산 타이쿤
- **문서**: 핵심 엔티티 정의
- **버전**: 1.0

---

## 1. 플레이어 (Player)

```python
class Player:
    cash: int              # 보유 현금 (초기: 500,000,000원)
    buildings: List[Building]  # 보유 건물 목록
    loans: List[Loan]      # 대출 목록

    # 계산 속성
    @property
    def total_building_value(self) -> int:
        """보유 부동산 총 가치"""
        return sum(b.current_price for b in self.buildings)

    @property
    def total_assets(self) -> int:
        """총 자산 (현금 + 부동산)"""
        return self.cash + self.total_building_value

    @property
    def total_debt(self) -> int:
        """총 부채"""
        return sum(loan.remaining for loan in self.loans)
```

### 초기 상태
| 속성 | 값 |
|------|-----|
| 보유 현금 | 5억원 |
| 보유 건물 | 없음 |
| 대출 | 없음 |

---

## 2. 맵 (Map)

```python
class Map:
    width: int             # 맵 가로 크기 (타일 수)
    height: int            # 맵 세로 크기 (타일 수)
    tiles: List[List[Tile]]  # 2D 타일 배열
    current_level: int     # 현재 맵 레벨 (1~5)

    regions: Dict[str, Region]  # 지역 정보
    # 예: {"강남구": Region(...), "서초구": Region(...)}
```

### 초기 상태
| 속성 | 값 |
|------|-----|
| 크기 | 20x20 |
| 초기 레벨 | 1 |
| 초기 지역 | 강남구 |

---

## 3. 타일 (Tile)

```python
class Tile:
    x: int                 # X 좌표
    y: int                 # Y 좌표
    terrain_type: str      # 지형 타입 ("land", "river", "park", "mountain")
    building: Optional[Building]  # 건물 (없으면 None)
    region: str            # 소속 지역 ("강남구", "서초구" 등)
```

### 지형 타입
| 타입 | 설명 |
|------|------|
| `land` | 일반 토지 (건물 배치 가능) |
| `river` | 강 (건물 배치 불가) |
| `park` | 공원 (건물 배치 불가) |
| `mountain` | 산 (건물 배치 불가) |

---

## 4. 게임 상태 (GameState)

```python
class GameState:
    # 시간
    current_month: int     # 현재 월 (0~359)
    current_year: int      # 현재 년도 (계산: month // 12)
    elapsed_time: float    # 경과 시간 (초)

    # 게임 상태
    state: str             # "menu", "playing", "game_over", "game_clear"
    is_paused: bool        # 일시정지 여부
    time_speed: int        # 시간 속도 (1, 2, 4)

    # 참조
    player: Player         # 플레이어
    map: Map               # 맵
    buildings: List[Building]  # 모든 건물
    events: List[Event]    # 발생한 이벤트 히스토리
```

---

## 관련 문서
- 건물(Building) 상세 → [05_buildings.md](05_buildings.md)
- 이벤트(Event) 상세 → [06_events.md](06_events.md)
- 지역(Region) 상세 → [04_regions.md](04_regions.md)
