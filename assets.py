from os import mkdir
import pathlib as pl
from PIL import Image
from settings import snakeBaseColor, foodBaseColor, snakeColors, foodColors
import pickle as pc

# Aboslute path
absPath = pl.Path.cwd()
# Assets path
assets = pl.Path(absPath/'assets')
# User files path
userFiles = pl.Path(absPath/'user_files')
if not userFiles.exists():
    mkdir('user_files')

# Game icon
gameIcon = pl.Path(assets/'icons/icon.png')

# Snake part images
partImgs = {
    'headRight': pl.Path(assets/'parts/head_right.png'),
    'headUp': pl.Path(assets/'parts/head_up.png'),
    'headLeft': pl.Path(assets/'parts/head_left.png'),
    'headDown': pl.Path(assets/'parts/head_down.png'),
    'bodyHor': pl.Path(assets/'parts/body_horizontal.png'),
    'bodyVer': pl.Path(assets/'parts/body_vertical.png'),
    'topRight': pl.Path(assets/'parts/body_topright.png'),
    'bottomRight': pl.Path(assets/'parts/body_bottomright.png'),
    'topLeft': pl.Path(assets/'parts/body_topleft.png'),
    'bottomLeft': pl.Path(assets/'parts/body_bottomleft.png'),
    'tailRight':pl.Path(assets/'parts/tail_right.png'),
    'tailUp':pl.Path(assets/'parts/tail_up.png'),
    'tailLeft':pl.Path(assets/'parts/tail_left.png'),
    'tailDown':pl.Path(assets/'parts/tail_down.png'),
}

# Food images
foodImgs = {
    'food': pl.Path(assets/'foods/apple.png'),
    'poison': pl.Path(assets/'foods/apple.png'),
}

# Changes sprite colors
def changeImgColor(img,colorTo,colorFrom):
    img = Image.open(img).convert('RGBA')
    width = img.size[0] 
    height = img.size[1] 
    for i in range(0,width):
        for j in range(0,height):
            data = img.getpixel((i,j))
            if (data[0]==255 and data[1]==255 and data[2]==255):
                img.putpixel((i,j),(255,255,255,0))
            elif (data[0]==colorFrom[0] and data[1]==colorFrom[1] and data[2]==colorFrom[2]):
                img.putpixel((i,j),colorTo)
    return img

# Part color change
partColoredImgs = {}
for k,img in partImgs.items():
    newDict={}
    for key,col in snakeColors.items():
        newDict[key]=changeImgColor(img,col,snakeBaseColor)
    partColoredImgs[k] = newDict

# Food color change
foodColoredImgs = {}
for k,img in foodImgs.items():
    for key,col in foodColors.items():
        color=changeImgColor(img,col,foodBaseColor)
        foodColoredImgs[key] = color

# Wall sprites
wall = pl.Path(assets/'walls/wall_pattern_horizontal.png')
sideWall = pl.Path(assets/'walls/wall_pattern_vertical.png')

# Highscore set up
spHighcoreFile = pl.Path(userFiles/'sp_highscores.pkl')
mpHighcoreFile = pl.Path(userFiles/'mp_highscores.pkl')
if not spHighcoreFile.exists():
    with open(spHighcoreFile,"wb") as out:
        pc.dump({}, out)
if not mpHighcoreFile.exists():
    with open(mpHighcoreFile,"wb") as out:
        pc.dump({}, out)

