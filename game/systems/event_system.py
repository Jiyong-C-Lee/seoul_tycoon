"""이벤트 시스템 - 랜덤 이벤트 발생 및 적용"""
import copy
import random

from game.core.constants import EVENT_CHANCE
from game.data.models import Event, GameState

EVENT_POOL: list[Event] = [
    Event(
        id="evt_policy_01",
        name="부동산 규제 강화",
        description="정부가 부동산 규제를 강화하여 시세가 하락합니다.",
        event_type="정책",
        duration=6,
        effects={"price_change": {"강남구": 0.90}},
        affected_regions=["강남구"],
    ),
    Event(
        id="evt_policy_02",
        name="부동산 규제 완화",
        description="정부가 부동산 규제를 완화하여 시세가 상승합니다.",
        event_type="정책",
        duration=6,
        effects={"price_change": {"강남구": 1.10}},
        affected_regions=["강남구"],
    ),
    Event(
        id="evt_dev_01",
        name="지하철 신규 노선 착공",
        description="강남구에 새 지하철 노선이 착공됩니다. 주거 시세 상승!",
        event_type="개발",
        duration=12,
        effects={"price_change": {"강남구": 1.15}},
        affected_regions=["강남구"],
        affected_building_types=["아파트", "빌라", "오피스텔"],
    ),
    Event(
        id="evt_econ_01",
        name="금리 인상",
        description="한국은행이 기준금리를 인상했습니다. 전반적 시세 하락.",
        event_type="경제",
        duration=6,
        effects={"price_change": {"강남구": 0.92}},
        affected_regions=["강남구"],
    ),
    Event(
        id="evt_econ_02",
        name="경기 호황",
        description="경기가 호황을 맞아 상업용 부동산 시세가 상승합니다.",
        event_type="경제",
        duration=8,
        effects={"price_change": {"강남구": 1.12}},
        affected_regions=["강남구"],
        affected_building_types=["편의점", "상가"],
    ),
    Event(
        id="evt_pop_01",
        name="인구 유입 증가",
        description="강남구로 인구가 유입되며 주거 수요가 급증합니다.",
        event_type="인구",
        duration=10,
        effects={"price_change": {"강남구": 1.08}},
        affected_regions=["강남구"],
        affected_building_types=["아파트", "빌라"],
    ),
]


def check_and_trigger_event(state: GameState) -> Event | None:
    """매월 확률적으로 이벤트 발생. 발생한 이벤트 반환, 없으면 None."""
    if random.random() > EVENT_CHANCE:
        return None

    # 현재 활성 이벤트와 중복되지 않는 이벤트 선택
    active_ids = {e.id for e in state.active_events}
    available = [e for e in EVENT_POOL if e.id not in active_ids]
    if not available:
        return None

    event = copy.deepcopy(random.choice(available))
    event.trigger_month = state.current_month
    event.remaining_months = event.duration

    state.active_events.append(event)
    state.event_history.append(event)
    return event


def update_active_events(state: GameState) -> None:
    """활성 이벤트 duration 감소, 만료 처리"""
    still_active: list[Event] = []
    for event in state.active_events:
        event.remaining_months -= 1
        if event.remaining_months > 0:
            still_active.append(event)
    state.active_events = still_active
