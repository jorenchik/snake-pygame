import pathlib as pb
from PIL import Image
from settings import snakeBaseColor, foodBaseColor, snakeColors, foodColors
import pickle as pc

# Aboslute path
absPath = pb.Path.cwd()
# Assets path
assets = pb.Path(absPath/'assets')
# Game icon
gameIcon = pb.Path(assets/'icons/icon.png')

# Snake part images
partImgs = {
    'headRight': pb.Path(assets/'parts/head_right.png'),
    'headUp': pb.Path(assets/'parts/head_up.png'),
    'headLeft': pb.Path(assets/'parts/head_left.png'),
    'headDown': pb.Path(assets/'parts/head_down.png'),
    'bodyHor': pb.Path(assets/'parts/body_horizontal.png'),
    'bodyVer': pb.Path(assets/'parts/body_vertical.png'),
    'topRight': pb.Path(assets/'parts/body_topright.png'),
    'bottomRight': pb.Path(assets/'parts/body_bottomright.png'),
    'topLeft': pb.Path(assets/'parts/body_topleft.png'),
    'bottomLeft': pb.Path(assets/'parts/body_bottomleft.png'),
    'tailRight':pb.Path(assets/'parts/tail_right.png'),
    'tailUp':pb.Path(assets/'parts/tail_up.png'),
    'tailLeft':pb.Path(assets/'parts/tail_left.png'),
    'tailDown':pb.Path(assets/'parts/tail_down.png'),
}

# Food images
foodImgs = {
    'food': pb.Path(assets/'parts/apple.png'),
    'poison': pb.Path(assets/'parts/apple.png'),
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
wall = pb.Path(assets/'walls/wall-pattern-2.png')
sideWall = pb.Path(assets/'walls/wall-pattern-3.png')

# Highscore set up
spHighcoreFile = pb.Path(absPath/'sp_highscores.pkl')
mpHighcoreFile = pb.Path(absPath/'mp_highscores.pkl')
if not spHighcoreFile.exists():
    with open("sp_highscores.pkl","wb") as out:
        pc.dump({}, out)
if not mpHighcoreFile.exists():
    with open("mp_highscores.pkl","wb") as out:
        pc.dump({}, out)

