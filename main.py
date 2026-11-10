import sys
import pygame

from config.const import (
    GAME_TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from config.levels import LEVELS

from modules.Menu import Menu
from modules.Game import Game
from modules.Victory import Victory

class Main():
    @staticmethod
    def run_game():
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        while True:
            # menu inicial
            menu_result = Menu(screen).run()
            if menu_result == 'quit':
                break

            players_count = 1 if menu_result == '1p' else 2
            print(f"""[INFO] Modo de {"1 Jogador" if players_count == 1 else "2 Jogadores"}""")

            if Main.play_levels(screen, players_count) == 'quit':
                break

        pygame.quit()
        sys.exit()

    @staticmethod
    def play_levels(screen, players_count: int) -> str:
        """Joga os níveis em sequência. Retorna 'menu' ou 'quit'."""
        current_level = 1
        while True:
            level_result = Game(level=current_level, players_count=players_count).run(screen=screen)

            if level_result is True:
                current_level += 1
                print(f"[INFO] Vitória! Indo para o nível {current_level}")

                if current_level not in LEVELS:
                    print("[INFO] Todos os níveis completados! Mostrando tela de vitória...")
                    Victory(players_count).run(screen)
                    return 'menu'

            elif level_result is False:
                print("[INFO] Game Over! Voltando ao menu...")
                return 'menu'

            else:
                # 'menu' (ESC) ou None (fechou a janela)
                return 'menu' if level_result == 'menu' else 'quit'

if __name__ == "__main__":
    Main.run_game()
