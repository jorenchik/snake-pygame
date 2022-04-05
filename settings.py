import configparser
from os import mkdir
import pathlib as pl

# Absolute path
absPath = pl.Path.cwd()
# User files
userFiles = pl.Path(absPath/'user_files')
if not userFiles.exists():
    mkdir('user_files')

# Config load / set up
configFile = pl.Path(userFiles/'config.ini')
print(configFile)
config = configparser.ConfigParser()
try: 
    config.read(configFile)
except:
    print('Error related to the config file, replacing the contents of it.')
    with open(configFile, 'w') as f:
        f.write('')
    config.read(configFile)

settings = {
    'multiplayer':False,
    'player1Color': 'blue',
    'player2Color': 'purple',
    'portalWalls': False,
    'speedIncAfterEat': False,
    'initialMovementPeriod': 250,
    'initialSpeed': 1,
    'poisonousFoodCount': 3,
    'foodCount': 3,
    'poisonousFoodRespawn': True
}
valid = True
if not config.has_section('GAMEPLAY'): valid = False
for op in settings.keys():
    if not config.has_option('GAMEPLAY', op):
        valid = False
        break
if not configFile.exists() or not valid:
    config['GAMEPLAY'] = settings
    with open(configFile, 'w') as configfile:
        config.write(configfile)

# Game caption
caption = 'Snake game'

# Gameplay
portalWalls = True if config['GAMEPLAY']['portalWalls'] == 'True' else False
multiplayer = True if config['GAMEPLAY']['multiplayer'] == 'True' else False
initialSpeed = int(config['GAMEPLAY']['initialSpeed'])
initialMovementPeriod = int(config['GAMEPLAY']['initialMovementPeriod'])
speedIncAfterEat = True if config['GAMEPLAY']['speedIncAfterEat'] == 'True' else False
poisonousFoodCount = int(config['GAMEPLAY']['poisonousFoodCount'])
foodCount = int(config['GAMEPLAY']['foodCount'])
foodLimit = 10
poisonousFoodRespawn = True if config['GAMEPLAY']['poisonousFoodRespawn'] == 'True' else False
speedUnit = 20
snakeBaseVelocity = (1,0)
minInitialSpeed = 1
maxInitialSpeed = 7
wallWidth = 15
wallHeight = 15

# Screen
res = (1920,1080)
fullscreen = True

# Font
scoreFontSize = 50
gameOverFontSize = 50
fpsFontSize = 30
scoreboardFontSize = 25
font = 'Arial'

# Colors
background = (37,38,33)
blue = (54,79,243)
red = (210,27,27)
white = (255,255,255)
grey = (31,31,47)
red = (255,0,0)
green = (41,159,32)
magenta = (255,0,255)
cyan = (0,255,255)
yellow = (255,255,0)
lime = (0,255,0)
purple = (238,130,238)
orange = (255,215,0)
brown = (165,42,42)
snakeBaseColor = (91,123,249)
foodBaseColor = (218,72,15)
snakeColors = {'blue':blue,'purple':purple,'lime':lime,'orange':orange,'brown':brown,'white':white,'magenta':magenta,'blue':blue,'yellow':yellow,'cyan':cyan}
foodColors = {'food':green, 'poison': red}
player1Color = snakeColors[config['GAMEPLAY']['player1Color']]
player2Color = snakeColors[config['GAMEPLAY']['player2Color']]

# Game colors
hitboxColor = red
snakeColor = grey
foodColor = green
poisonousFoodColor = red

# Playfield
rectDims = (30,20)
playfieldSize = (.8,.8)
playfieldYOffset = (.03)

# Menu
menuFontSize = 50
menuFontColor = white
menuItemMargin = 40
pointerSizeMult = 1
pointerSize = (15,30)
pointerLeftMargin = 20
scoreboardMargin = 20
scoreBottomPadding = 15