import sys
import pygame

from config.const import (
    GAME_TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from config.levels import LEVELS

from modules.Menu import Menu
from modules.Field import Field

class Main():
    def __init__(self):
        pass

    @staticmethod
    def run_game():
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        # menu inicial
        menu = Menu(screen)
        menu_result = menu.run()

        if menu_result == 'quit':
            pygame.quit()
            sys.exit()

        players_count = 1 if menu_result == '1p' else 2
        current_level = 1

        print(f"""[INFO] Modo de {"1 Jogador" if players_count == 1 else "2 Jogadores"}""")

        # failsafe screen
        game_running = True
        while game_running:
            field = Field(level=current_level)
            level_result  = field.run(screen=screen)

            if level_result:
                current_level += 1

            if current_level not in LEVELS:
                print("[INFO] Acabaram os levels")
                game_running = False

            else:
                print("[INFO] Game Over")
                game_running = False

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Main.run_game()