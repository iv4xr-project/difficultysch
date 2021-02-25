# Sprite Classes
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,game, x, y, gravity_factor, acceleration_factor):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE*2))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = (vec(x, y) * TILESIZE) + vec(0,TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos_init = vec(x,y) * TILESIZE
        self.was_c = False
        self.crouching = False
        self.gravity_factor = gravity_factor
        self.acceleration_factor = acceleration_factor
    
    def jump(self):
        #jump only if standing
        self.rect.x +=1
        hits_g = pg.sprite.spritecollide(self, self.game.ground, False)
        hits_p = pg.sprite.spritecollide(self, self.game.pipes, False)
        self.rect.x -=1
        if hits_g or hits_p:
            self.vel.y = -PLAYER_JUMP

    def crouch(self):
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

    def update(self, action = 0):
        self.acc = vec(0,PLAYER_GRAV*(1+self.gravity_factor))
        p = False
        if self.game.human:
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.acc.x = -PLAYER_ACC * (1+self.acceleration_factor)
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.acc.x = PLAYER_ACC * (1+self.acceleration_factor)
                p = True
            if keys[pg.K_s]:
                self.crouching = True
                self.was_c = True
                self.image = pg.Surface((TILESIZE,TILESIZE))
                self.image.fill(YELLOW)
                self.rect = self.image.get_rect()
            else:
                if self.crouching:
                    self.was_c = True
                else:
                    self.was_c = False
                self.crouching  = False
                self.image = pg.Surface((TILESIZE,TILESIZE*2))
                self.image.fill(YELLOW)
                self.rect = self.image.get_rect()
        else:
            if action == 1:
                self.acc.x = -PLAYER_ACC * (1+self.acceleration_factor)
            elif action == 2:
                self.acc.x = PLAYER_ACC * (1+self.acceleration_factor)
            elif action == 3:
                self.jump()
            elif action == 4:
                self.acc.x = -PLAYER_ACC * (1+self.acceleration_factor)
                self.jump()
            elif action == 5:
                self.acc.x = PLAYER_ACC * (1+self.acceleration_factor)
                self.jump()
        if p:
            pos_ant = vec(self.pos.x, self.pos.y)
        #apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #equations of motion
        self.vel += self.acc
        # nao percebo este 0.5, acho que deveria ser 1.
        #self.pos += self.vel + 0.5 * self.acc 
        self.pos += self.vel +  self.acc 

        #if p:
            #print(self.pos.x - pos_ant.x)
        self.rect.midbottom = self.pos

    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                print("col detect")
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    
class Ground(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        self.groups = game.all_sprites, game.ground
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Pipe(pg.sprite.Sprite):
    def __init__(self,game, x, y, height):
        self.groups = game.all_sprites, game.pipes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE*height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE - TILESIZE*(height-1)

class Flag(pg.sprite.Sprite):
    def __init__(self,game, x,y):
        self.groups = game.all_sprites, game.flag
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE* 8))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE - TILESIZE*7

class Block(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Spike(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        self.groups = game.all_sprites, game.spikes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
        
class Diamond(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        self.groups = game.all_sprites, game.diamonds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE        