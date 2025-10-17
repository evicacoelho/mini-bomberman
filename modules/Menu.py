import os
import pygame

from typing import Optional

from config.const import (
    GAME_TITLE,
    PATH_BACKGROUNDS,
    PATH_SOUNDS, 
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
        self.font_title = pygame.font.SysFont('Lato', 60, bold=True)
        self.font_options = pygame.font.SysFont('Arial', 36)
        self.selected_option = 0
        self.options = ["1 Player", "2 Players", "Controls", "Quit Game"]

        # colors
        self.color_title = "#FF4322"
        self.color_option = "#FFFFFF"
        self.color_selected = "#FFFF00"
        self.color_background = "#000000"

        # positions
        self.title_y = 100
        self.option_start_y = 250
        self.option_spacing = 50

        # background image
        self.image_background = False
        #self.image_background = pygame.image.load(os.path.join(PATH_BACKGROUNDS, 'menu.png')).convert_alpha()
        #self.image_background = pygame.transform.scale(self.image_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # background music
        pygame.mixer.music.load(os.path.join(PATH_SOUNDS, 'menu.mp3'))
        pygame.mixer.music.play(-1)

        # menu sounds
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        try:
            self.sounds['cursor'] = pygame.mixer.Sound(os.path.join(PATH_SOUNDS, 'title_screen_cursor.wav'))
            self.sounds['select'] = pygame.mixer.Sound(os.path.join(PATH_SOUNDS, 'title_screen_select.wav'))
        except Exception as e:
            print(f"[ERRO] Não foi possível carregar os sons do menu: {e}")

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
                    self.sounds['cursor'].play()
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.sounds['cursor'].play()
                    self.selected_option = (self.selected_option + 1) % len(self.options)

                # seleção
                if event.key == pygame.K_RETURN:
                    self.sounds['select'].play()
                    if self.selected_option == 0:
                        return '1p'
                    if self.selected_option == 1:
                        return '2p'
                    if self.selected_option == 2:
                        return 'controls'
                    if self.selected_option == 3:
                        return 'quit'
        
        return None
    
    def draw_controls_screen(self):
        try:
            controls_bg = pygame.image.load(os.path.join(PATH_BACKGROUNDS, 'controls-background.png')).convert()
            controls_bg = pygame.transform.scale(controls_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.screen.blit(controls_bg, (0, 0))
        except:
            self.screen.fill(self.color_background)
    
            instruction_font = pygame.font.SysFont('Arial', 24)
            instruction_text = "Image not found: controls-background.png"
            instruction_surface = instruction_font.render(instruction_text, True, "#FFFFFF")
            instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(instruction_surface, instruction_rect)    
        
        instruction_font = pygame.font.SysFont('Arial', 20)
        instruction_text = "Press ENTER to return to main menu"
        instruction_surface = instruction_font.render(instruction_text, True, "#FFFFFF")
        instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        self.screen.blit(instruction_surface, instruction_rect)

    def run_controls_screen(self) -> str:
        self.sounds['select'].play()  
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                    
                    # ENTER ou qualquer tecla para voltar (conforme solicitado)
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.sounds['select'].play()  # Toca som ao voltar
                        return "back"
            
            # Renderiza a tela de controles
            self.draw_controls_screen()
            
            # Atualiza a tela
            pygame.display.flip()
            self.clock.tick(TICK_VALUE)
        
        return "back"


    def run(
        self
    ) -> str:
        while True:
            # event handling
            result = self.event_handler()
            if result == 'controls':
                controls_result = self.run_controls_screen()
                if controls_result == 'quit':
                    return 'quit'
                continue
            
            elif result: 
                pygame.mixer.music.stop()
                return result

            # visual rendering
            self.draw()

            # game anatomy
            pygame.display.flip()
            self.clock.tick(TICK_VALUE)
