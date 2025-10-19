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

        game_running = True
        while game_running:
            field = Game(level=current_level, players_count=players_count)
            level_result = field.run(screen=screen)

            if level_result is True:
                # victory
                current_level += 1
                print(f"[INFO] Vitória! Indo para o nível {current_level}")
                
                # game win
                if current_level not in LEVELS:
                    print("[INFO] Todos os níveis completados! Mostrando tela de vitória...")
                    
                    victory_screen = Victory(players_count)
                    should_return_to_menu = victory_screen.run(screen)
                    
                    if should_return_to_menu:
                        return Main.run_game()  
                    
            elif level_result is False:
                # game over
                print("[INFO] Game Over! Reiniciando nível...")
                
            else:
                # quit
                game_running = False

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Main.run_game()