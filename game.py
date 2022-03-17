import pygame as pg
from settings import *
from assets import gameIcon
from grid import Playfield
import time as t
import random as rd


class SnakePart():
    def __init__(self, type, direction=False, speed=False):
        self.pos = (rd.randint(1,rectDims[0]-1),rd.randint(1,rectDims[1]-1))
        self.type = type
        self.direction = pg.Vector2(1,0) if not direction else direction
        self.speed = pg.Vector2(1,0) if not speed else speed
        x = game.getSnakePartCoords(self.pos)[0]
        y = game.getSnakePartCoords(self.pos)[1]
        self.rect = pg.Rect(x,y,game.playfield.rectSize[0],game.playfield.rectSize[1])

class Game:
    def __init__(self, caption, icon, resolution, font, playfield):
        pg.init()
        pg.display.set_caption(caption)
        # Main fields
        self.font = pg.font.SysFont(font, fontSize)
        pg.font.init()
        self.gameIcon = pg.image.load(icon)
        self.screen = pg.display.set_mode(resolution, pg.FULLSCREEN if fullscreen else None)
        self.SCREEN_WIDTH = pg.display.get_window_size()[0]
        self.SCREEN_HEIGHT = pg.display.get_window_size()[1]
        self.background = background
        self.hitboxColor = hitboxColor
        # Clock
        self.clock = pg.time.Clock()
        self.prevTime = t.time()
        self.now = False
        self.fps = fps
        self.dt = False
        # State fields
        self.active = True
        # Rects
        self.sidePadding = round((1-playfieldSize[0])/2, 3)
        self.topPadding = round((1-playfieldSize[1])/2, 3)
        self.topBorder = pg.Rect(self.SCREEN_WIDTH*self.sidePadding,self.SCREEN_HEIGHT*(self.topPadding),self.SCREEN_WIDTH*playfieldSize[0],1)
        self.bottomBorder = pg.Rect(self.SCREEN_WIDTH*self.sidePadding,self.SCREEN_HEIGHT*(playfieldSize[1]+self.topPadding),self.SCREEN_WIDTH*playfieldSize[0],1)
        self.leftBorder = pg.Rect(self.SCREEN_WIDTH*self.sidePadding,self.SCREEN_HEIGHT*self.topPadding,1,self.SCREEN_HEIGHT*(playfieldSize[1]))
        self.rightBorder = pg.Rect(self.SCREEN_WIDTH*(playfieldSize[0]+self.sidePadding),self.SCREEN_HEIGHT*self.topPadding,1,self.SCREEN_HEIGHT*playfieldSize[1])
        # Playfield
        self.playfield = playfield
        # Snake parts
        self.snakeParts = []
    def setBackground(self):
        if type(self.background).__name__ == 'tuple':
            self.screen.fill(self.background)
        if type(self.background).__name__ == 'PosixPath':
            self.screen.blit(pg.transform.scale(pg.image.load(background), (self.SCREEN_WIDTH,self.SCREEN_HEIGHT)),(0,0))
    def update(self):
        pg.display.update()
    def getEvents(self):
        return pg.event.get()
    def onUpdate(self):
        self.setBackground()
        self.clock.tick(self.fps)
        self.now = t.time()
        self.dt = (self.now - self.prevTime) * 1000
        self.prevTime = self.now
    def moveSnakePart(self,snakePart,pos):
        (snakePart.x, snakePart.y) = self.getSnakePartCoords(pos)
    def getSnakePartCoords(self, pos):
        return (self.playfield.rects[pos[0]][pos[1]].x,self.playfield.rects[pos[0]][pos[1]].y)

# Game initialization
playfieldWidth = res[0] * playfieldSize[0]
playfieldHeight = res[1] * playfieldSize[1]

playfield = Playfield(rectDims, (playfieldWidth, playfieldHeight), playfieldSize, res)
game = Game(caption,gameIcon,res,font,playfield)

snakeHead = SnakePart('head')
game.snakeParts.append(snakeHead)
for snakePart in game.snakeParts:
    game.moveSnakePart(snakePart,snakePart.pos)