"""Módulo que contém a classe para administrar os estados do jogo."""

class StateManager:
    """Gerencia os estados do jogo."""

    def __init__(self):
        self.state = None # Estado incial do jogo

    def set_state(self, new_state):
        """Define o estado atual"""
        self.state = new_state

    def handle_events(self):
        """Lida com evento do usuário"""
        if self.state:
            self.state.handle_events()

    def update(self):
        """Atualiza o estado do jogo"""
        if self.state:
            self.state.update()

    def render(self, screen):
        """Renderiza o estado atual na tela"""
        if self.state:
            self.state.render(screen)
            