from game import game
from settings import *
import pygame as pg

def main():
    # Active action loop
    while game.active:
        game.onUpdate()

        headPart = game.snakeParts[0]
        # Events
        if game.isQuit(): quit()
        if game.isKey(pg.K_UP):
            headPart.moveUp()
        if game.isKey(pg.K_DOWN):
            headPart.moveDown()
        if game.isKey(pg.K_LEFT):
            headPart.moveLeft()
        if game.isKey(pg.K_RIGHT):
            headPart.moveRight()

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

