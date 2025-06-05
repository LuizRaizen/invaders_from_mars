import pygame
from utils.settings import Settings
from utils.audio_manager import audio_manager
from core.playing_state import PlayingState
from entities.buttons import MenuButton


class Baseboard:
    def __init__(self, game, x, y):
        self.game = game
        self.config = Settings()
        self.color = (180, 180, 255)
        self.font = pygame.font.Font(*self.config.BASEBOARD['font'])
        self.text = self.font.render(self.config.BASEBOARD['text'], True, self.color)
        self.rect = self.text.get_rect()
        self.rect.centerx, self.rect.bottom = (x, y)

    def render(self, screen):
        screen.blit(self.text, self.rect)


class MenuState:
    def __init__(self, game):
        self.game = game
        self.config = Settings()

        self.font = pygame.font.Font("fonts/conthrax-sb.otf", 28)

        # Fundo e logo
        self.background = pygame.image.load('graphics/backgrounds/title_menu_bg.jpg')
        self.logo = pygame.image.load('graphics/images/logo.png')
        self.logo_rect = self.logo.get_rect(center=(self.config.SCREEN['width'] // 2, self.config.SCREEN['height'] // 4))

        # Rodapé
        self.baseboard = Baseboard(game, self.config.SCREEN['width'] // 2, self.config.SCREEN['height'] - 20)

        # Música
        audio_manager.play_music('title_bg')

        # Botões
        center_x = self.config.SCREEN['width'] // 2
        self.buttons = [
            MenuButton((center_x, 300), (250, 50), self.font, "JOGAR", self.start_game),
            MenuButton((center_x, 380), (250, 50), self.font, "OPÇÕES", self.go_to_options),
            MenuButton((center_x, 460), (250, 50), self.font, "SAIR", self.quit_game),
        ]

    def start_game(self):
        self.game.state_manager.set_state(PlayingState(self.game))

    def go_to_options(self):
        print("Abrir tela de opções (ainda não implementada)")
        # self.game.state_manager.set_state(OptionsState(self.game))

    def quit_game(self):
        self.game.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    button.handle_click()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, self.logo_rect)
        self.baseboard.render(screen)
        for button in self.buttons:
            button.draw(screen)
