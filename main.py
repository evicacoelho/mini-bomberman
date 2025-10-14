import sys
import pygame

from config.const import (
    GAME_TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)

from modules.Menu import Menu

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

        if menu_result == '1p':
            pass
        elif menu_result == '2p':
            pass
        elif menu_result == 'quit':
            pygame.quit()
            sys.exit()


        # failsafe screen
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
            
            screen.fill('#FFFFFF')

            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Main.run_game()