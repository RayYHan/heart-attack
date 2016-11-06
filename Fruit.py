import pygame, sys
from pygame.locals import *
from random import randint

class Fruit(pygame.sprite.Sprite):
    """Edible fruit
    Fruit is an edible object that will replenish the player's lost health.
    
    Attributes:
        rect(Rect): The Rect representation of Fruit's dimension and position.
    """
    def __init__(self, plat):
        """Inits Fruit with dimension, position and bounding Platform.
        
        Args:
            plat(Platform): The bounding platform for Fruit.
        """
        pygame.sprite.Sprite.__init__(self)
        self._plat = plat
        if randint(0, 1):
            self._image = pygame.image.load('peach.png').convert_alpha()
        else:
            self._image = pygame.image.load('banana.png').convert_alpha()
        self._xFromPlat = plat.rect[2]//2 - 15
        self._yFromPlat = - 50
        self.rect = self._image.get_rect()
        self.rect.x = self._plat.rect.x + self._xFromPlat
        self.rect.y = self._plat.rect.y + self._yFromPlat
        
    def update(self, target):
        """Updates and draw Fruit onto game screen.
        
        Args:
            target(pygame.Surface): The surface to draw Fruit onto.
        """
        pygame.sprite.Sprite.update(self)
        self.rect.x = self._plat.rect.x + self._xFromPlat
        self.rect.y = self._plat.rect.y + self._yFromPlat
        target.blit(self._image, (self.rect.x, self.rect.y))
        
class Cigar(Fruit):
    def __init__(self, plat):
        Fruit.__init__(self, plat)
        self._image = pygame.image.load('cigar.png').convert_alpha()
        self.name = 'cigar'
        
class Scroll(Fruit):
    """The end level item.
    Scroll is the item that is required to complete a level.
    Attributes:
        rect(Rect): The Rect representation of Fruit's dimension and position.
    """
    def __init__(self, plat):
        """Inits Scroll with dimension, position and bounding Platform.
        
        Args:
            plat(Platform): The bounding platform for Scroll.
        """
        self.name = 'scroll'
        Fruit.__init__(self, plat)
        self._image = pygame.image.load('scroll.png').convert_alpha()
        self._xFromPlat = plat.rect[2]//2 - 19
        self._yFromPlat = - 70
        self.rect = self._image.get_rect()
        self.rect.x = self._plat.rect.x + self._xFromPlat
        self.rect.y = self._plat.rect.y + self._yFromPlat