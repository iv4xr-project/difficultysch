import pygame as pg
import random as rd
import time
import aimabasedlrta
import sys
from search import *
from os import path
from settings import *
from sprites import *
from tilemap import *
vec = pg.math.Vector2

class Game:
    def __init__(self, human = True):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.human = human
        self.load_data()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.actions = ACTIONS

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.flag = pg.sprite.Group()
        self.font = pg.font.SysFont('Consolas', 30)
        self.reward = 0
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Ground(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == '2':
                    Pipe(self, col, row,2)
                if tile == 'F':
                    Flag(self, col, row)
                    self.goal = vec(col,row) * TILESIZE
        self.camera = Camera(self.map.width, self.map.height)
        
        if self.human:
            self.run()
        else:
            self.start_ticks=pg.time.get_ticks()
            self.playing = True
        
        #pos_init = [self.player.pos_init.x,self.player.pos_init.y]
        #goal = [self.goal.x,self.goal.y]
        return self.player.pos_init, self.goal, self.actions

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, MAP))

    def run(self):
        # Game Loop
        self.playing = True
        self.start_ticks=pg.time.get_ticks()
        while self.playing:
            self.seconds=int((pg.time.get_ticks()-self.start_ticks)/1000) #calculate how many seconds
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        

    def update(self, action = 0):
        # Game Loop - Update
        if self.human:
            self.all_sprites.update()
        else:
            self.all_sprites.update(action)
        self.camera.update(self.player)
        hits_ground = pg.sprite.spritecollide(self.player, self.ground, False)
        if hits_ground:
            if self.player.vel.y > 0:
                self.player.pos.y = hits_ground[0].rect.top
                self.player.vel.y = 0
            elif self.player.vel.y < 0:
                self.player.pos.y = hits_ground[0].rect.bottom + self.player.rect.height
                self.player.vel.y = 0
        hits_pipe = pg.sprite.spritecollide(self.player, self.pipes, False)
        if hits_pipe:
            if self.player.pos.x < hits_pipe[0].rect.left and hits_pipe[0].rect.top <= self.player.pos.y- self.player.rect.height/2:
                self.player.pos.x = hits_pipe[0].rect.left - self.player.rect.width/2
                self.player.vel.x = 0
            elif self.player.pos.x > hits_pipe[0].rect.left and hits_pipe[0].rect.top <= self.player.pos.y- self.player.rect.height/2 :
                self.player.pos.x = hits_pipe[0].rect.right + self.player.rect.width/2
                self.player.vel.x = 0
            elif hits_pipe[0].rect.top > self.player.pos.y- self.player.rect.height/2 :
                self.player.pos.y = hits_pipe[0].rect.top
                self.player.vel.y = 0
            
        hits_flag = pg.sprite.spritecollide(self.player, self.flag, False)
        if hits_flag:
            self.reward, self.cost = self.get_reward(False,True)
            print("YOU WON\nSCORE:", self.reward)
            self.playing = False
        if self.player.pos.y > 385.2 + TILESIZE:
            self.reward, self.cost = self.get_reward(True, False)
            print("Dead")
            print("GAMEOVER\nSCORE:", self.reward)
            self.playing = False
        if self.seconds == MAX_TIME:
            self.reward, self.cost = self.get_reward(False, False)
            print("No time left")
            print("GAMEOVER\nSCORE:", self.reward)
            self.playing = False
        self.reward, self.cost = self.get_reward(False, False)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def get_reward(self, dead, end):
        reward = int(self.player.pos.x - self.player.pos_init.x) + self.seconds*2
        if dead:
            reward-=200
        elif end:
            reward+=1000
        cost = 2000 - reward
        return reward, cost

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.draw_text(str(MAX_TIME - self.seconds), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def step(self, action):
        self.seconds=int((pg.time.get_ticks()-self.start_ticks)/1000) #calculate how many seconds
        self.clock.tick(FPS)
        self.update(action)
        self.draw()
        
        return self.reward ,  self.playing, self.player.pos, self.cost

class MySearchProblem(Problem):
    def __init__(self,actions, initial, goal):
        super().__init__(actions,initial, goal)

    def actions(self, state):
        return self.actions

    def h(self, state):
        #Returns least possible cost to reach a goal for the given state.
        if (state[1] > 385.2 + TILESIZE):
            r = 4000
        else:
            r = self.goal.x -state[0]
        return r

    def c(self, s, a, s1):
        #Returns a cost estimate for an agent to move from state 's' to state 's1'.
        return 1

    def goal_test(self, state):
        x = state
        if (x[1]==0 and x[0]==0) or x[0]>10:
            return True
        return False


def projx(s):
    return (round(s.x,2),round(s.y,2)) 


#ROBOT RUN
if AGENT:
    g = Game(False)
    g.show_start_screen()
    pos_init, goal, actions = g.new()
    print("init: ", pos_init, ", goal: ", goal)
    playing = True

    prob = MySearchProblem(actions, pos_init, goal)
    agent = aimabasedlrta.LRTAStarAgent(prob)
    pos = pos_init
    count = 0
    while 1:
        #time.sleep(0.1)
        print("-----------------------")
        action = agent(projx(pos),NOISE)
        #print("action: ",action)
        pos2 = pos
        reward, playing, next_pos, _ = g.step(action)
        agent.update(projx(pos),action,projx(next_pos))
        #RESET WORLD    
        if not playing:
            g.new()
            pos = pos_init
        else:
            pos = vec(next_pos.x, next_pos.y)
    pg.quit()

#HUMAN RUN
else:
    g = Game()
    while g.running:
        g.new()
    pg.quit()
