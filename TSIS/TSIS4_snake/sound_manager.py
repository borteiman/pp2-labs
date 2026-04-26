import pygame
from config import ASSETS_DIR


class SoundManager:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.sounds = {}

        try:
            self.sounds["eat"] = pygame.mixer.Sound(str(ASSETS_DIR / "eat.wav"))
            self.sounds["power"] = pygame.mixer.Sound(str(ASSETS_DIR / "power.wav"))
            self.sounds["crash"] = pygame.mixer.Sound(str(ASSETS_DIR / "crash.wav"))
        except pygame.error:
            self.sounds = {}

    def set_enabled(self, enabled):
        self.enabled = enabled

    def play(self, name):
        if not self.enabled:
            return
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()
