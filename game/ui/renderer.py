"""렌더링 시스템 - 모든 화면 그리기"""
import pygame

from game.core.constants import (
    CATEGORY_COLORS,
    COLOR_BG,
    COLOR_BLACK,
    COLOR_BUTTON,
    COLOR_BUTTON_DANGER,
    COLOR_BUTTON_HOVER,
    COLOR_DARK_GRAY,
    COLOR_GRAY,
    COLOR_HIGHLIGHT,
    COLOR_LAND,
    COLOR_LIGHT_GRAY,
    COLOR_MOUNTAIN,
    COLOR_NEGATIVE,
    COLOR_PANEL,
    COLOR_PANEL_BORDER,
    COLOR_PARK,
    COLOR_PLAYER_BORDER,
    COLOR_POSITIVE,
    COLOR_RIVER,
    COLOR_WHITE,
    FONT_NAME,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
    TOTAL_MONTHS,
)
from game.data.models import GameState
from game.systems.economy import can_buy
from game.utils.helpers import format_money

TERRAIN_COLORS = {
    "land": COLOR_LAND,
    "river": COLOR_RIVER,
    "park": COLOR_PARK,
    "mountain": COLOR_MOUNTAIN,
}


class Renderer:
    def __init__(self) -> None:
        self.font_large = pygame.font.SysFont(FONT_NAME, 48)
        self.font_medium = pygame.font.SysFont(FONT_NAME, 24)
        self.font_small = pygame.font.SysFont(FONT_NAME, 16)
        self.font_tiny = pygame.font.SysFont(FONT_NAME, 13)

    # ── 메인 메뉴 ──────────────────────────────────────────
    def draw_menu(self, screen: pygame.Surface, state: GameState) -> pygame.Rect:
        """메뉴 화면. '게임 시작' 버튼 Rect 반환."""
        screen.fill(COLOR_BG)

        # 타이틀
        title = self.font_large.render("서울 부동산 타이쿤", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title, title_rect)

        # 서브타이틀
        sub = self.font_medium.render(
            "30년 안에 최대한 자산을 모으세요!", True, COLOR_LIGHT_GRAY
        )
        sub_rect = sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
        screen.blit(sub, sub_rect)

        # 게임 시작 버튼
        btn_rect = pygame.Rect(0, 0, 240, 56)
        btn_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        mouse_pos = pygame.mouse.get_pos()
        color = COLOR_BUTTON_HOVER if btn_rect.collidepoint(mouse_pos) else COLOR_BUTTON
        pygame.draw.rect(screen, color, btn_rect, border_radius=8)
        btn_text = self.font_medium.render("게임 시작", True, COLOR_WHITE)
        screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

        # 조작법
        controls = [
            "SPACE: 일시정지  |  1/2/4: 속도  |  ESC: 선택 취소",
            "건물 클릭: 매수/매도",
        ]
        for i, line in enumerate(controls):
            txt = self.font_small.render(line, True, COLOR_GRAY)
            screen.blit(
                txt,
                txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 + i * 24)),
            )

        return btn_rect

    # ── 플레이 중 ──────────────────────────────────────────
    def draw_playing(
        self, screen: pygame.Surface, state: GameState
    ) -> dict[str, list]:
        """플레이 화면. 클릭 가능 영역 dict 반환."""
        screen.fill(COLOR_BG)
        clickables: dict[str, list] = {
            "buildings": [],
            "buttons": [],
        }

        self._draw_top_panel(screen, state)
        self._draw_map(screen, state, clickables)
        self._draw_bottom_panel(screen, state, clickables)
        if state.selected_building:
            self._draw_building_popup(screen, state, clickables)
        if state.event_notification_timer > 0:
            self._draw_event_notification(screen, state)

        return clickables

    def _draw_top_panel(self, screen: pygame.Surface, state: GameState) -> None:
        panel = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        pygame.draw.rect(screen, COLOR_PANEL, panel)
        pygame.draw.line(screen, COLOR_PANEL_BORDER, (0, 50), (SCREEN_WIDTH, 50))

        # 시간
        year_month = f"{state.current_year}년차 {state.current_month_in_year}월"
        txt = self.font_medium.render(year_month, True, COLOR_WHITE)
        screen.blit(txt, (16, 12))

        # 진행률 바
        progress = state.current_month / TOTAL_MONTHS
        bar_x, bar_y, bar_w, bar_h = 180, 18, 120, 14
        pygame.draw.rect(screen, COLOR_DARK_GRAY, (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        fill_w = int(bar_w * progress)
        if fill_w > 0:
            pygame.draw.rect(screen, COLOR_BUTTON, (bar_x, bar_y, fill_w, bar_h), border_radius=4)
        pct_txt = self.font_tiny.render(f"{progress * 100:.0f}%", True, COLOR_WHITE)
        screen.blit(pct_txt, (bar_x + bar_w + 6, bar_y - 1))

        # 자산 정보
        cash_color = COLOR_POSITIVE if state.player.cash >= 0 else COLOR_NEGATIVE
        items = [
            ("현금", format_money(state.player.cash), cash_color),
            ("부동산", format_money(state.player.total_building_value), COLOR_LIGHT_GRAY),
            ("총자산", format_money(state.player.total_assets), COLOR_WHITE),
        ]
        x_offset = 380
        for label, value, color in items:
            lbl = self.font_small.render(f"{label}: ", True, COLOR_GRAY)
            val = self.font_small.render(value, True, color)
            screen.blit(lbl, (x_offset, 16))
            screen.blit(val, (x_offset + lbl.get_width(), 16))
            x_offset += lbl.get_width() + val.get_width() + 24

    def _draw_map(
        self, screen: pygame.Surface, state: GameState, clickables: dict
    ) -> None:
        for row in state.tiles:
            for tile in row:
                px = MAP_OFFSET_X + tile.x * TILE_SIZE
                py = MAP_OFFSET_Y + tile.y * TILE_SIZE
                color = TERRAIN_COLORS.get(tile.terrain_type, COLOR_LAND)
                rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, COLOR_DARK_GRAY, rect, 1)

                if tile.building:
                    b = tile.building
                    bcolor = CATEGORY_COLORS.get(b.category, COLOR_GRAY)
                    brect = pygame.Rect(px + 3, py + 3, TILE_SIZE - 6, TILE_SIZE - 6)
                    pygame.draw.rect(screen, bcolor, brect, border_radius=3)
                    # 플레이어 소유 테두리
                    if b.owner == "player":
                        pygame.draw.rect(screen, COLOR_PLAYER_BORDER, brect, 2, border_radius=3)
                    # 선택된 건물 하이라이트
                    if state.selected_building and state.selected_building.id == b.id:
                        pygame.draw.rect(screen, COLOR_HIGHLIGHT, brect, 2, border_radius=3)
                    clickables["buildings"].append((brect, b))

    def _draw_bottom_panel(
        self, screen: pygame.Surface, state: GameState, clickables: dict
    ) -> None:
        panel_y = SCREEN_HEIGHT - 48
        panel = pygame.Rect(0, panel_y, SCREEN_WIDTH, 48)
        pygame.draw.rect(screen, COLOR_PANEL, panel)
        pygame.draw.line(
            screen, COLOR_PANEL_BORDER, (0, panel_y), (SCREEN_WIDTH, panel_y)
        )

        # 속도 버튼
        speed_labels = [
            ("일시정지" if not state.is_paused else "재생", "pause"),
            ("1x", 1),
            ("2x", 2),
            ("4x", 4),
        ]
        x = 16
        for label, action in speed_labels:
            btn_w = 80 if action == "pause" else 48
            btn_rect = pygame.Rect(x, panel_y + 8, btn_w, 32)
            mouse_pos = pygame.mouse.get_pos()
            is_active = (
                (action == "pause" and state.is_paused)
                or (isinstance(action, int) and state.time_speed == action and not state.is_paused)
            )
            if is_active:
                color = COLOR_BUTTON
            elif btn_rect.collidepoint(mouse_pos):
                color = COLOR_BUTTON_HOVER
            else:
                color = COLOR_DARK_GRAY
            pygame.draw.rect(screen, color, btn_rect, border_radius=4)
            txt = self.font_small.render(label, True, COLOR_WHITE)
            screen.blit(txt, txt.get_rect(center=btn_rect.center))
            clickables["buttons"].append((btn_rect, action))
            x += btn_w + 8

        # 활성 이벤트 표시
        if state.active_events:
            evt_text = " | ".join(
                f"{e.name} ({e.remaining_months}개월)" for e in state.active_events[:3]
            )
            txt = self.font_tiny.render(f"진행 중: {evt_text}", True, COLOR_HIGHLIGHT)
            screen.blit(txt, (x + 20, panel_y + 16))

    def _draw_building_popup(
        self, screen: pygame.Surface, state: GameState, clickables: dict
    ) -> None:
        b = state.selected_building
        if not b:
            return

        # 팝업 배경
        popup_w, popup_h = 320, 340
        popup_x = SCREEN_WIDTH - popup_w - 16
        popup_y = MAP_OFFSET_Y + 10
        popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)
        pygame.draw.rect(screen, COLOR_PANEL, popup_rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_PANEL_BORDER, popup_rect, 2, border_radius=8)

        y = popup_y + 16
        x = popup_x + 16
        inner_w = popup_w - 32

        # 건물명
        name_txt = self.font_medium.render(b.name, True, COLOR_WHITE)
        screen.blit(name_txt, (x, y))
        y += 36

        # 유형/카테고리
        type_txt = self.font_small.render(
            f"{b.building_type} ({b.category})", True, COLOR_LIGHT_GRAY
        )
        screen.blit(type_txt, (x, y))
        y += 28

        # 구분선
        pygame.draw.line(
            screen, COLOR_PANEL_BORDER, (x, y), (x + inner_w, y)
        )
        y += 12

        # 정보
        info_lines = [
            ("현재 시세", format_money(b.current_price)),
            ("임대 수익률", f"연 {b.rental_yield * 100:.1f}%"),
            ("월 예상 수익", format_money(int(b.current_price * b.rental_yield / 12))),
            ("소유자", {"player": "나", "npc": "NPC", "market": "매물"}.get(b.owner, b.owner)),
        ]
        if b.owner == "player":
            profit = b.current_price - b.purchase_price
            profit_pct = (profit / b.purchase_price * 100) if b.purchase_price else 0
            info_lines.append(("매수가", format_money(b.purchase_price)))
            info_lines.append(("수익률", f"{profit_pct:+.1f}%"))

        for label, value in info_lines:
            lbl = self.font_small.render(f"{label}:", True, COLOR_GRAY)
            val = self.font_small.render(value, True, COLOR_WHITE)
            screen.blit(lbl, (x, y))
            screen.blit(val, (x + 120, y))
            y += 24

        y += 12

        # 매수/매도 버튼
        if b.owner == "market" and b.is_for_sale:
            buyable = can_buy(state, b)
            btn_rect = pygame.Rect(x, y, inner_w, 36)
            color = COLOR_BUTTON if buyable else COLOR_DARK_GRAY
            mouse_pos = pygame.mouse.get_pos()
            if buyable and btn_rect.collidepoint(mouse_pos):
                color = COLOR_BUTTON_HOVER
            pygame.draw.rect(screen, color, btn_rect, border_radius=6)
            cost_text = format_money(b.current_price + int(b.current_price * 0.01))
            txt = self.font_small.render(f"매수 ({cost_text})", True, COLOR_WHITE)
            screen.blit(txt, txt.get_rect(center=btn_rect.center))
            clickables["buttons"].append((btn_rect, ("buy", b)))
        elif b.owner == "player":
            btn_rect = pygame.Rect(x, y, inner_w, 36)
            mouse_pos = pygame.mouse.get_pos()
            color = (
                COLOR_BUTTON_DANGER
                if not btn_rect.collidepoint(mouse_pos)
                else (220, 80, 80)
            )
            pygame.draw.rect(screen, color, btn_rect, border_radius=6)
            proceeds = format_money(b.current_price - int(b.current_price * 0.02))
            txt = self.font_small.render(f"매도 ({proceeds})", True, COLOR_WHITE)
            screen.blit(txt, txt.get_rect(center=btn_rect.center))
            clickables["buttons"].append((btn_rect, ("sell", b)))
        elif b.owner == "npc":
            txt = self.font_small.render("NPC 소유 (매수 불가)", True, COLOR_GRAY)
            screen.blit(txt, (x, y))

    def _draw_event_notification(
        self, screen: pygame.Surface, state: GameState
    ) -> None:
        if not state.event_notification:
            return
        alpha = min(255, int(state.event_notification_timer * 255 / 2))
        surf = pygame.Surface((SCREEN_WIDTH - 40, 40), pygame.SRCALPHA)
        surf.fill((40, 40, 80, alpha))
        txt = self.font_small.render(
            f"📰 {state.event_notification}", True, COLOR_HIGHLIGHT
        )
        surf.blit(txt, txt.get_rect(center=(surf.get_width() // 2, 20)))
        screen.blit(surf, (20, MAP_OFFSET_Y + 4))

    # ── 게임 오버 ──────────────────────────────────────────
    def draw_game_over(
        self, screen: pygame.Surface, state: GameState
    ) -> pygame.Rect:
        screen.fill((40, 20, 20))

        title = self.font_large.render("파산!", True, COLOR_NEGATIVE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 200)))

        lines = [
            f"플레이 기간: {state.current_year}년차 {state.current_month_in_year}월",
            f"최종 현금: {format_money(state.player.cash)}",
            f"최종 자산: {format_money(state.player.total_assets)}",
        ]
        for i, line in enumerate(lines):
            txt = self.font_medium.render(line, True, COLOR_LIGHT_GRAY)
            screen.blit(
                txt, txt.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 40))
            )

        btn_rect = pygame.Rect(0, 0, 200, 50)
        btn_rect.center = (SCREEN_WIDTH // 2, 480)
        mouse_pos = pygame.mouse.get_pos()
        color = COLOR_BUTTON_HOVER if btn_rect.collidepoint(mouse_pos) else COLOR_BUTTON
        pygame.draw.rect(screen, color, btn_rect, border_radius=8)
        txt = self.font_medium.render("처음으로", True, COLOR_WHITE)
        screen.blit(txt, txt.get_rect(center=btn_rect.center))

        return btn_rect

    # ── 게임 클리어 ────────────────────────────────────────
    def draw_game_clear(
        self, screen: pygame.Surface, state: GameState
    ) -> pygame.Rect:
        screen.fill((20, 40, 30))

        title = self.font_large.render("30년 완주 성공!", True, COLOR_POSITIVE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 180)))

        lines = [
            f"보유 현금: {format_money(state.player.cash)}",
            f"부동산 가치: {format_money(state.player.total_building_value)}",
            f"총 자산: {format_money(state.player.total_assets)}",
            f"보유 건물: {len(state.player.buildings)}채",
        ]
        for i, line in enumerate(lines):
            txt = self.font_medium.render(line, True, COLOR_WHITE)
            screen.blit(
                txt, txt.get_rect(center=(SCREEN_WIDTH // 2, 280 + i * 40))
            )

        btn_rect = pygame.Rect(0, 0, 200, 50)
        btn_rect.center = (SCREEN_WIDTH // 2, 500)
        mouse_pos = pygame.mouse.get_pos()
        color = COLOR_BUTTON_HOVER if btn_rect.collidepoint(mouse_pos) else COLOR_BUTTON
        pygame.draw.rect(screen, color, btn_rect, border_radius=8)
        txt = self.font_medium.render("처음으로", True, COLOR_WHITE)
        screen.blit(txt, txt.get_rect(center=btn_rect.center))

        return btn_rect
