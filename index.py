from game import game
from settings import *
import pygame as pg

# Game itself
def main():
    # Creates Snake #1
    game.createSnakePart('head', False)
    for snakePart in game.snakeParts:
        game.moveSnakePart(snakePart,snakePart.pos)

    # Adding first food
    game.createFood()
    
    # Active action loop
    while game.active:
        # Updates game state
        game.onUpdate()
        if not game.snakeAlive: gameOver()

        # Events
        headPart = game.snakeParts[0]

            # Quit
        if game.isQuit(): quit()

            # Changes snakes direction
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
            
        # Snakes' constant movement
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
        

        # Checks whether snakes are about to hit a wall
        for part in game.snakeParts:
            for food in game.foods:
                if game.checkRectalCollision(part.pos, food.pos):
                    lastSnakePart = game.snakeParts[-1]
                    game.foods.remove(food)
                    game.createSnakePart('body',lastSnakePart.prevMoveMoment, lastSnakePart.prevPos, pg.Vector2(lastSnakePart.prevVelocity))
                    game.createFood()

        # Draws elements
            # Draws the walls
        pg.draw.rect(game.screen, wallColor,game.topBorder)
        pg.draw.rect(game.screen, wallColor,game.bottomBorder)
        pg.draw.rect(game.screen, wallColor,game.leftBorder)
        pg.draw.rect(game.screen, wallColor,game.rightBorder)

            # Draws the rects if the setting is enabled
        rects = game.playfield.rects
        if drawPlayfieldRects:
            for col in rects:
                for rect in col:
                    pg.draw.rect(game.screen, wallColor,rect, 1)

            # Draws snakes' parts
        for snakePart in game.snakeParts:
            pg.draw.rect(game.screen, wallColor,snakePart, 5)

            # Draws foods
                # Draws regular foods
        for food in game.foods:
            pg.draw.rect(game.screen, foodColor, food.rect, 5)
                # Draws poisonous foods


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

