"""경제 시스템 - 정산, 시세 변동, 매수/매도"""
import random

from game.core.constants import (
    BANKRUPTCY_LIMIT,
    MAINTENANCE_RATE,
    TAX_RATE_BUY,
    TAX_RATE_SELL,
)
from game.data.models import Building, GameState


def process_monthly_settlement(state: GameState) -> int:
    """월별 정산: 임대 수익 입금, 관리비 차감. 순수익 반환."""
    total_income = 0
    for b in state.player.buildings:
        # 임대 수익
        monthly_rent = int(b.current_price * b.rental_yield / 12)
        total_income += monthly_rent
        # 관리비/세금
        monthly_maintenance = int(b.current_price * MAINTENANCE_RATE / 12)
        total_income -= monthly_maintenance
    state.player.cash += total_income
    return total_income


def update_prices(state: GameState) -> None:
    """모든 건물 시세 변동"""
    for b in state.buildings:
        # 1. 기본 변동률 (-2% ~ +3%)
        base_change = random.uniform(-0.02, 0.03)

        # 2. 활성 이벤트 효과
        event_change = 0.0
        for event in state.active_events:
            price_changes = event.effects.get("price_change", {})
            if b.region in price_changes:
                # 이벤트 효과를 월별로 분할 적용
                if event.duration > 0:
                    multiplier = price_changes[b.region]
                    event_change += (multiplier - 1.0) / event.duration

        total_change = 1.0 + base_change + event_change
        b.current_price = max(10_000_000, int(b.current_price * total_change))


def can_buy(state: GameState, building: Building) -> bool:
    """매수 가능 여부 확인"""
    total_cost = building.current_price + int(building.current_price * TAX_RATE_BUY)
    return (
        building.is_for_sale
        and building.owner == "market"
        and state.player.cash >= total_cost
    )


def buy_building(state: GameState, building: Building) -> bool:
    """건물 매수. 성공 여부 반환."""
    if not can_buy(state, building):
        return False
    tax = int(building.current_price * TAX_RATE_BUY)
    total_cost = building.current_price + tax
    state.player.cash -= total_cost
    building.owner = "player"
    building.is_for_sale = False
    building.purchase_price = building.current_price
    state.player.buildings.append(building)
    return True


def sell_building(state: GameState, building: Building) -> bool:
    """건물 매도. 성공 여부 반환."""
    if building.owner != "player":
        return False
    tax = int(building.current_price * TAX_RATE_SELL)
    proceeds = building.current_price - tax
    state.player.cash += proceeds
    building.owner = "market"
    building.is_for_sale = True
    building.purchase_price = 0
    state.player.buildings.remove(building)
    return True


def check_bankruptcy(state: GameState) -> bool:
    """파산 체크. 파산이면 True."""
    return state.player.cash < BANKRUPTCY_LIMIT
