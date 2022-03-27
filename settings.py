import configparser
import pathlib as pl

absPath = pl.Path.cwd()
configFile = pl.Path(absPath/'config.ini')
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
    'player1Color': 'white',
    'player2Color': 'magenta',
    'portalWalls': False,
    'speedIncAfterEat': False
}

valid = True
if not config.has_section('GAMEPLAY'): valid = False
for op in settings.keys():
    if not config.has_option('GAMEPLAY', op):
        valid = False
        break

if not configFile.exists() or not valid:
    config['GAMEPLAY'] = settings
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    configFile = pl.Path(absPath/'config.ini')

# Game caption
caption = 'Snake game'

# Gameplay
portalWalls = True if config['GAMEPLAY']['portalWalls'] == 'True' else False
selfRectalCollisionAllowed = False
otherRectalCollisionAllowed = False
multiplayer = True if config['GAMEPLAY']['multiplayer'] == 'True' else False
hitboxesVisible = False
initialMovingPeriod = 250
snakeBaseVelocity = (1,0)
speedIncAfterEat = True if config['GAMEPLAY']['speedIncAfterEat'] == 'True' else False

# Screen
res = (1920,1080)
# res = (800,600)
fullscreen = True
drawPlayfieldRects = False

# Fps and time
fps = 60

# Font
scoreFontSize = 50
gameOverFontSize = 50
fpsFontSize = 30
font = 'Arial'

# Colors
background = (37,38,33)
red = (210,27,27)
white = (255,255,255)
grey = (31,31,47)
red = (255,0,0)
green = (41,159,32)
magenta = (255,0,255)
cyan = (0,255,255)
yellow = (255,255,0)
lime = (0,255,0)
blue = (0,0,255)
snakeColors = {'white':white,'magenta':magenta,'blue':blue,'yellow':yellow,'cyan':cyan}
foodColors = {'food':green, 'poison': red}
player1Color = snakeColors[config['GAMEPLAY']['player1Color']]
player2Color = snakeColors[config['GAMEPLAY']['player2Color']]
snakeBaseColor = (91,123,249)
foodBaseColor = (218,72,15)

# Game colors
hitboxColor = red
wallColor = white
snakeColor = grey
foodColor = green
poisonousFoodColor = red

# Playfield
rectDims = (30,20)
    # percentages
playfieldSize = (.8,.8)
playfieldYOffset = (.03)

# Menu
menuFontSize = 50
menuFontColor = white
menuItemMargin = 40
pointerSizeMult = 1
pointerSize = (15,30)
pointerLeftMargin = 20