import pygame
import numpy as np
import os

class Weapon:
    def __init__(self, config):
        self.path = "assets/sprites/machinegun.png"
        self.last_shot = 0
        self.recoil = 0
        self.tex = self._load_tex()
        # ここでは mixer.init() しない（Engine側に任せる）
        self.shoot_sound = self._create_synth_sound()

    def _create_synth_sound(self):
        duration = 0.05 
        frequency = 22050
        n_samples = int(duration * frequency)
        buf = np.random.randint(-16384, 16384, n_samples, dtype=np.int16)
        decay = np.exp(-np.linspace(0, 5, n_samples))
        buf = (buf * decay).astype(np.int16)
        buf_stereo = np.vstack((buf, buf)).T.copy(order='C')
        return pygame.sndarray.make_sound(buf_stereo)

    def _load_tex(self):
        if os.path.exists(self.path):
            try:
                img = pygame.image.load(self.path).convert_alpha()
                return pygame.transform.scale(img, (500, 500))
            except: return None
        return None

    def trigger(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 100:
            self.last_shot = now
            self.recoil = 20
            if self.shoot_sound:
                self.shoot_sound.play()
            return True
        return False

    def update(self):
        if self.recoil > 0:
            self.recoil -= 4

    def draw(self, screen):
        w, h = screen.get_size()
        if self.tex:
            pos_x = w // 2 - self.tex.get_width() // 2
            pos_y = h - self.tex.get_height() + self.recoil + 15
            screen.blit(self.tex, (pos_x, pos_y))
        else:
            pygame.draw.rect(screen, (50, 50, 50), (w//2-30, h-120+self.recoil, 60, 120))
