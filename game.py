from turtle import back
import pygame as pg
from settings import *
from assets import gameIcon

class Game:
    def __init__(self, caption, icon, resolution, font):
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
        # State fields
        self.active = True
        # Rects
        self.topBorder = pg.Rect(self.SCREEN_WIDTH*.1,self.SCREEN_HEIGHT*.1,self.SCREEN_WIDTH*.8,1)
        self.bottomBorder = pg.Rect(self.SCREEN_WIDTH*.1,self.SCREEN_HEIGHT*.9,self.SCREEN_WIDTH*.8,1)
        self.leftBorder = pg.Rect(self.SCREEN_WIDTH*.1,self.SCREEN_HEIGHT*.1,1,self.SCREEN_HEIGHT*.8)
        self.rightBorder = pg.Rect(self.SCREEN_WIDTH*.9,self.SCREEN_HEIGHT*.1,1,self.SCREEN_HEIGHT*.8)
    def setBackground(self):
        if type(self.background).__name__ == 'tuple':
            self.screen.fill(self.background)
        if type(self.background).__name__ == 'PosixPath':
            self.screen.blit(pg.transform.scale(pg.image.load(background), (self.SCREEN_WIDTH,self.SCREEN_HEIGHT)),(0,0))
    def update(self):
        pg.display.update()
    def getEvents(self):
        return pg.event.get()

# Game initialization
game = Game(caption, gameIcon, res, font)