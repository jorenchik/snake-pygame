from game import game
from settings import *
import pygame as pg

def main():
    # Active action loop
    while game.active:
        game.onUpdate()

        # Events
        if game.isQuit(): quit()
        headPart = game.snakeParts[0]
        if headPart.movementPeriod:
            if headPart.prevMoveMoment:
                if (game.now - headPart.prevMoveMoment) >= headPart.movementPeriod: 
                    game.moveSnakePart(game.snakeParts[0],game.snakeParts[0].pos,game.snakeParts[0].velocity)
        else: game.moveSnakePart(game.snakeParts[0],game.snakeParts[0].pos,game.snakeParts[0].velocity)

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

