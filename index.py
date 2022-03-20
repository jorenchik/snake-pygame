from game import game
from settings import *
import pygame as pg

# Game itself
def main():
    # Creates Snake #1
    game.createSnakePart('head',0,player1Color,False)
    for snakePart in game.snakeParts:
        game.moveSnakePart(snakePart,snakePart.pos)

    # Creates Snake #2
    if multiplayer:
        game.createSnakePart('head',1,player2Color,False)
        for snakePart in game.snakeParts:
            game.moveSnakePart(snakePart,snakePart.pos)

    # Adding first food
    game.createFood(False)
    # Adding first poisonous food
    game.createFood(True)
    
    game.active = True
    # Active action loop
    while game.active:
        # Updates game state
        game.onUpdate()
        if game.isSnakeDead():
            game.snakeParts.clear()
            game.foods.clear()
            gameOver()
            break

        game.getPlayersScore()
        # Add score text
        score1Text = game.gameOverFont.render(f'P1 SCORE: {game.player1Score}', True, player1Color)
        game.screen.blit(score1Text, game.score1Pos)

        if multiplayer:
            score2Text = game.gameOverFont.render(f'P2 SCORE: {game.player2Score}', True, player2Color)
            game.screen.blit(score2Text, (game.score2Pos[0]-score2Text.get_width(), game.score2Pos[1]))


        # Events
        headParts = [x for x in game.snakeParts if x.type == 'head']
            # Quit
        if game.isQuit(): quit()

            # Changes snakes direction
        if (not game.previousDirChange or game.now - game.previousDirChange >= headParts[0].movementPeriod/2):
            if game.isKey(pg.K_RIGHT):
                headParts[0].changeDirToAnAngle(0)
                game.previousDirChange = game.now
            if game.isKey(pg.K_UP):
                headParts[0].changeDirToAnAngle(90)
                game.previousDirChange = game.now
            if game.isKey(pg.K_LEFT):
                headParts[0].changeDirToAnAngle(180)
                game.previousDirChange = game.now
            if game.isKey(pg.K_DOWN):
                headParts[0].changeDirToAnAngle(270)
                game.previousDirChange = game.now
            if multiplayer:
                if game.isKey(pg.K_d):
                    headParts[1].changeDirToAnAngle(0)
                    game.previousDirChange = game.now
                if game.isKey(pg.K_w):
                    headParts[1].changeDirToAnAngle(90)
                    game.previousDirChange = game.now
                if game.isKey(pg.K_a):
                    headParts[1].changeDirToAnAngle(180)
                    game.previousDirChange = game.now
                if game.isKey(pg.K_s):
                    headParts[1].changeDirToAnAngle(270)
                    game.previousDirChange = game.now
                
        # Snakes' constant movement
        for headPart in headParts:
            relatedSnakeParts = headPart.getRelatedSnakeParts()
            for i, part in enumerate(relatedSnakeParts):
                if part.movementPeriod:
                    part.prevPos = part.pos
                    part.prevVelocity = part.velocity
                    if part.prevMoveMoment:
                        if (game.now - part.prevMoveMoment) >= part.movementPeriod:
                            game.moveSnakePart(part,part.pos,part.velocity)
                            if part.type != 'head':
                                part.velocity = pg.Vector2(relatedSnakeParts[i-1].prevVelocity)
                    else:
                        game.moveSnakePart(part,part.pos,part.velocity)
                else: game.moveSnakePart(part,part.pos,part.velocity)
        

        # Checks if snake's head has the same position with a food
        for headPart in headParts:
            relatedSnakeParts = headPart.getRelatedSnakeParts()
            for i, part in enumerate(relatedSnakeParts):
                for food in game.foods:
                    if game.checkRectalCollision(part.pos, food.pos):
                        relatedSnakeParts = [x for x in game.snakeParts if x.snakeIndex == part.snakeIndex]
                        lastSnakePart = relatedSnakeParts[-1]
                        game.foods.remove(food)
                        game.createSnakePart('body',part.snakeIndex,part.color,lastSnakePart.prevMoveMoment, lastSnakePart.prevPos, pg.Vector2(lastSnakePart.prevVelocity))
                        game.createFood(False)


        # Checks whether any part of a snake hits another
        if not otherRectalCollisionAllowed:      
            for headPart in headParts:
                relatedSnakeParts = headPart.getRelatedSnakeParts()
                for i, part in enumerate(relatedSnakeParts):
                    unrelatedSnakeParts = [x for x in game.snakeParts if x not in relatedSnakeParts]
                    for unrelatedPart in unrelatedSnakeParts:
                        if game.checkRectalCollision(part.pos,unrelatedPart.pos):
                            part.alive = False
                            unrelatedPart.alive = False

        # Checks whether any part of a snake hits itself
        if not selfRectalCollisionAllowed:
            for headPart in headParts:
                relatedSnakeParts = headPart.getRelatedSnakeParts()
                for i, part in enumerate(relatedSnakeParts):
                    # Passes if it is a head part
                    if part.type == 'head': continue
                    if game.checkRectalCollision(headPart.pos, part.pos):
                        part.alive = False
                

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
        for part in game.snakeParts:
            pg.draw.rect(game.screen, part.color,part, 5)

            # Draws foods
                # Draws regular foods
        for food in game.foods:
            if food.type == 'food':
                pg.draw.rect(game.screen, foodColor, food.rect, 5)
            else:
                pg.draw.rect(game.screen, poisonousFoodColor, food.rect, 5)
                # Draws poisonous foods


        # End of the update
        game.update()

# Game restart/quit screen
def gameOver():
    while True:
        game.onUpdate()
        game.setBackground()
        text = game.gameOverFont.render('GAME OVER | PRESS SPACE TO RESTART | PRESS ESCAPE TO EXIT', True, white)
        game.screen.blit(text, (game.SCREEN_WIDTH/2-text.get_width()/2, game.SCREEN_HEIGHT/2-text.get_height()/2))
        if game.isQuit(): quit()
        if game.isKey(pg.K_SPACE):
            break
        game.update()
# Starting the game's main loop
while True: main()

