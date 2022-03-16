import pygame as pg

class Playfield:
    def __init__(self, rects, size):
        self.rects = rects

class GridRect:
    def __init__(self, pos):
        self.pos = pg.Vector2(pos)
    