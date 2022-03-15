import pygame as pg
from settings import *
from assets import gameIcon

class Game:
    def __init__(self, caption, icon, resolution, font):
        pg.init()
        pg.display.set_caption(caption)
        self.font = pg.font.SysFont(font, fontSize)
        pg.font.init()
        self.gameIcon = pg.image.load(icon)
        self.screen = pg.display.set_mode(resolution)
        self.SCREEN_WIDTH = pg.display.get_window_size()[0]
        self.SCREEN_HEIGHT = pg.display.get_window_size()[1]

# Game initialization
game = Game(caption, gameIcon, res, font)