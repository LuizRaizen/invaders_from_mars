import time

from utils.settings import Settings
from entities.ships import Ship, DoubleShootShip


class PowerUpManager:
    """Gerencia os power-ups ativos e seus tempos de duração"""

    def __init__(self, game):
        self.game = game
        self.config = Settings()
        self.active_powerups = {}  # Armazena os power-ups ativos e seus tempos

    def activate_powerup(self, powerup_type, duration=10):
        """Ativa um power-up e define seu tempo de expiração"""
        self.active_powerups[powerup_type] = time.time() + duration  # Marca o tempo de expiração

        if powerup_type == "speed":
            self.game.ship.speed_boost_active = True  # Ativa o boost de velocidade
            self.game.ship.acceleration = 0.5  # Aceleração mais rápida ao pressionar as teclas
            self.game.ship.speed += 3  # Impulso inicial
        elif powerup_type == "shield":
            self.game.ship.activate_shield()
        elif powerup_type == "double_shoot":
            self.game.ship.activate_double_shoot()
            
    def get_remaining_time(self, powerup_type):
        """Retorna o tempo restante de um power-up ativo"""
        if powerup_type in self.active_powerups:
            return max(0, int(self.active_powerups[powerup_type] - time.time()))  # Retorna tempo em segundos
        return 0

    def update(self):
        """Verifica se algum power-up expirou e remove seus efeitos"""
        current_time = time.time()
        expired_powerups = [p for p, end_time in self.active_powerups.items() if current_time >= end_time]

        for powerup in expired_powerups:
            if powerup == "speed":
                self.game.ship.speed_boost_active = False
                self.game.ship.acceleration = 0.2  # Retorna à aceleração normal
                self.game.ship.speed -= 3  # Reduz velocidade de volta ao normal
            elif powerup == "shield":
                self.game.ship.deactivate_shield()
            elif powerup == "double_shoot":
                xpos = self.game.ship.rect.centerx
                self.game.ship = Ship(self.game, xpos)

            del self.active_powerups[powerup]  # Remove o power-up expirado
    