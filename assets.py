import pathlib as pb
from PIL import Image
import numpy as np
from settings import colors, colorKeys
import pygame as pg

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
    'bottomLeft': pb.Path(assets/'parts/body_bottomleft.png')
}

# if (data[0]==91 and data[1]==123 and data[2]==249):
                # img.putpixel((i,j),(44, 44, 44))

imgBaseColor = (91,123,249)
def changeImgColor(img,colorTo,colorFrom=imgBaseColor):
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

# changeImgColor(partImgs['headRight'],(255,0,0)).show()
# exit()

partColoredImgs = {}
for k,img in partImgs.items():
    newDict={}
    for key,col in colors.items():
        newDict[key]=changeImgColor(img,col)
    partColoredImgs[k] = newDict

