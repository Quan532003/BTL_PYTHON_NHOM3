import pygame, path
from constants import *
from data import *

projectileImage = pygame.image.load(path.projectile_image)
manaOrbImage = pygame.image.load(path.mana_orb_image)
hpOrbImage = pygame.image.load(path.hp_orb_image)

class Projectile():
    def __init__(self, x, y, direction):
        # transform
        self.x = x
        self.y = y
        self.direction = direction
        # properties
        self.speed = PROJECTILE["speed"]
        self.dame = PROJECTILE["dame"]
        # collider
        self.hitBox = projectileImage.get_rect()
        self.hitBox.x = self.x
        self.hitBox.y = self.y

    def draw(self, screen : pygame.Surface):
        self.move()
    
        screen.blit(projectileImage, (self.x, self.y))

        self.hitBox.x = self.x
        self.hitBox.y = self.y

        if COLLIDER_DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

    def hit(self, enemy):
        if self.hitBox.colliderect(enemy.hitBox):
            return True
        return False
    
    def move(self):
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

class Orb():
    def __init__(self, x, y, target):
        # transform
        self.x = x
        self.y = y
        self.target = target
        # properties
        self.tag : str
        # collider
        self.hitBox : pygame.Rect 

    def draw(self, screen):
        pass

    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox):
            return True
        return False

class ManaOrb(Orb):
    def __init__(self, x, y, target):
        super().__init__(x, y, target)
        # properties
        self.tag = "MP"
        # collider
        self.hitBox = manaOrbImage.get_rect()
        self.hitBox.x = self.x
        self.hitBox.y = self.y

    def draw(self, screen : pygame.Surface):
        screen.blit(manaOrbImage, (self.x, self.y))

        if COLLIDER_DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

class HpOrb(Orb):
    def __init__(self, x, y, target):
        super().__init__(x, y, target)
        # properties
        self.tag = "HP"
        # collider
        self.hitBox = hpOrbImage.get_rect()
        self.hitBox.x = self.x
        self.hitBox.y = self.y

    def draw(self, screen : pygame.Surface):
        screen.blit(hpOrbImage, (self.x, self.y))

        if COLLIDER_DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 4)
