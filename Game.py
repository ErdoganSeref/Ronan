import pygame
import random
from opensimplex import OpenSimplex
from Settings import *
from Object import Object
from Enemy import Enemy
from Player import Player
from Arrow import Arrow
from Camera import Camera
class Game:
    
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.camera = Camera
        self.running = True
        self.player = Player(PLAYER_PNG, random.randint(0,WINDOW_WIDTH), random.randint(0,WINDOW_HEIGHT), PLAYER_ORIENTATION, PLAYER_HP, PLAYER_SPEED, PLAYER_RELOAD_TIME, PLAYER_FIRE_RATE, PLAYER_AMMUNITION_CAPACITY)
        self.arrows = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group()
        self.allSprites.add(self.player)
        self.SPAWN_ENEMY = pygame.USEREVENT

        #tmp = OpenSimplex(seed=SEED)
        #self.map = [[ tmp.noise2d(x,y) for x in range(WINDOW_WIDTH//TILE_WIDTH) ] for y in range(WINDOW_HEIGHT//TILE_HEIGHT) ]
         
    def start(self):
        pygame.init()
        pygame.mixer.get_init()
        pygame.time.set_timer(self.SPAWN_ENEMY, int(1/ENEMY_SPAWNRATE))
        SHOOT_SOUND = pygame.mixer.Sound(SHOOT_OGG)
        RELOAD_SOUND = pygame.mixer.Sound(RELOAD_WAV)
        while self.running:
            self.window.fill((255,255,255))
            self.handleCollisions()
            
            self.arrows.update(self.window, self.camera)

            self.enemies.update(self.window, self.camera, self.player)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.SPAWN_ENEMY:
                    self.spawnEnemy()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.player.direction.x = -1
            if keys[pygame.K_RIGHT]:
                self.player.direction.x = 1
            if keys[pygame.K_UP]:
                self.player.direction.y = -1
            if keys[pygame.K_DOWN]:
                self.player.direction.y = 1
            if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                self.player.direction.x = 0
            if keys[pygame.K_DOWN] and keys[pygame.K_UP]:
                self.player.direction.y = 0

            if keys[pygame.K_SPACE] and self.player.ammunition > 0 and not self.player.reloading and pygame.time.get_ticks() - self.player.lastShot > int(1/self.player.fireRate):
                self.player.lastShot = pygame.time.get_ticks()
                self.player.ammunition -= 1
                xDirection = 0
                x = 0
                if self.player.orientation == -1:
                    xDirection = -1
                    x = self.player.rect.x
                elif self.player.orientation == 1:
                    xDirection = 1
                    x = self.player.rect.x + 16
                arrow = Arrow(ARROW_PNG, x, self.player.position.y, self.player.orientation, ARROW_SPEED, ARROW_MAX_RANGE, (xDirection,0))
                self.arrows.add(arrow)
                self.allSprites.add(arrow)
                pygame.mixer.Sound.play(SHOOT_SOUND)
            if keys[pygame.K_r] and not self.player.reloading:
                self.player.lastReload = pygame.time.get_ticks()
                self.player.reload()
                pygame.mixer.Sound.play(RELOAD_SOUND)
            if self.player.reloading and pygame.time.get_ticks() - self.player.lastReload > self.player.reloadTime:
                self.player.reloading = False

            self.player.update(self.window, self.camera)

            pygame.display.update()


    
    def renderMap(self):
        y = 0
        for layer in self.map:
            x = 0
            for tile in layer:
                if tile <= 0:
                    pygame.draw.rect(self.window, (255,0,255), pygame.Rect(x*16+self.player.camera.x, y*16+self.player.camera.y, TILE_WIDTH, TILE_HEIGHT) )
                if tile > 0:
                    pygame.draw.rect(self.window, (255,255,0), pygame.Rect(x*16+self.player.camera.x, y*16+self.player.camera.y, TILE_WIDTH, TILE_HEIGHT) )

                x += 1
            y += 1
    def spawnEnemy(self):
        x = random.randint(0, self.window.get_width() )
        y = random.randint(0, self.window.get_height() )

        while pygame.math.Vector2(self.player.rect.topleft).distance_to(pygame.math.Vector2(x, y)) < MIN_ENEMY_SPAWN_DISTANCE:
            x = random.randint(0, self.window.get_width() )
            y = random.randint(0, self.window.get_height() )
            
        enemy = Enemy(ENEMY_PNG, x, y, ENEMY_ORIENTATION, ENEMY_SPEED, (self.player.rect.x - x, self.player.rect.y - y) )
        self.enemies.add(enemy)
        self.allSprites(enemy)

        
    def handleCollisions(self):
        pygame.sprite.groupcollide(self.arrows, self.enemies, True, True, pygame.sprite.collide_mask)
        if pygame.sprite.spritecollideany(self.player, self.enemies, pygame.sprite.collide_mask) and pygame.time.get_ticks() - self.player.lastGotHit > INVINCIBLE_DURATION:
            self.player.HP -= 1
            self.player.lastGotHit = pygame.time.get_ticks()
            if self.player.HP <= 0:
                self.running = False

        
