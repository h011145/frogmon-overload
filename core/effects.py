import pygame
import random
import math

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 255  # 透明度（時間とともに減る）
        self.color = (255, random.randint(150, 255), 0) # オレンジ〜黄色

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 15 # 素早く消える
        return self.life > 0

    def draw(self, screen):
        # 光り輝く火花を描画
        size = random.randint(2, 4)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
