import pygame, sys, Background, Platform, Player, Monster
from pygame.locals import *
from turtledemo.nim import SCREENWIDTH

def main():
    """The main game function that contains all the game attributes and the
        main game loop.
    """
    pygame.init()
    FPS = 30
    fps_clock = pygame.time.Clock()
    
    SCREENSIZE = (800, 600)
    
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("Journey to the West")
    
    pygame.mouse.set_visible(False)
    
    background = Background.Background((800, 600))
    platform = Platform.platformGroup()
    player = Player.Player((-100, 0))
    
    moveL = False
    moveR = False
    
    gameIdle =True
    gameContinue = True
    gamePause = False
    gamePrompt = 0
    
    endGameCounter = 100
    
    pygame.mixer.music.load('bg.ogg')
    pygame.mixer.music.set_endevent(USEREVENT)
    pygame.mixer.music.play()
    
    fullscreen = False
    
    fileCount = 1
    
    while True:
#         fileName = 'screen' + str(fileCount) + '.jpg'
#         fileCount = fileCount + 1
#         if fileCount % 10 == 1:
#             pygame.image.save(screen, fileName)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == USEREVENT:
                    pygame.mixer.music.play()
            if (event.type == KEYDOWN and event.key == K_RETURN and 
                (pygame.key.get_mods() & KMOD_ALT)):
                if fullscreen:
                    fullscreen = False
                    screen = pygame.display.set_mode(SCREENSIZE)
                else:
                    fullscreen = True
                    screen = pygame.display.set_mode(SCREENSIZE, FULLSCREEN)
            if gameContinue:
                gamePrompt = player.prompt
                if gameIdle:
                    if event.type == KEYDOWN and event.key == K_RETURN:
                        gameIdle = False
                        player.unhideHeart()
                elif gamePause:
                    if event.type == KEYDOWN:
                        if event.key == K_p:
                            gamePause = False
                        if event.key == K_q:
                            pygame.quit()
                            sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_EQUALS:
                            player.increaseHealth()
                        if event.key == K_RIGHT:
                            moveR = True
                        if event.key == K_LEFT:
                            moveL = True
                        if event.key == K_SPACE:
                            player.jump()
                        if event.key == K_p:
                            gamePause = True
                        if event.key == K_RETURN:
                            if gamePrompt != 0:
                                gamePrompt = 0
                                player.prompt = 0
                    if event.type == KEYUP:
                        if event.key == K_RIGHT:
                            moveR = False
                        if event.key == K_LEFT:
                            moveL = False
            else:
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        background = Background.Background((800, 600))
                        platform = Platform.platformGroup()
                        player = Player.Player((150, 200))
                        gameContinue = True
                        moveL = False
                        moveR = False
                    if event.key == K_q:
                        pygame.quit()
                        sys.exit()
        
        if gameContinue:
            if gameIdle:
                player.hideHeart()
                player.land(platform.platList(), Platform.Platform(1, (13000, 3)))
                background.update(screen)
                player.update(screen)
                demo(screen)
                platform.update(screen)
                if not player.moveR():
                    background.moveR()
            elif gamePause:
                #prompt('cigar', screen)
                pause(screen)
                
            elif gamePrompt != 0:
                if gamePrompt == 1:
                    prompt('fat', screen)
                elif gamePrompt == 2:
                    prompt('salt', screen)
                elif gamePrompt == 3:
                    prompt('cigar', screen)
                elif gamePrompt == 4:
                    prompt('couch', screen)
            else:
                if moveL:
                    player.moveL()
                if moveR:
                    if not player.moveR():
                        background.moveR()
                        platform.moveR()
                        screen.fill((0, 0, 0))
                player.land(platform.platList(), platform.finalPlat())
                player.enemyCollision(platform.monList())
                player.fruitCollison(platform.fruList())
                player.fireballCollison(platform.fireList())
                if player.gameOver() or player.win():
                    gameContinue = False
                background.update(screen)
                platform.update(screen)
                player.update(screen)
        else:
            if endGameCounter == 0:
                gameIdle = True
                background = Background.Background((800, 600))
                platform = Platform.platformGroup()
                player = Player.Player((150, 200))
                gameContinue = True
                moveL = False
                moveR = False
                endGameCounter = 100
            else: endGameCounter -= 1
            if player.win():
                gameWon(screen)
            else:
                gameOver(screen)
 
        pygame.display.update()
        fps_clock.tick(FPS)
    
def demo(target):
    """Displays the starting screen of the game.
    
    Args:
        target(pygame.Surface): The surface to draw starting screen onto.
    """
    font1 = pygame.font.SysFont('Chinese Takeaway', 70, 5, False)
    font2 = pygame.font.SysFont('Chinese Takeaway', 20, 5, False)
    label1 = pygame.image.load('jtw.png')
    label2 = font2.render('Press <- or -> to move, space to jump', True, (125, 125, 125))
    label3 = font2.render('Press ENTER to start', True, (0, 0, 255))
    target.blit(label1, (80, 150))
    target.blit(label2, (100, 350))
    target.blit(label3, (100, 380))
    
def prompt(item, target):
    if item == 'cigar':
        promptImg = pygame.image.load('cigarp.png').convert_alpha()
    elif item == 'fat':
        promptImg = pygame.image.load('fatp.png').convert_alpha()
    elif item == 'salt':
        promptImg = pygame.image.load('saltp.png').convert_alpha()
    elif item == 'couch':
        promptImg = pygame.image.load('couchp.png').convert_alpha()
    target.blit(promptImg, (100, 100))
    
def pause(target):
    """Displays the pause screen of the game.
    
    Args:
        target(pygame.Surface): The surface to draw pause screen onto.
    """
    font1 = pygame.font.SysFont('Chinese Takeaway', 40, 5, False)
    font2 = pygame.font.SysFont('Chinese Takeaway', 20, 5, False)
    label = font1.render('GAME PAUSED', True, (0, 255, 0))
    label2 = font2.render('Press P to resume', True, (0, 0, 255))
    label3 = font2.render('Press Q to quit', True, (0, 0, 255))
    target.blit(label, (100, 300))
    target.blit(label2, (100, 350))
    target.blit(label3, (100, 375))

def gameOver(target):
    """Displays the gameOver screen of the game.
    
    Args:
        target(pygame.Surface): The surface to draw gameOver screen onto.
    """
    font1 = pygame.font.SysFont('Chinese Takeaway', 40, 5, False)
    font2 = pygame.font.SysFont('Chinese Takeaway', 20, 5, False)
    label = font1.render('GAME OVER', True, (0, 255, 0))
    label2 = font2.render('Press R to restart', True, (0, 0, 255))
    label3 = font2.render('Press Q to quit', True, (0, 0, 255))
    target.blit(label, (100, 300))
    target.blit(label2, (100, 350))
    target.blit(label3, (100, 375))
    
def gameWon(target):
    """Displays the winning screen of the game.
    
    Args:
        target(pygame.Surface): The surface to draw winning screen onto.
    """
    font1 = pygame.font.SysFont('Chinese Takeaway', 40, 5, False)
    font2 = pygame.font.SysFont('Chinese Takeaway', 20, 5, False)
    label = font1.render('YOU WIN', True, (0, 255, 0))
    label2 = font2.render('Press R to restart', True, (0, 0, 255))
    label3 = font2.render('Press Q to quit', True, (0, 0, 255))
    target.blit(label, (100, 300))
    target.blit(label2, (100, 350))
    target.blit(label3, (100, 375))

if __name__ == '__main__':
    main()