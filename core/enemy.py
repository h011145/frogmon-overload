import math
import pygame
import os

class Enemy:
    def __init__(self, x, y, speed=2.0):
        self.x = x
        self.y = y
        self.start_x = x
        self.alive = True
        self.move_range = 150
        self.direction = 1
        self.speed = speed
        
        # 立ち絵だけ読み込む
        self.tex = self._load_tex("assets/sprites/enemy.png")

    def _load_tex(self, path):
        if os.path.exists(path):
            img = pygame.image.load(path).convert()
            colorkey = img.get_at((0,0))
            img.set_colorkey(colorkey, pygame.RLEACCEL)
            return img
        return None

    def die(self):
        """撃たれたら即座に存在を消すためのフラグ"""
        self.alive = False

    def update(self, player):
        if not self.alive: return
        self.x += self.direction * self.speed
        if abs(self.x - self.start_x) > self.move_range:
            self.direction *= -1
