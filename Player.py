import pygame, sys
from pygame.locals import *

GREY = (123, 123, 123)

class Player(pygame.sprite.Sprite):
    """Game player
    Player is the character controlled by the game player.
    
    Attributes:
        rect(Rect): The Rect representation of Player's dimension and position.
    """
    def __init__(self, pos):
        """Inits Player with images, dimension, position and other attributes.
        """
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.image.load('king.png').convert_alpha()
        self._hurtImage = pygame.image.load('kinghurt.png').convert_alpha()
        self._heartImage = pygame.image.load('heart.png').convert_alpha()
        self.rect = self._image.get_rect()
        (self.rect.x, self.rect.y) = pos
        self._life = 5
        self._grounded = False
        self._gravity = 0
        self._jumping = 0
        self._dieCounter = 0
        self._yOffset = 0
        self._bouncing = 0
        self._onFinalPlatform = False
        self._won = False
        self._showHeart = True
        self._dir = 0;
        self.prompt = 0;
    
    def update(self, target):
        """Updates and draw Player onto game screen.
        
        Args:
            target(pygame.Surface): The surface to draw Player onto.
        """
        pygame.sprite.Sprite.update(self)
        self._bounce()
        if self._dir == 0:
            self._hurtImage = pygame.image.load('kinghurt.png').convert_alpha()
        else:
            self._hurtImage = pygame.image.load('kinghurtr.png').convert_alpha()
        if self._showHeart:
            for i in range(0, self._life):
                target.blit(self._heartImage, (10 + i * 40, 10))
        if self._jumping != 0:
            self.rect.y -= 20
            self._jumping -= 1
        self._fall()
        if self._dieCounter > 0: self._dieCounter -= 1
        if self._dir == 0:
            self._image = pygame.image.load('king.png').convert_alpha()
        else:
            self._image = pygame.image.load('kingr.png').convert_alpha()
        if self._dieCounter % 3 == 0:
            target.blit(self._image, (self.rect.x, self.rect.y + self._yOffset))
        else:
            target.blit(self._hurtImage, (self.rect.x, self.rect.y + 
                                          self._yOffset))
        
    def _bounce(self):
        if self._bouncing == 0: self._bouncing = 10
        if self._bouncing > 5:
            self._yOffset -= 2
            self._bouncing -= 1
        elif self._bouncing >0:
            self._yOffset += 2
            self._bouncing -=1
    
    def jump(self):
        """Handles the actions for Player to jump
        """
        if self._grounded: self._jumping = 7
    
    def _fall(self):
        if not self._grounded: self._gravity += 1
        else: self._gravity = 0
        self.rect.y += self._gravity
        if self.rect.y > 700:
            self.die()
        
    def land(self, spriteList, finalPlat):
        """Checks if Player is landed on a Platform. If so, checks whether it's
            a regular Platform or the finalPlatform.
            
        Args:
            spriteList(pygame.Sprite.Group): The sprite group that contains all
                the Platforms.
            finalPlat(Platform): The finalPlatform.
        """
        collidList = pygame.sprite.spritecollide(self, spriteList, False)
        if len(collidList) == 0: self._grounded = False
        else:
            for block in collidList:
                if self.rect.y < block.rect.y - 70:
                    self.rect.y = block.rect.y - 94
                    self._grounded = True
                if block == finalPlat and block.rect.x <= 0:
                    block.rect.x = 0
                    self._onFinalPlatform = True
        
    def enemyCollision(self, enemyList):
        """Checks whether Player has collided with an enemy. If so, checks the
            collision side to determine damage recipient.
            
        Args:
            enemyList(pygame.Sprite.Group): The sprite group that contains all
                Monsters and Bosses.
        """
        collidList = pygame.sprite.spritecollide(self, enemyList, False)
        if len(collidList) != 0:
            for enemy in collidList:
                self.prompt = enemy._name
                self.die()
                enemy.die()
#                 if self.rect.y + 70 < enemy.rect.y: 
#                     enemy.die()
#                     self._jumping = 3
#                 else:
#                     if self._dieCounter == 0:
#                         self.die()
                    
    def fruitCollison(self, fruList):
        """Checks whether Player has collided with a Fruit and whether Player 
        has lost health point(s). If both are true, replenishes Player's health.
        
        Args:
            fuitList(pygame.Sprite.Group): The group that contains all Fruits.
        """
        collidList = pygame.sprite.spritecollide(self, fruList, True)
        if len(collidList) > 0:
            if self._onFinalPlatform:
                self._won = True
            elif self._life < 5:
                self._life += 1
                
    def fireballCollison(self, fireList):
        """Checks whether Player has collided with a Fireball. If so, Player
            receives damage.
            
        Args: fireList(pygame.Sprite.Group): The group that contains all 
            Fireballs.
        """
        collidList = pygame.sprite.spritecollide(self, fireList, True)
        if len(collidList) > 0:
            self.die()
    
    def moveL(self):
        """Moves the player to the left.
        
        Returns:
            bool: True if Player moves, False otherwise.
        """
        self._dir = 1
        if self.rect.x > 0:
            self.rect.x -= 10
            return True
        else:
            self.rect.x = 0
            return False
            
    def moveR(self):
        """Moves the player to the right.
        
        Returns:
            bool: True if Player moves, False otherwise.
        """
        self._dir = 0
        if self.rect.x < 350 or self._onFinalPlatform:
            if self.rect.x < 800 - 65:
                self.rect.x += 10
            return True
        else:
            self.rect.x = 350
            return False
        
    def die(self):
        """Receives damage to the player.
        """
        self._life -= 1
        self._dieCounter = 30
        
    def gameOver(self):
        """Checks whether Player health is depleted
        
        Return:
            bool: True is Player is out of health, False otherwise.
        """
        if self._life < 0: self._life = 0
        return not self._life
    
    def win(self):
        """Checks if Player has won the current level.
        
        Return:
            bool: True is Player has won, False otherwise.
        """
        return self._won
    
    def hideHeart(self):
        """Hides Player's health points from display.
        """
        self._showHeart = False
    
    def unhideHeart(self):
        """Unhides Player's health points from display.
        """
        self._showHeart = True
        
    def increaseHealth(self):
        """Increases Player health by 1
        """
        self._life += 1;
        