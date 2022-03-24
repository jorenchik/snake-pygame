from turtle import back

from matplotlib.style import available
from game import game, get_key
from settings import *
import pygame as pg

# Game itself
def main():

    # Creates Snake #1
    game.createSnakePart('head',0,game.player1Color,False)
    for snakePart in game.snakeParts:
        game.moveSnakePart(snakePart,snakePart.pos)

    # Creates Snake #2
    if game.multiplayer:
        game.createSnakePart('head',1,game.player2Color,False)
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
        score1Text = game.gameOverFont.render(f'P1 SCORE: {game.player1Score}', True, game.player1Color)
        game.screen.blit(score1Text, game.score1Pos)
        if game.multiplayer:
            score2Text = game.gameOverFont.render(f'P2 SCORE: {game.player2Score}', True, game.player2Color)
            game.screen.blit(score2Text, (game.score2Pos[0]-score2Text.get_width(), game.score2Pos[1]))


        # Events
        headParts = [x for x in game.snakeParts if x.type == 'head']
            # Quit
        if game.isQuit(): quit()

        # Dont move unsless movement button's been pressed
        if (game.isKey(pg.K_RIGHT) or game.isKey(pg.K_UP) or game.isKey(pg.K_LEFT) or game.isKey(pg.K_DOWN)) and headParts[0].velocity.length() == 0: game.setBaseVelocity()
        if game.multiplayer:
            if (game.isKey(pg.K_d) or game.isKey(pg.K_w) or game.isKey(pg.K_a) or game.isKey(pg.K_s)) and headParts[0].velocity.length() == 0: game.setBaseVelocity()

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
            if game.multiplayer:
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
            headPart.getRelatedSnakeParts()
            for i, part in enumerate(headPart.relatedSnakeParts):
                if part.movementPeriod:
                    part.prevPos = part.pos
                    part.prevVelocity = part.velocity
                    if part.prevMoveMoment:
                        if (game.now - part.prevMoveMoment) >= part.movementPeriod*game.dt:
                            game.moveSnakePart(part,part.pos,part.velocity)
                            if part.type != 'head':
                                part.velocity = pg.Vector2(headPart.relatedSnakeParts[i-1].prevVelocity)
                            
                    else:
                        game.moveSnakePart(part,part.pos,part.velocity)
                else: game.moveSnakePart(part,part.pos,part.velocity)
        
        # Checks if snake's head has the same position with a food
        for headPart in headParts:
            headPart.getRelatedSnakeParts()
            for i, part in enumerate(headPart.relatedSnakeParts):
                for food in game.foods:
                    if game.checkRectalCollision(part.pos, food.pos):
                        headPart.relatedSnakeParts = [x for x in game.snakeParts if x.snakeIndex == part.snakeIndex]
                        if food.type == 'food':
                            lastSnakePart = headPart.relatedSnakeParts[-1]
                            game.foods.remove(food)
                            game.createSnakePart('body',part.snakeIndex,part.color,lastSnakePart.prevMoveMoment, lastSnakePart.prevPos, pg.Vector2(lastSnakePart.prevVelocity))
                        if food.type == 'poison':
                            lastSnakePart = headPart.relatedSnakeParts[-1]
                            game.foods.remove(food)
                            if len(headPart.relatedSnakeParts) > 1:
                                game.snakeParts.remove(lastSnakePart)
                        if len([x for x in game.foods if x.type == 'food']) > 0:
                            game.createFood(True)
                        else:
                            game.createFood(False)
        # Checks whether any part of a snake hits another
        if not otherRectalCollisionAllowed:      
            for headPart in headParts:
                headPart.getRelatedSnakeParts()
                for i, part in enumerate(headPart.relatedSnakeParts):
                    unrelatedSnakeParts = [x for x in game.snakeParts if x not in headPart.relatedSnakeParts]
                    for unrelatedPart in unrelatedSnakeParts:
                        if game.checkRectalCollision(part.pos,unrelatedPart.pos):
                            part.alive = False
                            unrelatedPart.alive = False
        # Checks whether any part of a snake hits itself
        if not selfRectalCollisionAllowed:
            for headPart in headParts:
                headPart.getRelatedSnakeParts()
                for i, part in enumerate(headPart.relatedSnakeParts):
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
        # for part in game.snakeParts:
        #     # pg.draw.rect(game.screen, part.color,part, 5)
        #     game.screen.blit(part.sprite, (part.rect.x, part.rect.y))

            # Draws foods
                # Draws regular foods
        for food in game.foods:
            if food.type == 'food':
                pg.draw.rect(game.screen, foodColor, food.rect, 5)
            else:
                pg.draw.rect(game.screen, poisonousFoodColor, food.rect, 5)
                # Draws poisonous foods

        # End of the update
        for headPart in headParts:
            for i, part in enumerate(headPart.relatedSnakeParts):
                part.getAngle().rotateSprite(part.angle)
                game.screen.blit(part.sprite, (part.rect.x, part.rect.y))
        game.update()

# Game restart/quit screen
def gameOver():
    while True:
        game.onUpdate().setBackground()
        text = game.gameOverFont.render('GAME OVER | PRESS ANY KEY TO RETURN TO MAIN MENU', True, white)
        game.screen.blit(text, (game.SCREEN_WIDTH/2-text.get_width()/2, game.SCREEN_HEIGHT/2-text.get_height()/2))
        if game.isQuit(): quit()
        if game.isAnyKey(): break
        game.update()

def gameMenu():
    game.menuPointingTo = 0
    while True:
        game.onUpdate().setBackground()
        menuItems = []
        startBtn = game.createMenuItem('START')
        settingsBtn = game.createMenuItem('SETTINGS')
        exitBtn = game.createMenuItem('EXIT')
        menuItems.extend([startBtn, settingsBtn, exitBtn])
        game.showMenuItems(menuItems)
        if game.isKey(pg.K_UP):
            if game.menuPointingTo == 0: game.menuPointingTo = len(menuItems)-1
            else: game.menuPointingTo -= 1
        if game.isKey(pg.K_DOWN):
            if game.menuPointingTo == len(menuItems)-1: game.menuPointingTo = 0
            else: game.menuPointingTo += 1
        if game.isKey(pg.K_RETURN) and game.menuPointingTo == menuItems.index(startBtn): break
        if game.isKey(pg.K_RETURN) and game.menuPointingTo == menuItems.index(settingsBtn): 
            settingsMenu()
            game.menuPointingTo = 0
        if game.isKey(pg.K_RETURN) and game.menuPointingTo == menuItems.index(exitBtn): exit()
        game.update()

def settingsMenu():
    game.menuPointingTo = 0
    while True:
        game.onUpdate().setBackground()
        menuItems = []
        wallMode = game.createMenuItem(f'WALL MODE: {"PORTAL" if game.portalWalls else "REGULAR"}')
        multiplayerOn = game.createMenuItem(f'MODE: {"1 PLAYER" if not game.multiplayer else "2 PLAEYRS"}')
        colorPlayer1Btn = game.createMenuItem(f'PLAYER 1 COLOR: {get_key(game.player1Color, colors).upper()}')
        if game.multiplayer:
            colorPlayer2Btn = game.createMenuItem(f'PLAYER 2 COLOR: {get_key(game.player2Color, colors).upper()}')
        backBtn = game.createMenuItem('BACK')
        menuItems.extend([wallMode, multiplayerOn,colorPlayer1Btn])
        if game.multiplayer:
            menuItems.append(colorPlayer2Btn)
        menuItems.append(backBtn)
        game.showMenuItems(menuItems)
        if game.isKey(pg.K_UP):
            if game.menuPointingTo == 0: game.menuPointingTo = len(menuItems)-1
            else: game.menuPointingTo -= 1
        if game.isKey(pg.K_DOWN):
            if game.menuPointingTo == len(menuItems)-1: game.menuPointingTo = 0
            else: game.menuPointingTo += 1
        if game.isKey(pg.K_RETURN) and game.menuPointingTo == menuItems.index(colorPlayer1Btn):
            game.getPlayerNextColor(0)
        if game.isKey(pg.K_RETURN) and game.menuPointingTo == menuItems.index(wallMode): 
            game.portalWalls = not game.portalWalls
        if game.multiplayer:
            if game.isKey(pg.K_RETURN) and game.menuPointingTo == menuItems.index(colorPlayer2Btn): 
                game.getPlayerNextColor(1)
        if game.isKey(pg.K_RETURN) and game.menuPointingTo == menuItems.index(multiplayerOn): 
            game.multiplayer = not game.multiplayer
        if game.isKey(pg.K_RETURN) and game.menuPointingTo == menuItems.index(backBtn): break
        game.update()

# Starting the game's main loop
while True:
    gameMenu()
    main()

