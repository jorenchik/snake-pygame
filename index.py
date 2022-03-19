from game import game, Game, Playfield, gameIcon
from settings import *
import pygame as pg

# Game itself
def main():
    game.createSnakePart('head', False)
    for snakePart in game.snakeParts:
        game.moveSnakePart(snakePart,snakePart.pos)

    # Adding first food
    game.createFood()
    
    # Active action loop
    while game.active:
        # Game state update
        game.onUpdate()
        if not game.snakeAlive: gameOver()

        # Events
        headPart = game.snakeParts[0]

            # Quit
        if game.isQuit(): quit()

            # Change snakes direction
        if (not game.previousDirChange or game.now - game.previousDirChange >= headPart.movementPeriod/2):
            if game.isKey(pg.K_RIGHT):
                headPart.changeDirToAnAngle(0)
                game.previousDirChange = game.now
            if game.isKey(pg.K_UP):
                headPart.changeDirToAnAngle(90)
                game.previousDirChange = game.now
            if game.isKey(pg.K_LEFT):
                headPart.changeDirToAnAngle(180)
                game.previousDirChange = game.now
            if game.isKey(pg.K_DOWN):
                headPart.changeDirToAnAngle(270)
                game.previousDirChange = game.now
            
            

        for i, part in enumerate(game.snakeParts):
            if part.movementPeriod:
                part.prevPos = part.pos
                part.prevVelocity = part.velocity
                if part.prevMoveMoment:
                    if (game.now - part.prevMoveMoment) >= part.movementPeriod:
                        game.moveSnakePart(part,part.pos,part.velocity)
                        if part.type != 'head':
                            part.velocity = pg.Vector2(game.snakeParts[i-1].prevVelocity)
                else:
                    game.moveSnakePart(part,part.pos,part.velocity)
            else: game.moveSnakePart(part,part.pos,part.velocity)
        
        for part in game.snakeParts:
            for food in game.foods:
                if game.checkRectalCollision(part.pos, food.pos):
                    lastSnakePart = game.snakeParts[-1]
                    game.foods.remove(food)
                    game.createSnakePart('body',lastSnakePart.prevMoveMoment, lastSnakePart.prevPos, pg.Vector2(lastSnakePart.prevVelocity))
                    game.createFood()

        # Draw the walls
        pg.draw.rect(game.screen, wallColor,game.topBorder)
        pg.draw.rect(game.screen, wallColor,game.bottomBorder)
        pg.draw.rect(game.screen, wallColor,game.leftBorder)
        pg.draw.rect(game.screen, wallColor,game.rightBorder)

        # Draw the rects
        rects = game.playfield.rects
        if drawPlayfieldRects:
            for col in rects:
                for rect in col:
                    pg.draw.rect(game.screen, wallColor,rect, 1)

        # Draw snake parts
        for snakePart in game.snakeParts:
            pg.draw.rect(game.screen, wallColor,snakePart, 5)

        # Draw foods
        for food in game.foods:
            pg.draw.rect(game.screen, foodColor, food.rect, 5)

        # End of the update
        game.update()

# Game restart/quit screen
def gameOver():
    while not game.snakeAlive:
        game.onUpdate()
        game.setBackground()
        if game.isQuit(): quit()
        game.update()

# Starting the game's main loop
main()

