import pygame
import math
import os

class Raycaster:
    def __init__(self, screen, render_cfg, player_cfg):
        self.screen = screen
        # 処理を軽くするため、光線の本数を少し減らすかステップを最適化
        self.ray_count = render_cfg['ray_count'] // 2  # 本数を半分に
        self.max_depth = 800 # 射撃場の端まで届けば十分
        self.fov = player_cfg['fov']
        self.screen_w = screen.get_width()
        self.screen_h = screen.get_height()
        self.ray_step_w = self.screen_w / self.ray_count
        self.step_angle = self.fov / self.ray_count
        self.wall_tex = self._load_tex("assets/textures/wall.png")

    def _load_tex(self, path):
        if os.path.exists(path):
            return pygame.image.load(path).convert()
        return None

    def cast(self, player, enemies, bullets):
        # 1. 壁の計算（ステップを大きくして高速化）
        for i in range(self.ray_count):
            angle = player.angle - self.fov / 2 + i * self.step_angle
            sin_a, cos_a = math.sin(angle), math.cos(angle)
            
            # depthのステップを 1 から 5 に増やして計算回数を 1/5 に
            for depth in range(1, self.max_depth, 5):
                tx, ty = player.x + cos_a * depth, player.y + sin_a * depth
                grid_x, grid_y = int(tx / player.map.tile_size), int(ty / player.map.tile_size)
                
                if 0 <= grid_y < len(player.map.grid) and 0 <= grid_x < len(player.map.grid[0]):
                    if player.map.grid[grid_y][grid_x] == 1:
                        depth *= math.cos(player.angle - angle)
                        wall_h = (player.map.tile_size * self.screen_h) / (depth + 0.0001)
                        
                        if self.wall_tex:
                            tex_x = int(tx + ty) % player.map.tile_size
                            sample_x = int(tex_x * self.wall_tex.get_width() / player.map.tile_size)
                            column = self.wall_tex.subsurface(sample_x, 0, 1, self.wall_tex.get_height())
                            column = pygame.transform.scale(column, (int(self.ray_step_w) + 1, int(wall_h)))
                            self.screen.blit(column, (i * self.ray_step_w, self.screen_h/2 - wall_h/2))
                        else:
                            pygame.draw.rect(self.screen, (100, 100, 100), (i * self.ray_step_w, self.screen_h/2 - wall_h/2, self.ray_step_w + 1, wall_h))
                        break

        # 2. エネミー描画（距離でソートして描画負荷を安定させる）
        sorted_enemies = sorted(enemies, key=lambda e: math.sqrt((e.x-player.x)**2 + (e.y-player.y)**2), reverse=True)
        for en in sorted_enemies:
            self._draw_sprite(player, en, (255, 0, 0), 1.0, en.tex)
            
        for b in bullets:
            if b.alive: self._draw_sprite(player, b, (255, 255, 0), 0.2, None)

    def _draw_sprite(self, player, obj, color, size_scale, tex):
        dx, dy = obj.x - player.x, obj.y - player.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 10 or dist > 1000: return # 遠すぎるスプライトは描画しない
        
        theta = math.atan2(dy, dx) - player.angle
        while theta > math.pi: theta -= 2 * math.pi
        while theta < -math.pi: theta += 2 * math.pi

        if abs(theta) < self.fov:
            base_size = (player.map.tile_size * self.screen_h) / (dist + 0.0001)
            screen_x = (theta / self.fov + 0.5) * self.screen_w
            
            if tex:
                aspect = tex.get_width() / tex.get_height()
                draw_h = base_size * size_scale
                draw_w = draw_h * aspect
                img = pygame.transform.scale(tex, (int(draw_w), int(draw_h)))
                self.screen.blit(img, (screen_x - draw_w/2, self.screen_h/2 + base_size/2 - draw_h))
            else:
                pygame.draw.rect(self.screen, color, (screen_x - base_size/4, self.screen_h/2 - base_size/2, base_size/2, base_size))
