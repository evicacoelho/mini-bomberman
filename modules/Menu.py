import os
import pygame

from typing import Optional

from config.const import (
    GAME_TITLE,
    PATH_ASSETS,
    PATH_BACKGROUNDS, 
    TICK_VALUE,
    WINDOW_HEIGHT, 
    WINDOW_WIDTH,
)

class Menu():
    def __init__(
            self, 
            screen,
        ):
        # params
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_options = pygame.font.SysFont('Arial', 36)
        self.selected_option = 0
        self.options = ["Jogar 1P", "Jogar 2P", "Sair do Jogo"]

        # colors
        self.color_title = "#FF9988"
        self.color_option = "#FFFF00"
        self.color_selected = "#FFFFFF"
        self.color_background = "#000000"

        # positions
        self.title_y = 100
        self.option_start_y = 250
        self.option_spacing = 70

        # background image
        self.image_background = pygame.image.load(os.path.join(PATH_BACKGROUNDS, 'menu.png')).convert_alpha()
        self.image_background = pygame.transform.scale(self.image_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # background music
        pygame.mixer.music.load(os.path.join(PATH_BACKGROUNDS, 'menu.mp3'))
        pygame.mixer.music.play(-1)

    def draw(
        self
    ):
        if self.image_background:
            self.screen.blit(self.image_background, (0,0))

            title_surface = self.font_title.render(GAME_TITLE, True, self.color_title)
            title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, self.title_y))
            
            self.screen.blit(title_surface, title_rect)
        
        else: 
            self.screen.fill(self.color_background)

            title_surface = self.font_title.render(GAME_TITLE, True, self.color_title)
            title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, self.title_y))
            
            self.screen.blit(title_surface, title_rect)

        # menu & menu colors
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = self.color_selected
                indicator = self.font_options.render(">", True, color)
                indicator_rect = indicator.get_rect(
                    midright=(WINDOW_WIDTH // 2 - 150, self.option_start_y + i * self.option_spacing)
                )
                self.screen.blit(indicator, indicator_rect)
            
            else: color = self.color_option

            option_surface = self.font_options.render(option, True, color)

            option_rect = option_surface.get_rect(
                center=(WINDOW_WIDTH // 2, self.option_start_y + i * self.option_spacing)
            )

            self.screen.blit(option_surface, option_rect)

    def event_handler(
        self,
    ) -> Optional[str]:
        for event in pygame.event.get():
            # finalização de tarefa
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                
                # navegação direcional
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_option = (self.selected_option + 1) % len(self.options)

                # seleção
                if event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        return '1p'
                    if self.selected_option == 1:
                        return '2p'
                    if self.selected_option == 2:
                        return 'quit'
        
        return None


    def run(
        self
    ) -> str:
        while True:
            

            # event handling
            result = self.event_handler()
            if result: return result

            # visual rendering
            self.draw()

            # game anatomy
            pygame.display.flip()
            self.clock.tick(TICK_VALUE)
