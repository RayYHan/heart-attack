import pygame, sys
from pygame.locals import *

WHITE = (255, 255, 255)
SKYBLUE = (135, 206, 255)
GREY = (125, 125, 125)
BLACK = (100, 100, 100)

class Background:
    """Game Background
    This class generates and control the entire non-interactive backgroung of
        the game.
    """
    def __init__(self, size):
        """Inits Background with size and element positions.
        
        Args:
            size(tuple): The desired (width, height) of the background. 
        """
        self._size = size
        (self._width, self._height) = size
        self._cloudCord = (0, 0)
        #self._mountCord = (200, self._height - 149)
        self._mountCord = (0, 0)
    
    def update(self, target):
        """Updates and draws the background onto the screen.
        
        Args:
            target(pygame.Surface): The screen surface to draw Background onto.
        """
        background = pygame.Surface(self._size).convert()
        background.fill(SKYBLUE)
        cloudLayer = pygame.Surface((self._width, 210))
        cloudLayer.fill(SKYBLUE)
        self._drawCloud(cloudLayer, 100, 100)
        self._drawCloud(cloudLayer, 300, 150)
        self._drawCloud(cloudLayer, 150, 200)
        cloudLayer.set_colorkey(SKYBLUE)
        mountLayer = pygame.image.load('city.png').convert_alpha()
        #mountLayer = pygame.Surface((self._width, 150))
        #mountLayer.fill(SKYBLUE)
        #self._drawMountain(mountLayer, 0, 0)
        #mountLayer.set_colorkey(SKYBLUE)
        background.blit(mountLayer, self._mountCord)
        background.blit(mountLayer, (self._mountCord[0] + 800, self._mountCord[1]))
        background.blit(mountLayer, (self._mountCord[0] - 800, self._mountCord[1]))
        self._drawSun(background, self._width - 150 , 25)
        target.blit(background, (0, 0))
        
    def _drawCloud(self, surface, x, y):
        pygame.draw.circle(surface, WHITE, [x - 15, y], 10)
        pygame.draw.circle(surface, WHITE, [x + 15, y], 10)
        pygame.draw.circle(surface, WHITE, [x, y - 10], 10)
        pygame.draw.polygon(surface, WHITE, [[x - 15, y - 10], [x - 15, y + 10], [x + 40, y + 10]])
        
    def _drawMountain(self, surface, x, y):
        mountainSurface = pygame.Surface((150, 150))
        mountainSurface.fill(SKYBLUE)
        pygame.draw.polygon(mountainSurface, GREY, [[10, 150], [140, 150], [110, 0], [40, 0]])
        pygame.draw.polygon(mountainSurface, BLACK, [[10, 150], [140, 150], [110, 0], [40, 0]], 2)
        pygame.draw.polygon(mountainSurface, GREY, [[90, 150], [148, 150], [140, 75], [100, 75]])
        pygame.draw.polygon(mountainSurface, BLACK, [[90, 150], [148, 150], [140, 75], [100, 75]], 2)
        pygame.draw.polygon(mountainSurface, GREY, [[20, 150], [100, 150], [90, 40], [40, 40]])
        pygame.draw.polygon(mountainSurface, BLACK, [[20, 150], [100, 150], [90, 40], [40, 40]], 2)
        pygame.draw.polygon(mountainSurface, GREY, [[2, 150], [60, 150], [50, 90], [12, 90]])
        pygame.draw.polygon(mountainSurface, BLACK, [[2, 150], [60, 150], [50, 90], [12, 90]], 2)
        surface.blit(mountainSurface, [x, y])
        
    def _drawSun(self, surface, x, y):
        GOLD = (255, 215, 0)
        tempSurf = pygame.Surface((100, 100))
        pygame.draw.polygon(tempSurf, GOLD, [[50, 0], [45, 15], [55, 15]])
        pygame.draw.polygon(tempSurf, GOLD, [[0, 50], [15, 45], [15, 55]])
        pygame.draw.polygon(tempSurf, GOLD, [[100, 50], [85, 45], [85, 55]])
        pygame.draw.polygon(tempSurf, GOLD, [[50, 100], [45, 85], [55, 85]])
        tempSurf = pygame.transform.rotate(tempSurf, 45)
    
        pygame.draw.circle(tempSurf, GOLD, [71, 71], 30)
        pygame.draw.polygon(tempSurf, GOLD, [[70, 20], [65, 35], [75, 35]])
        pygame.draw.polygon(tempSurf, GOLD, [[20, 70], [35, 65], [35, 75]])
        pygame.draw.polygon(tempSurf, GOLD, [[120, 70], [105, 65], [105, 75]])
        pygame.draw.polygon(tempSurf, GOLD, [[70, 120], [65, 105], [75, 105]])
        
        tempSurf.set_colorkey((0, 0, 0))
        surface.blit(tempSurf, (x, y))
        
    def moveL(self):
        """Moves the Background to the right when the player moves to the left.
        """
        self._cloudCord = (self._cloudCord[0] + 5, self._cloudCord[1])
        self._mountCord = (self._mountCord[0] + 10, self._mountCord[1])
            
        if self._cloudCord[0] > self._width + 10:
            self._cloudCord = (-350, self._cloudCord[1])
        if self._cloudCord[0] < -351:
            self._cloudCord = (self._width + 9, self._cloudCord[1])
        if self._mountCord[0] > self._width:
            self._mountCord = (0, self._mountCord[1])
        if self._mountCord[0] < 0:
            self._mountCord = (800, self._mountCord[1])
            
    def moveR(self):
        """Moves the Background to the left when the player moves to the right.
        """
        self._cloudCord = (self._cloudCord[0] - 5, self._cloudCord[1])
        self._mountCord = (self._mountCord[0] - 10, self._mountCord[1])
        
        if self._cloudCord[0] > self._width + 10:
            self._cloudCord = (-350, self._cloudCord[1])
        if self._cloudCord[0] < -351:
            self._cloudCord = (self._width + 9, self._cloudCord[1])
        if self._mountCord[0] > 800:
            self._mountCord = (0, self._mountCord[1])
        if self._mountCord[0] < 0:
            self._mountCord = (800, self._mountCord[1])