import pygame, sys
from pygame.locals import *
from random import randint, random

RED = (255, 0, 0)

class Monster(pygame.sprite.Sprite):
    """Monster base class.
    The class contains the basic functions that are shared by all monster
        classes.
    Attributes:
        rect(Rect): The dimension and position of the class.
    """
    def __init__(self, plat):
        """Inits Monster with image, size, position, bounding platform, moving
            direction and sound effect.
            
        Args:
            plat(Platform): The platform to bound the Monster to.
        """
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.Surface((25, 50)).convert()
        self._image.fill(RED)
        self.rect = self._image.get_rect()
        self._plat = plat
        self.rect.x = plat.rect.x + plat.rect[2] - 60
        self.rect.y = plat.rect.y - 50
        self._xFromPlat = plat.rect[2] - 60
        self._yFromPlat = - 50
        self._movingDir = 1
        self._yOffset = 0
        self._bouncing = 0
        self._dieSound = pygame.mixer.Sound('pop.ogg')
        
    def update(self, target):
        """Updates and draws the Monster onto the game surface.
        
        Args:
            target(pygame.Surface): the surface to draw Monster onto.
        """
        pygame.sprite.Sprite.update(self)
        self._move()
        self._bounce()
        self.rect.x = self._plat.rect.x + self._xFromPlat
        self.rect.y = self._plat.rect.y + self._yFromPlat
        target.blit(self._image, (self.rect.x, self.rect.y + self._yOffset))
        
    def _move(self):
        return
    
    def _bounce(self):
        if self._bouncing == 0: self._bouncing = 10
        if self._bouncing > 5:
            self._yOffset -= 2
            self._bouncing -= 1
        elif self._bouncing >0:
            self._yOffset += 2
            self._bouncing -=1
    
    def die(self):
        """Action taken when Monster receives damages.
        """
        self._dieSound.play(loops=0, maxtime=0, fade_ms=0)
        self.kill()
        
class Monster1(Monster):
    """Monster type one
    The first type of monster encountered by player in the game. It moves back
        and forth on its bounding platform with not additional actions.
        
    Attributes:
        rect(Rect): The Rect representation of Monster1's dimension and
            position.
    """
    def __init__(self, plat):
        """Inits Monster1 with image, size, position and additional base class 
            attributes.
            
        Args:
            plat(Platform): The bounding platform for Monster1.
        """
        Monster.__init__(self, plat)
        self._name = 1
        self._yFromPlat = -80
        self._image = pygame.image.load('mon1.png').convert_alpha()
        self.rect = self._image.get_rect()
        
    def _move(self):
        Monster._move(self)
        if self._movingDir == 0:
            self._image = pygame.image.load('mon1r.png').convert_alpha()
            if self._xFromPlat < self._plat.rect[2] - 50:
                self._xFromPlat += 5
            else:
                self._xFromPlat = self._plat.rect[2] - 50 
                self._movingDir = 1
        else:
            self._image = pygame.image.load('mon1.png').convert_alpha()
            if self._xFromPlat > 50:
                self._xFromPlat -= 5
            else:
                self._xFromPlat = 50
                self._movingDir = 0
                
class Monster2(Monster):
    """Monster type two
    The second type of monster encountered by player in the game. It moves back
        and forth on its bounding platform and has a random chance of jumping.
        
    Attributes:
        rect(Rect): The Rect representation of Monster2's dimension and
            position.
    """
    def __init__(self, plat):
        """Inits Monster2 with image, size, position and additional base class 
            attributes.
            
        Args:
            plat(Platform): The bounding platform for Monster2.
        """
        Monster.__init__(self, plat)
        self._name = 2
        self._yFromPlat = -80
        self._image = pygame.image.load('mon2.png').convert_alpha()
        self.rect = self._image.get_rect()
        self._jumping = 0
    
    def _move(self):
        Monster._move(self)
        rand = randint(0, 25)
        if rand == 10: self._jump()
        if self._jumping > 5:
            self._yFromPlat -= 30
            self._jumping -= 1
        elif self._jumping > 0:
            self._yFromPlat += 30
            self._jumping -= 1
        if self._movingDir == 0:
            self._image = pygame.image.load('mon2r.png').convert_alpha()
            if self._xFromPlat < self._plat.rect[2] - 50:
                self._xFromPlat += 5
            else:
                self._xFromPlat = self._plat.rect[2] - 50 
                self._movingDir = 1
        else:
            self._image = pygame.image.load('mon2.png').convert_alpha()
            if self._xFromPlat > 50:
                self._xFromPlat -= 5
            else:
                self._xFromPlat = 50
                self._movingDir = 0
                
    def _jump(self):
        if self._jumping == 0: self._jumping = 10
        
class Fireball(pygame.sprite.Sprite):
    def __init__(self, monster):
        pygame.sprite.Sprite.__init__(self)
        self._name = 3
        self.monster = monster
        self._image = pygame.image.load('fireball.png').convert_alpha()
        self.rect = self._image.get_rect()
        if self.monster._movingDir == 0:
            self.rect.center =  (self.monster.rect.right + 50, self.monster.rect.center[1] - 20)
        else:
            self.rect.center =  (self.monster.rect.left - 50, self.monster.rect.center[1] - 20)
        self._movingDir = self.monster._movingDir
        self._xFromPlat = self.rect.x - self.monster._plat.rect.x
        
    def update(self, target):
        if (self.rect.left < self.monster._plat.rect.left or
            self.rect.right > self.monster._plat.rect.right):
            self.kill()
        else:
            if self._movingDir == 0:
                self._xFromPlat += 20
            else:
                self._xFromPlat -= 20
            self.rect.x = self.monster._plat.rect.x + self._xFromPlat
            target.blit(self._image, (self.rect.x, self.rect.y))
            
class Monster3(Monster1):
    """Monster type three
    The second type of monster encountered by player in the game. It moves back
        and forth on its bounding platform and shoots fireballs at a time
        interval.
        
    Attributes:
        rect(Rect): The Rect representation of Monster3's dimension and
            position.
    """
    def __init__(self, plat):
        """Inits Monster3 with image, size, position and additional base class 
            attributes.
            
        Args:
            plat(Platform): The bounding platform for Monster3.
        """
        Monster1.__init__(self, plat)
        self._name = 3
        self._fireballList = pygame.sprite.Group()
        self._image = pygame.image.load('mon3.png').convert_alpha()
        self.rect = self._image.get_rect()
        self._yFromPlat = -80
        self._fireballCounter = 10
    
    def _move(self):
        Monster1._move(self)
        if self._movingDir == 0:
            self._image = pygame.image.load('mon3r.png').convert_alpha()
        else:
            self._image = pygame.image.load('mon3.png').convert_alpha()
    
    def update(self, target):
        """Updates and draws the Monster3 onto the game surface.
        
        Args:
            target(pygame.Surface): the surface to draw Monster3 onto.
        """
        Monster1.update(self, target)
        if len(self._fireballList) == 0 and self._fireballCounter == 0:
            fireball = Fireball(self)
            self._fireballList.add(fireball)
            self._fireballCounter = 10
        elif self._fireballCounter > 0:
            self._fireballCounter -= 1
        else:
            self._fireballList.update(target)
            
    def fireball(self):
        """The getter function for Monster3's fireballs
        
        Returns:
            pygame.Sprite.Group: A sprite group contains all Monster3's
                fireballs.
        """
        return self._fireballList
    
    def die(self):
        """Action taken when Monster3 receives damages.
        """
        Monster1.die(self)
        for fire in self._fireballList:
            fire.kill()
            
class Boss1(Monster):
    """Boss type one
    The first type of boss encountered by player in the game. It moves back
        and forth on its bounding platform and has a chance of pausing at the
        far left and far right. Boss1 has greater speed and health than regular
        monsters.
        
    Attributes:
        rect(Rect): The Rect representation of Monster3's dimension and
            position.
    """
    def __init__(self, plat):
        """Inits Boss1 with image, size, position and additional base class 
            attributes.
            
        Args:
            plat(Platform): The bounding platform for Boss1.
        """
        Monster.__init__(self, plat)
        self._name = 4
        self._life = 1
        self._plat = plat
        self._xFromPlat = self._plat.rect[2] + 100
        self._yFromPlat = -100
        self._image = pygame.image.load('boss1.png').convert_alpha()
        self._heartImage = pygame.image.load('bheart.png').convert_alpha()
        self.rect = self._image.get_rect();
        
    def update(self, target):
        """Updates and draws the Boss1 onto the game surface.
        
        Args:
            target(pygame.Surface): the surface to draw Boss1 onto.
        """
        Monster.update(self, target)
        if self._plat.rect.x <= 0:
            for i in range(0, self._life):
                target.blit(self._heartImage, (760 - i * 40, 10))
        
    def _move(self):
        Monster._move(self)
        if self._plat.rect.x <= 0:
            if self._movingDir == 0:
                self._image = pygame.image.load('boss1r.png').convert_alpha()
                if self._xFromPlat == 50:
                    if randint(1, 20) == 5:
                        self._xFromPlat += 20
                elif self._xFromPlat < self._plat.rect[2] - 200:
                    self._xFromPlat += 20
                else:
                    self._xFromPlat = self._plat.rect[2] - 200
                    self._movingDir = 1
            else:
                self._image = pygame.image.load('boss1.png').convert_alpha()
                if (self._xFromPlat <= self._plat.rect[2] + 100 and 
                    self._xFromPlat > self._plat.rect[2] - 50):
                    self._xFromPlat -= 5 
                if self._xFromPlat == self._plat.rect[2] - 200:
                    if randint(1, 20) == 5:
                        self._xFromPlat -= 20
                elif self._xFromPlat > 50:
                    self._xFromPlat -= 20
                else:
                    self._xFromPlat = 50
                    self._movingDir = 0
                    
    def die(self):
        """Action taken when Boss1 receives damages.
        """
        self._dieSound.play()
        if self._life == 1:
            self._life -= 1
            self.kill()
        elif self._life < 1:
            self.kill()
        else: self._life -= 1
        
    def isDead(self):
        """Checks whether Boss1 is dead.
        
        Returns:
            bool: True if Boss1 is dead, False otherwise.
        """
        return self._life <= 0;