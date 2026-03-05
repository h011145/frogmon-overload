import pygame, math, random
from core.player import Player
from core.raycaster import Raycaster
from core.map import Map
from core.weapon import Weapon
from core.enemy import Enemy
from core.effects import Particle # 追加

class Bullet:
    def __init__(self, x, y, angle):
        self.x, self.y = x, y
        self.angle = angle
        self.speed = 25
        self.alive = True

    def update(self, game_map):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        gx, gy = int(self.x / game_map.tile_size), int(self.y / game_map.tile_size)
        if 0 <= gy < len(game_map.grid) and 0 <= gx < len(game_map.grid[0]):
            if game_map.grid[gy][gx] == 1: self.alive = False
        else: self.alive = False

class GameEngine:
    def __init__(self, config):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((config['window']['width'], config['window']['height']))
        self.map = Map()
        self.player = Player(config['player'], self.map)
        self.player.x, self.player.y, self.player.angle = 500, 750, -math.pi/2
        self.renderer = Raycaster(self.screen, config['render'], config['player'])
        self.weapon = Weapon(config)
        self.enemies = []
        self.bullets = []
        self.particles = [] # エフェクトリスト
        self.score = 0
        self.current_speed = 2.0
        self.game_clear = False
        self.start_bgm()
        self.spawn_enemy() 
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)

    def start_bgm(self):
        try:
            pygame.mixer.music.load("assets/sounds/bgm.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except: pass

    def spawn_enemy(self):
        if self.score < 10:
            self.enemies = [Enemy(random.randint(200, 800), 300, self.current_speed)]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                if event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    if self.score >= 10: 
                        self.game_clear = True
                        pygame.mixer.music.fadeout(2000)
                    else: self.spawn_enemy()
            
            if not self.game_clear:
                if pygame.mouse.get_pressed()[0] and self.weapon.trigger():
                    self.bullets.append(Bullet(self.player.x, self.player.y, self.player.angle))
                
                self.player.update()
                self.weapon.update()
                for en in self.enemies: en.update(self.player)
                
                # エフェクトの更新
                self.particles = [p for p in self.particles if p.update()]
                
                for b in self.bullets[:]:
                    b.update(self.map)
                    if not b.alive:
                        if b in self.bullets: self.bullets.remove(b)
                        continue
                    for en in self.enemies[:]:
                        if en.alive and math.sqrt((b.x - en.x)**2 + (b.y - en.y)**2) < 45:
                            # 撃破時に火花を20個生成！
                            # 3D空間の座標から画面上の座標(400, 225付近)に火花を散らす
                            for _ in range(20):
                                self.particles.append(Particle(400 + random.randint(-50, 50), 225 + random.randint(-50, 50)))
                            en.die()
                            self.enemies.remove(en)
                            self.score += 1
                            self.current_speed += 1.5
                            pygame.time.set_timer(pygame.USEREVENT, 300)

            self.screen.fill((20, 20, 40)) 
            pygame.draw.rect(self.screen, (30, 30, 30), (0, 225, 800, 225))
            self.renderer.cast(self.player, self.enemies, self.bullets)
            
            # 火花の描画
            for p in self.particles: p.draw(self.screen)
            
            self.weapon.draw(self.screen)
            self.screen.blit(self.font.render(f"SCORE: {self.score} / 10", True, (255, 255, 255)), (20, 20))
            if self.game_clear:
                txt = self.font.render("MISSION CLEAR!", True, (0, 255, 0))
                self.screen.blit(txt, txt.get_rect(center=(400, 225)))

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
