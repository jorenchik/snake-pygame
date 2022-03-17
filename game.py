from turtle import back, screensize
import pygame as pg
from settings import *
from assets import gameIcon
from grid import Playfield
import time


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
        self.prevTime = time.time()
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
        self.now = time.time()
        self.dt = (self.now - self.prevTime) * 1000
        self.prevTime = self.now

# Game initialization
playfieldWidth = res[0] * playfieldSize[0]
playfieldHeight = res[1] * playfieldSize[1]

playfield = Playfield(rectDims, (playfieldWidth, playfieldHeight), playfieldSize, res)
game = Game(caption,gameIcon,res,font,playfield)
