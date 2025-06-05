import pygame

from utils.settings import Settings


class GameOverState:
    """Tela de Game Over"""

    def __init__(self, game, win=False):
        self.game = game
        self.config = Settings()
        self.win = win
        self.font_1 = pygame.font.Font("fonts/conthrax-sb.otf", 50)
        self.font_2 = pygame.font.Font("fonts/conthrax-sb.otf", 22)
        self.text_rect = None

        # Configurações do texto
        if self.win:
            self.text = self.font_1.render("Parabéns! Você venceu!", True, (0, 255, 0), )
        else:
            self.text = self.font_1.render("GAME OVER", True, (255, 0, 0))
            self.text_render = self.text.get_rect()
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.config.SCREEN['width'] // 2, (self.config.SCREEN['height'] // 2) - 80)

        # Configurações das instruções
        self.instruction = self.font_2.render("Pressione ENTER para voltar ao Menu", True, (255, 255, 255))
        self.inst_rect = self.instruction.get_rect()
        self.inst_rect.center = (self.config.SCREEN['width'] // 2, (self.config.SCREEN['height'] // 2) + 80)

    def handle_events(self):
        """Captura eventos do usuário"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                from core.menu_state import MenuState # Importação tardia para evitar problemas
                self.game.state_manager.set_state(MenuState(self.game)) # Retorna ao menu

    def update(self):
        pass # Nada para atualizar

    def render(self, screen):
        """Renderiza a tela de Game Over"""
        screen.fill((0, 0, 0))
        if self.text_rect:
            screen.blit(self.text, self.text_rect)
        screen.blit(self.instruction, self.inst_rect)
