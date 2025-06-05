import pygame

class AudioManager:
    """Classe para gerenciar os efeitos sonoros e músicas do jogo."""
    
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.musics = {}
        self.current_music = None  # Guarda a música atualmente tocando

    def load_sound(self, sound_name, path):
        """Carrega um efeito sonoro."""
        self.sounds[sound_name] = pygame.mixer.Sound(path)
    
    def play_sound(self, sound_name):
        """Toca um efeito sonoro carregado."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def load_music(self, music_name, path):
        """Carrega uma música de fundo."""
        self.musics[music_name] = path

    def play_music(self, music_name, loop=True):
        """Reproduz uma música de fundo sem reiniciar se já estiver tocando."""
        if music_name in self.musics:
            # Se já estiver tocando a mesma música, não reiniciar
            if self.current_music == music_name and pygame.mixer.music.get_busy():
                return  

            # Para qualquer música anterior antes de iniciar uma nova
            pygame.mixer.music.stop()  
            pygame.mixer.music.load(self.musics[music_name])
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music = music_name  # Atualiza a música atual

    def stop_music(self):
        """Para qualquer música de fundo que esteja tocando."""
        pygame.mixer.music.stop()
        self.current_music = None  # Reseta a música atual


# Instância global de gerenciamento de áudio
audio_manager = AudioManager()

# Carregar sons essenciais
audio_manager.load_sound("button_hover", "sounds/effects/Select #2.mp3")
audio_manager.load_sound("button_click", "sounds/effects/Choose #4.mp3")
audio_manager.load_sound("explosion", "sounds/effects/Down #5.mp3")
audio_manager.load_sound("shoot", "sounds/effects/Shoot #2.mp3")
audio_manager.load_sound("level_up", "sounds/effects/LevelUp #1.mp3")
audio_manager.load_sound("power_up", "sounds/effects/PowerUp #2.wav")
audio_manager.load_sound("game_over", "sounds/effects/LevelUp #1.mp3")

# Carregar trilha sonora do jogo
audio_manager.load_music("title_bg", "sounds/bgm/title.mp3")  # Alterado para MP3
audio_manager.load_music("gameplay_bg", "sounds/bgm/gameplay.mp3")  # Alterado para MP3
        