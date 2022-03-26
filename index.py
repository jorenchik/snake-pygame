from game import game, get_key, degrees, pl1Keys,pl2Keys
from settings import *
import pygame as pg

# Game itself
def main():
    # Creates Snake #1
    headPart = game.createSnakePart('head',0,game.player1Color,False)
    game.createSnakePart('tail',0,game.player1Color,False, (headPart.pos[0]-1,headPart.pos[1]))
    for snakePart in game.snakeParts: game.moveSnakePart(snakePart,snakePart.pos)

    # Creates Snake #2
    if game.multiplayer:
        headPart = game.createSnakePart('head',1,game.player2Color,False)
        game.createSnakePart('tail',1,game.player2Color,False, (headPart.pos[0]-1,headPart.pos[1]))
        for snakePart in game.snakeParts: game.moveSnakePart(snakePart,snakePart.pos)

    # Adding first food
    game.createFood(False)
    # Adding first poisonous food
    game.createFood(True)
    
    # Active action loop
    game.active = True
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
        score1Text = game.gameOverFont.render(f'P1 SCORE: {game.player1Score-1}', True, game.player1Color)
        game.screen.blit(score1Text, game.score1Pos)
        if game.multiplayer:
            score2Text = game.gameOverFont.render(f'P2 SCORE: {game.player2Score-1}', True, game.player2Color)
            game.screen.blit(score2Text, (game.score2Pos[0]-score2Text.get_width(), game.score2Pos[1]))

        # Events
        headParts = [x for x in game.snakeParts if x.type == 'head']
        if game.isQuit(): quit()

        # Dont move unsless movement button's been pressed
        if (game.isKey(pg.K_RIGHT) or game.isKey(pg.K_UP) or game.isKey(pg.K_LEFT) or game.isKey(pg.K_DOWN)) and headParts[0].velocity.length() == 0: 
            pg.time.set_timer(game.moveEvent, game.movementPeriod)
            game.setBaseVelocity()
        if game.multiplayer and (game.isKey(pg.K_d) or game.isKey(pg.K_w) or game.isKey(pg.K_a) or game.isKey(pg.K_s)) and headParts[0].velocity.length() == 0:
            pg.time.set_timer(game.moveEvent, game.movementPeriod)
            game.setBaseVelocity()

        # Changes snakes direction
        if not game.player1ChangedDir:
            for i,key in enumerate(pl1Keys):
                if game.isKey(key):
                    headParts[0].changeDirToAnAngle(degrees[i])
                    headParts[0].changedDirection = True
                    game.player1ChangedDir = True
        if not game.player1ChangedDir and game.multiplayer:
            for i,key in enumerate(pl2Keys):
                if game.isKey(key):
                    headParts[1].changeDirToAnAngle(degrees[i])
                    headParts[1].changedDirection = True
                    game.player2ChangedDir = True

        if game.isEvent(game.moveEvent):
            for headPart in headParts:
                for i, part in enumerate(headPart.relatedSnakeParts):
                    if part.movementPeriod and part.prevMoveMoment:
                        for food in game.foods:
                            if game.checkRectalCollision(part.pos, food.pos):
                                headPart.relatedSnakeParts = [x for x in game.snakeParts if x.snakeIndex == part.snakeIndex]
                                if food.type == 'food':
                                    lastSnakePart = headPart.relatedSnakeParts[-1]
                                    lastSnakePart.type = 'body'
                                    game.foods.remove(food)
                                    game.createSnakePart('tail',part.snakeIndex,part.color,lastSnakePart.prevMoveMoment, lastSnakePart.prevPos, pg.Vector2(lastSnakePart.prevVelocity))
                                if food.type == 'poison':
                                    lastSnakePart = headPart.relatedSnakeParts[-1]
                                    game.foods.remove(food)
                                    if len(headPart.relatedSnakeParts) > 2:
                                        game.snakeParts.remove(lastSnakePart)
                                        part.relatedSnakeParts.remove(lastSnakePart)
                                        headPart.relatedSnakeParts[-1].type = 'tail'

                                if len([x for x in game.foods if x.type == 'food']) > 0: game.createFood(True)
                                else: game.createFood(False)
                        if not selfRectalCollisionAllowed:
                            for i, part in enumerate(headPart.relatedSnakeParts):
                                # Passes if it is a head part
                                if part.type == 'head': continue
                                if game.checkRectalCollision(headPart.pos, part.pos): part.alive = False
                        if not otherRectalCollisionAllowed:  
                            unrelatedSnakeParts = [x for x in game.snakeParts if x not in headPart.relatedSnakeParts]
                            for unrelatedPart in unrelatedSnakeParts:
                                if game.checkRectalCollision(part.pos,unrelatedPart.pos): part.alive, unrelatedPart.alive = False, False
                

        # Snakes' constant movement
        if not game.isSnakeDead():
            if game.isEvent(game.moveEvent):
                for headPart in headParts:
                    headPart.getRelatedSnakeParts()
                    for i, part in enumerate(headPart.relatedSnakeParts):
                        part.prevPos, part.prevVelocity = (part.pos[0],part.pos[1]), pg.Vector2((part.velocity.x,part.velocity.y))
                        game.moveSnakePart(part,part.pos,part.velocity)
                        if part.type != 'head': part.velocity = pg.Vector2(headPart.relatedSnakeParts[i-1].prevVelocity)
                        if part.type == 'head':
                            part.changedDirection = False
                            if part.snakeIndex == 0:
                                game.player1ChangedDir = False
                            if part.snakeIndex == 1:
                                game.player2ChangedDir = False
            for headPart in headParts:
                headPart.getRelatedSnakeParts()
                for i, part in enumerate(headPart.relatedSnakeParts):
                    if part.type == 'head' and part.changedDirection == True: 
                        game.screen.blit(part.sprite, (part.rect.x, part.rect.y))
                        continue
                    if part.type == 'head':
                        part.getAngle().rotateSprite(part.angle)
                    else:
                        prevAngle = part.angle
                        part.getAngle()
                        if part.angle != prevAngle: part.rotateSprite(part.angle)
                        part.getAngle().rotateSprite(part.angle)
                    game.screen.blit(part.sprite, (part.rect.x, part.rect.y))

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
                for rect in col: pg.draw.rect(game.screen, wallColor,rect, 1)
        # Draws snakes' part hitboxes if visible
        if hitboxesVisible:
            for part in game.snakeParts: pg.draw.rect(game.screen, part.color,part, 5)
        # Draws foods
        for food in game.foods: game.screen.blit(food.sprite, (food.rect.x, food.rect.y))
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
        colorPlayer1Btn = game.createMenuItem(f'PLAYER 1 COLOR: {get_key(game.player1Color, snakeColors).upper()}')
        if game.multiplayer:
            if(game.player1Color == game.player2Color): game.getPlayerNextColor(1)
            colorPlayer2Btn = game.createMenuItem(f'PLAYER 2 COLOR: {get_key(game.player2Color, snakeColors).upper()}')
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

