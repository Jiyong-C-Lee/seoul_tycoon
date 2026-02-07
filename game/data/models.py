"""게임 데이터 모델 정의"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Building:
    id: str
    name: str
    building_type: str  # "아파트", "빌라", "편의점" 등
    category: str       # "주거", "상업", "복합"
    x: int
    y: int
    region: str
    base_price: int
    current_price: int
    rental_yield: float  # 연간 임대 수익률
    owner: str = "market"  # "player", "npc", "market"
    is_for_sale: bool = True
    purchase_price: int = 0


@dataclass
class Tile:
    x: int
    y: int
    terrain_type: str  # "land", "river", "park", "mountain"
    region: str = "강남구"
    building: Building | None = None


@dataclass
class Region:
    name: str
    base_trend: float = 0.002  # 월별 기본 상승 추세
    unlocked: bool = True


@dataclass
class Player:
    cash: int
    buildings: list[Building] = field(default_factory=list)

    @property
    def total_building_value(self) -> int:
        return sum(b.current_price for b in self.buildings)

    @property
    def total_assets(self) -> int:
        return self.cash + self.total_building_value


@dataclass
class Event:
    id: str
    name: str
    description: str
    event_type: str  # "정책", "개발", "경제", "인구"
    duration: int  # 지속 개월
    effects: dict[str, Any] = field(default_factory=dict)
    affected_regions: list[str] = field(default_factory=list)
    affected_building_types: list[str] = field(default_factory=list)
    remaining_months: int = 0
    trigger_month: int = 0


@dataclass
class GameState:
    current_month: int = 0
    state: str = "menu"  # "menu", "playing", "game_over", "game_clear"
    is_paused: bool = False
    time_speed: int = 1  # 1, 2, 4
    player: Player = field(default_factory=lambda: Player(cash=0))
    tiles: list[list[Tile]] = field(default_factory=list)
    buildings: list[Building] = field(default_factory=list)
    active_events: list[Event] = field(default_factory=list)
    event_history: list[Event] = field(default_factory=list)
    elapsed_time: float = 0.0
    selected_building: Building | None = None
    event_notification: str = ""
    event_notification_timer: float = 0.0

    @property
    def current_year(self) -> int:
        return self.current_month // 12 + 1

    @property
    def current_month_in_year(self) -> int:
        return self.current_month % 12 + 1
