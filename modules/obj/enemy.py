import pygame
import path
import math
from utils import *
from constants import *

pygame.mixer.init()

# load image
SkuImg = pygame.image.load(path.skull_image)
SkehandImg = pygame.image.load(path.skeleton_image)
# load sound
SkuSound = pygame.mixer.Sound(path.skull_sound)
SkuSound.set_volume(1)


# đầu lâu (skull) lao đến tấn công player
class Skull(object):

    def __init__(self, x, y, width, height, target):
        """
        x, y: position
        width, height: size
        target: player
        """
        # transform
        # vị trí
        self.x = x
        self.y = y
        # kích thước
        self.width = width
        self.height = height

        self.target = target # đối tượng tấn cống
        # properties
        self.speed = 5
        self.dame = 5
        # collider
        self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height) # hộp va chạm của đối tượng
        # sound
        pygame.mixer.Channel(4).play(SkuSound)

    def draw(self, screen):
        """
        Draw skull
        """
        self.move()

        screen.blit(SkuImg, (self.x, self.y))

        self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height) # hộp va chạm của đối tượng skull

        if COLLIDER_DEBUG: # Vẽ hộp va chạm trong trường hợp debug
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

    def hit(self):
        """
        Kiểm tra va chạm với player
        
        Return: True nếu va chạm, False nếu không va chạm
        """
        if self.hitBox.colliderect(self.target.hitBox): # nếu hộp va chạm của skull chạm vào hộp va chạm của player
            return True
        return False

    def move(self):
        """
        Di chuyển skull theo hướng của player
        """
        
        dx = min(self.speed, abs(self.x - self.target.x)) # tính khoảng cách theo trục x

        # di chuyển theo hướng của player theo trục x
        if self.x < self.target.x:
            self.x += dx
        else:
            self.x -= dx

        dy = min(self.speed, abs(self.y - self.target.y + 10)) # tính khoảng cách theo trục y

        # di chuyển theo hướng của player theo trục y
        if self.y < self.target.y - 7:
            self.y += dy
        else:
            self.y -= dy



# skull fly around boss (đầu lâu bay quanh boss)
class FloatingSkull(object):
    
    def __init__(self, target, player, number):
        """
        target: boss
        player: player
        number: số thứ tự của đầu lâu
        """

        # transform
        self.x = target.x
        self.y = target.y
        self.width = 64
        self.height = 64
        self.target = target
        self.player = player
        self.number = number
        # properties
        self.alpha = 0
        self.dame = 5
        self.radius = 160
        # collider
        self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height) # tạo hộp va chạm của đầu lâu bay quanh skull
        # sound
        pygame.mixer.Channel(4).play(SkuSound)

    def draw(self, screen):
        """
        Draw skull
        """
        self.move()

        screen.blit(SkuImg, (self.x, self.y)) # vẽ hình ảnh skull

        limit_screen(self) # giới hạn di chuyển của đầu lâu trong màn hình

        self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height) # tạo hộp va chạm của đầu lâu bay quanh skull

        if COLLIDER_DEBUG: # Vẽ hộp va chạm trong trường hợp debug
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

    def hit(self):
        """
        Kiểm tra va chạm với player
        """
        if self.hitBox.colliderect(self.player.hitBox): # hộp va chạm của đầu lâu bay quanh skull chạm vào hộp va chạm của player
            return True
        return False

    def move(self):
        """
        Di chuyển đầu lâu bay quanh skull theo quỹ đạo tròn quanh target(boss)
        Tính toán tọa độ x, y của đầu lâu bay quanh skull theo góc alpha, bán kính và số thứ tự của đầu lâu
        """
        self.alpha += 0.1 

        if self.alpha == 360:
            self.alpha = 0

        self.x = self.target.x+90 - self.radius * \
            math.cos(self.alpha + self.number*80)
        self.y = self.target.y+95 - self.radius * \
            math.sin(self.alpha + self.number*80)



# skeleton hand tấn công player, quét ngang map
class SkeHand(object):
    def __init__(self, x, y, facing, target):
        """
        x, y: position
        facing: hướng xoay của cái tay (1: phải, -1: trái)
        target: player
        """

        # transform
        self.x = x
        self.y = y
        self.target = target # player
        self.rotate = 0 # góc xoay của cái tay
        # properties
        self.facing = facing  # hướng di chuyển của cái tay (1: phải, -1: trái)
        self.speed = 8
        self.dame = 3
        # collider
        self.hitBox = pygame.Rect(self.x, self.y, 34, 120) # tạo hộp va chạm của cái tay

    def draw(self, screen):
        """
        Draw skeleton hand
        """

        # vẽ hình ảnh và hộp va chạm của cái tay với các góc xoay khác nhau
        if self.rotate == 0:
            screen.blit(SkehandImg, (self.x, self.y - 60)) # vẽ hình ảnh cái tay
            self.hitBox = pygame.Rect(self.x, self.y - 60, 34, 120) # tạo hộp va chạm của cái tay
        if self.rotate == 90:
            screen.blit((pygame.transform.rotate(SkehandImg, -90)),
                        (self.x - 60, self.y - 17))
            self.hitBox = pygame.Rect(self.x - 60, self.y - 17, 120, 34)
        if self.rotate == 180:
            screen.blit(pygame.transform.flip(
                SkehandImg, True, True), (self.x, self.y - 60))
            self.hitBox = pygame.Rect(self.x, self.y - 60, 34, 120)
        if self.rotate == 270:
            screen.blit((pygame.transform.rotate(SkehandImg, 90)),
                        (self.x - 30, self.y - 7))
            self.hitBox = pygame.Rect(self.x - 30, self.y - 7, 120, 34)

        if COLLIDER_DEBUG: # Vẽ hộp va chạm trong trường hợp debug
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2) # vẽ hộp va chạm

    def hit(self):
        """
        Kiểm tra va chạm với player
        """
        if self.hitBox.colliderect(self.target.hitBox): # hộp va chạm của cái tay chạm vào hộp va chạm của player
            return True
        return False

    def move(self):
        """
        Di chuyển tay xương xoay tròn và đi ngang qua màn hình
        """
        
        self.x += 8 * self.facing # di chuyển cái tay theo hướng của nó
        self.rotate += 90 # xoay cái tay theo hướng của nó

        # reset rotate
        if (self.rotate >= 360):
            self.rotate = 0
        