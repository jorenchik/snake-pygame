from typing import NewType
from matplotlib.style import available
from pandas import array
import pygame as pg
from settings import *
from assets import gameIcon
from grid import Playfield
import time as t
import random as rd
import numpy as np

# Helper funtion (Die and dump)
def dd(var):
    print(var)
    exit()

class Food():
    def __init__(self, isPoisonous:bool=False):
        pos = game.getRandomAvailablePos()
        if pos:
            self.pos = (pos[0],pos[1])
        else:
            game.gameWon = True
            self.pos = (rd.randint(1,rectDims[0]-1),rd.randint(1,rectDims[1]-1))
        self.x = game.getCoords(self.pos)[0]
        self.y = game.getCoords(self.pos)[1]
        self.poisonous = isPoisonous
        # Appearance
        self.rect = pg.Rect(self.x,self.y,game.playfield.rectSize[0],game.playfield.rectSize[1])
        self.color = foodColor

class SnakePart():
    def __init__(self,type,prevMoveMoment=False,pos=False,velocity=False):
        # General props
        self.type = type
        # Physical props
        self.pos = (pos[0] if pos else rd.randint(1,rectDims[0]-1),pos[1] if pos else rd.randint(1,rectDims[1]-1))
        self.prevPos = pos
        self.prevVelocity = velocity
        self.x = game.getCoords(self.pos)[0]
        self.y = game.getCoords(self.pos)[1]
        self.velocity = pg.Vector2(4,0) if not velocity else velocity
        self.prevMoveMoment = False if not prevMoveMoment else prevMoveMoment
        if self.velocity.length() > 0:
            self.movementPeriod = 1/self.velocity.length()
        else:
            self.movementPeriod = False
        # Appearance
        self.rect = pg.Rect(self.x,self.y,game.playfield.rectSize[0],game.playfield.rectSize[1])
        self.color = snakeColor
    def changeDirToAnAngle(self, angle):
        if angle == 0 and self.velocity.x >= 0: (self.velocity.y, self.velocity.x) = (0, self.velocity.length())
        if angle == 90 and self.velocity.y <= 0: (self.velocity.y, self.velocity.x) = (-self.velocity.length(), 0)
        if angle == 180 and self.velocity.x <= 0: (self.velocity.y, self.velocity.x) = (0, -self.velocity.length())
        if angle == 270 and self.velocity.y >= 0: (self.velocity.y, self.velocity.x) = (self.velocity.length(), 0)

class Game:
    def __init__(self, caption, icon, resolution, font, playfield):
        pg.init()
        pg.display.set_caption(caption)
        # Main fields
        self.font = pg.font.SysFont(font, fontSize)
        pg.font.init()
        self.gameIcon = pg.image.load(icon)
        self.screen = pg.display.set_mode(resolution, pg.FULLSCREEN if fullscreen else 0)
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
        self.previousDirChange = False
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
        self.occupiedPositions = []
        self.availablePositions = []
        self.getAvailablePositions()
        # Snake parts
        self.snakeParts = []
        # Foods
        self.foods = []
        # Events
        self.events = []
        # State
        self.snakeAlive = True
        self.gameWon = False
    def setBackground(self):
        if type(self.background).__name__ == 'tuple':
            self.screen.fill(self.background)
        if type(self.background).__name__ == 'PosixPath':
            self.screen.blit(pg.transform.scale(pg.image.load(background), (self.SCREEN_WIDTH,self.SCREEN_HEIGHT)),(0,0))
    def update(self):
        pg.display.update()
    def getEvents(self):
        return pg.event.get()
    def isQuit(self):
        for event in self.events:
            if event.type == pg.QUIT: return True
            if hasattr(event, 'key'):
                if self.isKey(pg.K_ESCAPE): return True
        return False
    def isKey(self, key):
        for event in self.events:
            if event.type == pg.KEYDOWN:
                if event.key == key: 
                    return True
        return False
    def onUpdate(self):
        # Deltatime
        self.setBackground()
        self.clock.tick(self.fps)
        self.now = t.time()
        self.dt = (self.now - self.prevTime) * 1000
        self.prevTime = self.now
        # Get events
        self.events = self.getEvents()
        # Determines occupied positions on the playfield
        self.occupiedPositions = []
        for snakePart in self.snakeParts:
            self.occupiedPositions.append(snakePart.pos)
        for food in self.foods:
            self.occupiedPositions.append(food.pos)
        self.getAvailablePositions()
    def moveSnakePart(self,snakePart,pos,velocity=False):
        if self.snakeAlive:
            if velocity:
                if velocity.x > 0: xMove = 1
                elif velocity.x < 0: xMove = -1
                else: xMove = 0
                if velocity.y > 0: yMove = 1
                elif velocity.y < 0: yMove = -1
                else: yMove = 0
            else:
                yMove = 0
                xMove = 0 
            if (snakePart.pos[0]+xMove not in range(0, rectDims[0]) or snakePart.pos[1]+yMove not in range(0, rectDims[1])) and not portalWalls:
                self.snakeAlive = False
            else:
                (newXPos, newYPos) = (int(pos[0]+xMove), int(pos[1]+yMove))
                
                if newXPos >= rectDims[0]: newXPos -= rectDims[0]
                if newXPos < 0: newXPos += rectDims[0]
                if newYPos >= rectDims[1]: newYPos -= rectDims[1]
                if newYPos < 0: newYPos += rectDims[1]
                snakePart.pos = (newXPos, newYPos)
                snakeCoords = self.getCoords(snakePart.pos)
                (snakePart.x, snakePart.y) = snakeCoords
                (snakePart.rect.x, snakePart.rect.y) = snakeCoords
                snakePart.prevMoveMoment = t.time()
    def getCoords(self, pos):
        return (self.playfield.rects[pos[0]][pos[1]].x,self.playfield.rects[pos[0]][pos[1]].y)
    def createFood(self):
        self.foods.append(Food())
    def createSnakePart(self, type, prevMoveMoment, pos=False, velocity=False):
        self.snakeParts.append(SnakePart(type,prevMoveMoment, pos if pos else False, velocity if velocity else False))
    def checkRectalCollision(self,pos1,pos2):
        if pos1[0] == pos2[0] and pos1[1] == pos2[1]: return True
        else: return False
    def getAvailablePositions(self):
        self.availablePositions = []
        for col in self.playfield.rects:
            for rect in col:
                if rect.pos not in self.occupiedPositions:
                    self.availablePositions.append(rect.pos)
    def getRandomAvailablePos(self):
        if len(self.availablePositions) == 0: return False
        return rd.choice(self.availablePositions)

# Game initialization
playfieldWidth = res[0] * playfieldSize[0]
playfieldHeight = res[1] * playfieldSize[1]

playfield = Playfield(rectDims, (playfieldWidth, playfieldHeight), playfieldSize, res)
game = Game(caption,gameIcon,res,font,playfield)
