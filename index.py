from game import game
from settings import *
import pygame as pg

def main():
    # Active action loop
    while game.active:
        game.onUpdate()

        # Events
        game.events = game.getEvents()
        # print(game.events)
        if game.isQuit(): quit()

        # Draw the walls
        pg.draw.rect(game.screen, wallColor,game.topBorder)
        pg.draw.rect(game.screen, wallColor,game.bottomBorder)
        pg.draw.rect(game.screen, wallColor,game.leftBorder)
        pg.draw.rect(game.screen, wallColor,game.rightBorder)

        # Draw the rects
        rects = game.playfield.rects
        for col in rects:
            for rect in col:
                pg.draw.rect(game.screen, wallColor,rect, 1)

        # Draw snake parts
        for snakePart in game.snakeParts:
            pg.draw.rect(game.screen, wallColor,snakePart, 5)

        game.update()
main()

