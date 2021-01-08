import pygame as pg
import random as rd
import time
import aimabasedlrta
import sys
import math
from search import *
from os import path
from settings import *
from sprites import *
from tilemap import *
vec = pg.math.Vector2

class Game:
    def __init__(self, human = True, map = MAP):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.load_data(map)
        if(PHOTOMODE):
            self.screen = pg.display.set_mode((self.map.width, self.map.height))
        else:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.human = human
        
        self.font_name = pg.font.match_font(FONT_NAME)
        self.actions = ACTIONS
        self.won = False
        self.passwalls = False

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.flag = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.diamonds = pg.sprite.Group()
        self.font = pg.font.SysFont('Consolas', 30)
        self.reward = 0
        self.steps = 0
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
                if tile == '3':
                    Block(self,col, row)
                if tile == '4':
                    Spike(self,col, row)
                if tile == 'D':
                    Diamond(self,col, row)                    
        self.camera = Camera(self.map.width, self.map.height)
        if self.human:
            self.run()
        else:
            self.start_ticks=pg.time.get_ticks()
            self.playing = True
        
        #pos_init = [self.player.pos_init.x,self.player.pos_init.y]
        #goal = [self.goal.x,self.goal.y]
        return self.player.pos_init, self.goal, self.actions

    def load_data(self, map):
        #game_folder = path.dirname(__file__)
        #print(game_folder)
        game_folder = "maps/"
        print(game_folder)
        self.map = Map(path.join(game_folder,map))

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
        self.steps += 1
        if self.human:
            self.all_sprites.update()
        else:
            self.all_sprites.update(action)

        self.camera.update(self.player)
        self.check_colisions()
        if self.player.pos.y > self.map.height + TILESIZE/2:
            self.reward, self.cost = self.get_reward(True, False)
            if self.human:
                print("Dead")
                print("GAMEOVER\nSCORE:", self.reward)
            self.won = False
            self.playing = False
        if self.seconds == MAX_TIME :           #or (not self.human and steps/FPS == MAX_TIME)
            self.reward, self.cost = self.get_reward(False, False)
            if self.human:
                print("No time left")
                print("GAMEOVER\nSCORE:", self.reward)
            self.won = False
            self.playing = False
        self.reward, self.cost = self.get_reward(False, False)

    def check_colisions(self):

        hits_ground = pg.sprite.spritecollide(self.player, self.ground, False)
        if hits_ground:
            if self.player.vel.y > 0:
                self.player.pos.y = hits_ground[0].rect.top
                self.player.vel.y = 0
            elif self.player.vel.y < 0:
                #time.sleep(5)
                if self.player.was_c:
                    self.player.crouching = True
                    self.player.crouch()
                self.player.pos.y = hits_ground[0].rect.bottom + self.player.rect.height
                self.player.vel.y = 0
                
        hits_pipe = pg.sprite.spritecollide(self.player, self.pipes, False)
        if hits_pipe and not self.passwalls:
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
            if self.human:
                print("YOU WON\nSCORE:", self.reward)
            self.won = True
            self.playing = False
            self.passwalls = False

        hits_spike = pg.sprite.spritecollide(self.player, self.spikes, False)
        if hits_spike:
            self.reward, self.cost = self.get_reward(True,True)
            if self.human:
                print("YOU LOST\nSCORE:", self.reward)
            self.won = False
            self.playing = False
            self.passwalls = False
            
        hits_diamond = pg.sprite.spritecollide(self.player, self.diamonds, False)
        if hits_diamond:
            self.passwalls = True

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
        if not PHOTOMODE:
            self.draw_text(str(MAX_TIME - int(self.seconds)), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()
        if PHOTOMODE:
                while 1:
                    continue

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
        self.seconds=(pg.time.get_ticks()-self.start_ticks)/1000 #calculate how many seconds
        self.update(action)
        #self.draw()
        
        return self.seconds ,  self.playing, self.player.pos, self.won

class MySearchProblem(Problem):
    def __init__(self,actions, initial, goal, game):
        super().__init__(actions,initial, goal)
        self.game = game

    def actions(self, state):
        return self.actions

    def h(self, state, bsf):
        #Returns least possible cost to reach a goal for the given state.
        if(not self.game.playing and not self.game.won):
            r = 4000
        else :
            
            #print(bsf)
            #d = self.calc_dist(state)
            d = self.goal.x - self.initial.x
            #print(d)
            #d_step = d/bsf

            #r = int(self.goal.x - state[0] / d_step)                           #working for no reason          
            #r = int((self.goal.x - state[0]) / d_step)
            #r = int(self.calc_dist(state) / d_step)                           #supposed to work
            
            #r = math.ceil((self.goal.x - state[0]-TILESIZE/2)/ 1)
            r = math.ceil((self.goal.x - state[0]-TILESIZE/2)/ 5)
            #r = math.ceil((self.goal.x - state[0]-TILESIZE/2)/ 5.8)
            #r = int(self.calc_dist(state) / 5) 

            #print(r)
        return r

    def calc_dist(self, state):
        goal_up = self.goal.y - (8 * TILESIZE) - TILESIZE
        #print(goal_up, " <= " , state[1], " <= ", self.goal.y + TILESIZE)
        if goal_up <= state[1] <= self.goal.y + TILESIZE:
            return self.goal.x - state[0]
        else:
            closest_point = min([goal_up, self.goal.y], key=lambda x:abs(x-state[1]))
            return math.sqrt( (state[0]- self.goal.x)**2  + (state[1]- closest_point)**2)
        
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

def savereport(filename,beststeps, trials):
    with open("maps/"+ filename+ "/report_"+filename+".txt", 'w') as fid:
        fid.write("Converged in " + str(trials-1000) + " trials\n")
        fid.write("Best solution in " + str(beststeps) + " steps\n")


def play(map, trials, noise):
    MAP = map
    g = Game(False, map)
    pos_init, goal, actions = g.new()
    prob = MySearchProblem(actions, pos_init, goal, g)
    agent = aimabasedlrta.LRTAStarAgent(prob)
    agent.loadfromfile("maps/"+MAP[:-4]+"/agent"+MAP[:-4]+".pkl")
    completed = 0
    fla = -1
    steps = 0
    trial = 0
    comp_score = 0
    bestsofar = 10000
    completed = 0
    pos = pos_init
    maxscore = FPS*MAX_TIME
    while trial < trials:
        steps += 1
        if(trial == 0):
            action = agent(projx(pos),0,fla)
        else:
            action = agent(projx(pos),noise,fla)
        seconds, playing, next_pos, won = g.step(action)
        g.draw()
        g.clock.tick(FPS)
        if not playing:
            if won:
                #stats for analysis
                completed +=1
                comp_score += steps
                bestsofar = min(steps,bestsofar)         
            
            g.new()
            pos = pos_init
                
            steps = 0
            trial += 1
            g.passwalls = False
        else:
            pos = vec(next_pos.x, next_pos.y)
    print("comp:", completed, "score: ",  comp_score)
    return completed, comp_score, maxscore - bestsofar, maxscore

def main():
    #ROBOT RUN
    if AGENT:
        g = Game(False)
        g.show_start_screen()
        pos_init, goal, actions = g.new()
        print("init: ", pos_init, ", goal: ", goal)
        playing = True
        draw = DRAW
        realtime = REALTIME
        prob = MySearchProblem(actions, pos_init, goal, g)
        agent = aimabasedlrta.LRTAStarAgent(prob)
        if LOADFILE:
            agent.loadfromfile("maps/"+MAP[:-4]+"/agent"+MAP[:-4]+".pkl")
        pos = pos_init
        trial = 0
        steps = 0
        bestsofar = 10000
        row_g = 0
        seconds = 0
        completed = 0
        comp_score = 0
        show_dict = False
        fla = -1
        maxscore = FPS*MAX_TIME
        notquit = True
        while notquit:
            if LOADFILE and trial == 100000:
                with open("maps/"+ MAP[:-4]+ "/report_"+MAP[:-4]+".txt", 'r') as fid:
                    data = fid.readlines()

                if len(data) == 2:   
                    data.append("Completed the level " + str(completed/100000 *100) + "% of the times (100000 with " + str(NOISE) + " noise)\n")
                    data.append("Average score: " + str(maxscore - round(comp_score/completed,2))+ " out of possible " + str(maxscore - bestsofar))
                else:
                    data[2] = "Completed the level " + str(completed/100000 *100) + "% of the times (100000 with " + str(NOISE) + " noise)\n"
                    data[3] = "Average score: " + str(maxscore - round(comp_score/completed,2))+ " out of possible " + str(maxscore - bestsofar)
                    
                with open("maps/"+ MAP[:-4]+ "/report_"+MAP[:-4]+".txt", 'w') as fid:
                    fid.writelines( data )    
                print("TEST OVER, Completed the level ", completed/100000*100 ,"% of the times")
                break
            steps += 1
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    notquit = False
                if (event.type == pg.KEYDOWN and event.key == pg.K_p):
                    leave = False
                    while not leave:
                        for event in pg.event.get():
                            if (event.type == pg.KEYDOWN and event.key == pg.K_p):
                                leave = True
                if (event.type == pg.KEYDOWN and event.key == pg.K_d):
                    draw = not draw
                if (event.type == pg.KEYDOWN and event.key == pg.K_r):
                    realtime = not realtime
                if (event.type == pg.KEYDOWN and event.key == pg.K_m):
                    fla = fla * -1
                    show_dict = not show_dict
            if(trial == 0):
                action = agent(projx(pos),0,fla)
            else:
                action = agent(projx(pos),NOISE,fla)
            #print("action: ",action)
            
            seconds, playing, next_pos, won = g.step(action)
            if draw:
                g.draw()
            if realtime:
                g.clock.tick(FPS)
            if LEARNING:
                agent.update(projx(pos),action,projx(next_pos),fla)

            #RESET WORLD         
            if not playing:    
                if won:
                    
                    #stats for analysis
                    completed +=1
                    comp_score += steps

                    bestsofar = min(steps,bestsofar)
                    if(steps == bestsofar):
                        row_g+=1
                    print(G,"end, trial",trial,"in",steps,"steps/",bestsofar, W)
                    if row_g == 1000 and not LOADFILE:
                        if SAVEFILE:
                            print('Saving agent!')
                            if(not os.path.isdir("maps/"+MAP[:-4])):
                                print("hello")
                                os.mkdir("maps/"+MAP[:-4])
                            agent.savetofile("maps/"+MAP[:-4] + "/agent" + MAP[:-4]+ ".pkl")
                            savereport(MAP[5:-4], steps, trial)
                        break
                else:
                    print(R,"end, trial",trial,"in",steps,"steps/",bestsofar, W)
                    row_g = 0


                g.new()
                pos = pos_init
                
                steps = 0
                trial += 1
                
                # deveria aqui algum reset de estado. por agora so
                g.passwalls = False
            else:
                pos = vec(next_pos.x, next_pos.y)
                #print(pos)
        pg.quit()

    #HUMAN RUN
    else:
        g = Game()
        while g.running:
            g.new()
        pg.quit()

if __name__ == "__main__":
    main()