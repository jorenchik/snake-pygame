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

        for part in game.snakeParts:
            for food in game.foods:
                if game.checkRectalCollision(part.pos, food.pos):
                    lastSnakePart = game.snakeParts[-1]
                    game.foods.remove(food)
                    game.createSnakePart('body',lastSnakePart.prevMoveMoment, lastSnakePart.prevPos, lastSnakePart.prevVelocity)
                
        for i, part in enumerate(game.snakeParts):
            if part.movementPeriod:
                part.prevPos = part.pos
                part.prevVelocity = part.velocity
                if part.prevMoveMoment:
                    if (game.now - part.prevMoveMoment) >= part.movementPeriod:
                        game.moveSnakePart(part,part.pos,part.velocity)
                else:
                    game.moveSnakePart(part,part.pos,part.velocity)
            else: game.moveSnakePart(part,part.pos,part.velocity)
            
            
        # for part in game.snakeParts:
        #     print(part.velocity)

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

        # Draw foods
        for food in game.foods:
            pg.draw.rect(game.screen, foodColor, food.rect, 5)
    

        # for part in game.snakeParts:
        #     print(part.prevMoveMoment)
        game.update()
main()

