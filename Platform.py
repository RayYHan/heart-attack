import pygame, sys, Background, Monster, Fruit
from pygame.locals import *
from pygame.display import update
from random import randint

LBROWN = (204, 169, 116)
DBROWN = (123, 97, 46)

class Platform(pygame.sprite.Sprite):
    """In-game platform
    All in-game platforms are generated with this class from a 20X20 piece.
    Attributes:
        rect(Rect): a Rect variable that represents the dimension and position
            of the platform.
    """
    
    def __init__(self, size, pos):
        """ inits Platform with image, size and position.
        
        Args:
            size(int): Number of 20X20 pieces.
            pos(tuple): The position of the platform in relation to the game
                background.
        """
        
        pygame.sprite.Sprite.__init__(self)
        self._size = size
        self._image = pygame.Surface((self._size * 20, 20)).convert()
        #self._image = pygame.image.load('cement.png').convert()
        self.rect = Rect(pos[0], pos[1], size * 20, 20)
        self._startingX = self.rect.x
    
    def update(self, target):
        """ Updates and draws the platform to the game background.
        
        Args:
            target(pygame.Surface): The surface to draw the platform on.
        """
        platPiece = pygame.image.load('cement.png').convert()
        for i in range(0, self._size):
            self._image.blit(platPiece, (i * 20 ,0))
        target.blit(self._image, (self.rect.x, self.rect.y))
    
    def _drawPlatform(self):
        platSurf = pygame.Surface((20, 20)).convert()
        platSurf.fill(LBROWN)
        pygame.draw.rect(platSurf, DBROWN, (0, 0, 19, 19), 2)
        pygame.draw.rect(platSurf, DBROWN, (3, 3, 13, 13), 2)
        pygame.draw.rect(platSurf, DBROWN, (6, 6, 7, 7), 2)
        return platSurf
    
    def moveL(self):
        """Moves the platform to the right when the player moves to the left.
        """
        if self.rect.x < self._startingX:
            self.rect.x = self.rect.x + 15
        elif self.rect.x > self._startingX:
            self.rect.x = self._startingX
        
    def moveR(self):
        """Moves the platform to the left when the player moves to the right.
        """
        self.rect.x = self.rect.x - 15

class platformGroup:
    """Platform group class
    A group that contains all the in-game platforms and objects on the
        platforms.
    """
    def __init__(self):
        """Inits class platformGroup with platforms, monsters, fruits and 
        monster fireballs.
        """
        self._platformList = pygame.sprite.Group()
        self._monsterList = pygame.sprite.Group()
        self._fruitList = pygame.sprite.Group()
        self._fireballList = pygame.sprite.Group()
        
        self._platformList.add(Platform(40, (0, 580)))
        
        group1 = [[1000, 580, 40], [1250, 460, 5]#,
                  #[2000, 580, 40], [2200, 460, 5], [2600, 460, 5],
                  #[3000, 580, 40], [3200, 460, 5], [3600, 460, 5], 
                  #[3400, 360, 5]
                  ]
        for plat in group1:
            block = Platform(plat[2], (plat[0], plat[1]))
            if block._size > 10:
                monster = Monster.Monster1(block)
            self._platformList.add(block)
            self._monsterList.add(monster)
            
        group2 = [[2000, 580, 40]
                  #[4000, 580, 40],
                  #[5000, 580, 40],
                  #[6000, 580, 40]
                  ]
        for plat in group2:
            block = Platform(plat[2], (plat[0], plat[1]))
            if block._size > 10:
                monster = Monster.Monster2(block)
            self._platformList.add(block)
            self._monsterList.add(monster)
            
        group3 = [[3000, 580, 40], [3200, 460, 5], [3600, 460, 5]
                  #[7000, 580, 40], [7250, 460, 5],
                  #[8000, 580, 40], [8200, 460, 5], [8600, 460, 5],
                  #[9000, 580, 40], [9200, 460, 5], [9600, 460, 5], 
                  #[9400, 360, 5]
                  ]
        for plat in group3:
            block = Platform(plat[2], (plat[0], plat[1]))
            if block._size > 10:
                monster = Monster.Monster3(block)
            self._platformList.add(block)
            self._monsterList.add(monster)
        for plat in self._platformList:
            if plat._size < 10 and randint(0, 2) == 2:
                fruit = Fruit.Fruit(plat)
                self._fruitList.add(fruit)
                
        self.finalPlatform = Platform(40, (4000, 580))
        self._platformList.add(self.finalPlatform)
        #self._monsterList.empty()
        self.boss = Monster.Boss1(self.finalPlat())
        self._monsterList.add(self.boss)
        
                
    def update(self, target):
        """Updates and draws all the in-game objects on the screen.
        
        Args:
            target(pygame.Surface): The screen to draw objects to.
        """
        self._platformList.update(target)
        self._monsterList.update(target)
        self._fruitList.update(target)
        for mon in self._monsterList:
            if mon.__class__.__name__ == 'Monster3':
                for fire in mon.fireball():
                    self._fireballList.add(fire)
        if self.boss.isDead():
            block = Platform(5, (self.finalPlatform.rect.x + 700, 480))
            self._platformList.add(block)
            self.scroll = Fruit.Scroll(block)
            self._fruitList.add(self.scroll)
            
        
    def moveL(self):
        """Moves all the platforms to the right when player moves to the left.
        """
        for plat in self._platformList:
            plat.moveL()
            
    def moveR(self):
        """Moves all the platforms to the left when player moves to the right.
        """
        for plat in self._platformList:
            plat.moveR()
            
    def platList(self):
        """The getter function for the list contains all the platforms.
        
        Returns:
            pygame.Sprite.Group: A sprite group that contains all the platforms.
        """
        return self._platformList
    
    def monList(self):
        """The getter function for the list contains all the monsters.
        
        Returns:
            pygame.Sprite.Group: A sprite group that contains all the Monsters.
        """
        return self._monsterList
    
    def fruList(self):
        """The getter function for the list contains all the fruits.
        
        Returns:
            pygame.Sprite.Group: A sprite group that contains all the fruits.
        """
        return self._fruitList
    
    def fireList(self):
        """The getter function for the list contains all the fireballs.
        
        Returns:
            pygame.Sprite.Group: A sprite group that contains all the fireballs.
        """
        return self._fireballList
    
    def finalPlat(self):
        """The getter function for the final platforms.
        
        Returns:
            Platform: The last platform in the game.
        """
        return self.finalPlatform