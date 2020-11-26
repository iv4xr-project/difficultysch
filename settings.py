# game options/settings
TITLE = "MARIO"
MAP = "maps/map_dif3.txt"
WIDTH = 480
HEIGHT = 416
FPS = 60

#Player properties
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 18

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (165,42,42)

TILESIZE = 32
FONT_NAME = 'arial'
MAX_TIME = 20

#SPACESTATE 0 = NOP, 1 = left, 2 = right, 3 = jump, 4 - left+jump, 5 - right+jump
ACTIONS = [2,3,0]

#AGENT
AGENT = True
DRAW = True
REALTIME = True
SAVEFILE = True
LOADFILE = False
NOISE = 0.0


#console color
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple