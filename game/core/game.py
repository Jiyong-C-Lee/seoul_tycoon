"""메인 게임 클래스 - 게임 루프, 상태 관리"""
import pygame

from game.core.constants import (
    FPS,
    INITIAL_CASH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SECONDS_PER_MONTH,
    TITLE,
    TOTAL_MONTHS,
)
from game.data.models import GameState, Player
from game.systems.economy import (
    buy_building,
    check_bankruptcy,
    process_monthly_settlement,
    sell_building,
    update_prices,
)
from game.systems.event_system import check_and_trigger_event, update_active_events
from game.ui.renderer import Renderer
from game.utils.helpers import generate_map, place_buildings


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.renderer = Renderer()
        self.state = GameState()
        self.running = True

        # 클릭 가능 영역 (매 프레임 갱신)
        self.clickables: dict[str, list] = {"buildings": [], "buttons": []}
        self.menu_start_btn: pygame.Rect | None = None
        self.end_btn: pygame.Rect | None = None

    def init_new_game(self) -> None:
        """새 게임 초기화"""
        tiles = generate_map()
        buildings = place_buildings(tiles)
        self.state = GameState(
            state="playing",
            player=Player(cash=INITIAL_CASH),
            tiles=tiles,
            buildings=buildings,
        )

    def run(self) -> None:
        """메인 게임 루프"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                self._handle_key(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)

    def _handle_key(self, key: int) -> None:
        if self.state.state != "playing":
            return

        if key == pygame.K_SPACE:
            self.state.is_paused = not self.state.is_paused
        elif key == pygame.K_1:
            self.state.is_paused = False
            self.state.time_speed = 1
        elif key == pygame.K_2:
            self.state.is_paused = False
            self.state.time_speed = 2
        elif key == pygame.K_4:
            self.state.is_paused = False
            self.state.time_speed = 4
        elif key == pygame.K_ESCAPE:
            self.state.selected_building = None

    def _handle_click(self, pos: tuple[int, int]) -> None:
        if self.state.state == "menu":
            if self.menu_start_btn and self.menu_start_btn.collidepoint(pos):
                self.init_new_game()
            return

        if self.state.state in ("game_over", "game_clear"):
            if self.end_btn and self.end_btn.collidepoint(pos):
                self.state = GameState()  # 메뉴로 복귀
            return

        if self.state.state == "playing":
            # 버튼 체크 (우선)
            for btn_rect, action in self.clickables.get("buttons", []):
                if btn_rect.collidepoint(pos):
                    self._handle_button(action)
                    return

            # 건물 클릭 체크
            for brect, building in self.clickables.get("buildings", []):
                if brect.collidepoint(pos):
                    self.state.selected_building = building
                    return

            # 빈 곳 클릭 → 선택 해제
            self.state.selected_building = None

    def _handle_button(self, action) -> None:
        if action == "pause":
            self.state.is_paused = not self.state.is_paused
        elif isinstance(action, int):
            self.state.is_paused = False
            self.state.time_speed = action
        elif isinstance(action, tuple):
            cmd, building = action
            if cmd == "buy":
                if buy_building(self.state, building):
                    self.state.selected_building = building
            elif cmd == "sell":
                if sell_building(self.state, building):
                    self.state.selected_building = None

    def _update(self, dt: float) -> None:
        if self.state.state != "playing":
            return

        # 이벤트 알림 타이머 감소
        if self.state.event_notification_timer > 0:
            self.state.event_notification_timer -= dt

        if self.state.is_paused:
            return

        # 시간 경과
        month_duration = SECONDS_PER_MONTH / self.state.time_speed
        self.state.elapsed_time += dt
        if self.state.elapsed_time >= month_duration:
            self.state.elapsed_time -= month_duration
            self._advance_month()

    def _advance_month(self) -> None:
        """월 전환 처리"""
        self.state.current_month += 1

        # 1. 정산
        process_monthly_settlement(self.state)

        # 2. 시세 변동
        update_prices(self.state)

        # 3. 이벤트
        event = check_and_trigger_event(self.state)
        if event:
            self.state.event_notification = f"{event.name}: {event.description}"
            self.state.event_notification_timer = 4.0
        update_active_events(self.state)

        # 4. 파산 체크
        if check_bankruptcy(self.state):
            self.state.state = "game_over"
            return

        # 5. 클리어 체크
        if self.state.current_month >= TOTAL_MONTHS:
            self.state.state = "game_clear"

    def _draw(self) -> None:
        if self.state.state == "menu":
            self.menu_start_btn = self.renderer.draw_menu(self.screen, self.state)
        elif self.state.state == "playing":
            self.clickables = self.renderer.draw_playing(self.screen, self.state)
        elif self.state.state == "game_over":
            self.end_btn = self.renderer.draw_game_over(self.screen, self.state)
        elif self.state.state == "game_clear":
            self.end_btn = self.renderer.draw_game_clear(self.screen, self.state)
