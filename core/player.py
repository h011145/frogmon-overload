import pygame
import math

class Player:
    def __init__(self, cfg, game_map):
        self.x, self.y = cfg['start_pos']
        self.angle = 0
        self.speed = cfg['speed']
        self.sensitivity = cfg['mouse_sensitivity']
        self.map = game_map

    def update(self):
        # マウス旋回
        rel_x, _ = pygame.mouse.get_rel()
        self.angle += rel_x * self.sensitivity
        
        # キー移動
        keys = pygame.key.get_pressed()
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        
        if keys[pygame.K_w]: self.move(dx, dy)
        if keys[pygame.K_s]: self.move(-dx, -dy)

    def move(self, dx, dy):
        # 衝突判定（Mapクラスを参照）
        nx = int((self.x + dx * 2) / self.map.tile_size)
        ny = int((self.y + dy * 2) / self.map.tile_size)
        if self.map.grid[int(self.y/self.map.tile_size)][nx] == 0:
            self.x += dx
        if self.map.grid[ny][int(self.x/self.map.tile_size)] == 0:
            self.y += dy
