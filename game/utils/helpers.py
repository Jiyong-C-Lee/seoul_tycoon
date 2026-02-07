"""유틸리티 함수"""
import random

from game.core.constants import (
    BUILDING_TYPES,
    MAP_HEIGHT,
    MAP_WIDTH,
)
from game.data.models import Building, Tile


def format_money(amount: int) -> str:
    """금액을 억/만원 단위로 포맷"""
    if amount < 0:
        return "-" + format_money(-amount)
    if amount >= 100_000_000:
        eok = amount // 100_000_000
        remainder = (amount % 100_000_000) // 10_000
        if remainder > 0:
            return f"{eok}억 {remainder:,}만원"
        return f"{eok}억원"
    if amount >= 10_000:
        return f"{amount // 10_000:,}만원"
    return f"{amount:,}원"


def generate_map() -> list[list[Tile]]:
    """20x20 타일 맵 생성 (강, 공원 포함)"""
    tiles: list[list[Tile]] = []
    for y in range(MAP_HEIGHT):
        row: list[Tile] = []
        for x in range(MAP_WIDTH):
            terrain = "land"
            # 강: 맵 하단 2줄
            if y >= MAP_HEIGHT - 2:
                terrain = "river"
            # 공원: 몇 군데 고정
            elif (x, y) in {(5, 5), (5, 6), (6, 5), (6, 6),
                            (14, 10), (14, 11), (15, 10), (15, 11)}:
                terrain = "park"
            # 산: 우상단 코너
            elif x >= MAP_WIDTH - 3 and y <= 2:
                terrain = "mountain"
            row.append(Tile(x=x, y=y, terrain_type=terrain, region="강남구"))
        tiles.append(row)
    return tiles


def place_buildings(tiles: list[list[Tile]]) -> list[Building]:
    """빈 land 타일에 건물 랜덤 배치"""
    land_tiles: list[Tile] = []
    for row in tiles:
        for tile in row:
            if tile.terrain_type == "land" and tile.building is None:
                land_tiles.append(tile)

    random.shuffle(land_tiles)
    num_buildings = min(18, len(land_tiles))
    buildings: list[Building] = []

    for i in range(num_buildings):
        tile = land_tiles[i]
        btype, category, price_min, price_max, rental_yield = random.choice(
            BUILDING_TYPES
        )
        base_price = random.randint(price_min // 10_000_000, price_max // 10_000_000) * 10_000_000
        # 일부는 NPC 소유 (매수 불가)
        if i < 3:
            owner = "npc"
            is_for_sale = False
        else:
            owner = "market"
            is_for_sale = True

        building = Building(
            id=f"building_{i:03d}",
            name=f"{tile.region} {btype} {i + 1}",
            building_type=btype,
            category=category,
            x=tile.x,
            y=tile.y,
            region=tile.region,
            base_price=base_price,
            current_price=base_price,
            rental_yield=rental_yield,
            owner=owner,
            is_for_sale=is_for_sale,
        )
        tile.building = building
        buildings.append(building)

    return buildings
