import pygame

from core.state_manager import StateManager
from core.menu_state import MenuState
from utils.settings import Settings
from utils.powerup_manager import PowerUpManager
from utils.audio_manager import audio_manager


class Game:
    
    def __init__(self):
        pygame.init()
        self.config = Settings() # Configurações do jogo
        self.screen = pygame.display.set_mode((self.config.SCREEN['width'], self.config.SCREEN['height']))
        pygame.display.set_icon(pygame.image.load('graphics/images/icon.png'))
        pygame.display.set_caption("Invasão Alienigena")

        self.clock = pygame.time.Clock()
        self.running = True  # Atributo que garante que o jogo esteja em execução
        self.paused = False  # Atributo para controlar o estado de pausa
        self.powerup_manager = PowerUpManager(self)  # Inicializa o gerenciador de power-ups
        self.powerup_freeze = False  # Paralisação temporária ao pegar power-up
        self.powerup_freeze_end_time = 0  # Controla o tempo de paralisação

        # Gerenciador de estados
        self.state_manager = StateManager()
        self.state_manager.set_state(MenuState(self))

    def toggle_pause(self):
        """Alterna entre pausar e retomar o jogo"""
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        if not self.powerup_freeze:  # Só permite pausar se não houver paralização de power-up ativa
            self.paused = not self.paused

    def update_powerup_freeze(self):
        """Verifica se o tempo de paralisação do power-up acabou e libera o jogo"""
        if self.powerup_freeze and pygame.time.get_ticks() >= self.powerup_freeze_end_time:
            self.powerup_freeze = False  # Libera o jogo para continuar
            self.powerup_manager.activate_powerup(self.active_powerup.type)  # Agora ativa o efeito
            self.active_powerup = None  # Remove o power-up ativo

    def run(self):
        """Loop principal do jogo."""
        while self.running:
            self.state_manager.handle_events()
            self.state_manager.update()
            self.state_manager.render(self.screen)
            pygame.display.flip()
            self.clock.tick(self.config.SCREEN['fps'])

        pygame.quit()

        
if __name__ == '__main__':
    game = Game()
    game.run()
