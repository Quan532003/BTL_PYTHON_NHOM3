import pygame
import utils
import random
import path
import data
import math
from pygame.locals import *
from constants import *
from modules.obj.projectile import *

pygame.mixer.init()

# load animation
idle = [pygame.image.load(path.idle_1_image),
        pygame.image.load(path.idle_2_image),
        pygame.image.load(path.idle_3_image),
        pygame.image.load(path.idle_1_image)]

walkDown = [pygame.image.load(path.walk_down_1_image),
            pygame.image.load(path.walk_down_2_image)]
walkUp = [pygame.image.load(path.walk_up_1_image),
          pygame.image.load(path.walk_up_2_image)]
walkRight = [pygame.image.load(path.walk_right_1_image),
             pygame.image.load(path.walk_right_2_image),
             pygame.image.load(path.walk_right_3_image),
             pygame.image.load(path.walk_right_1_image)]
walkLeft = [pygame.image.load(path.walk_left_1_image),
            pygame.image.load(path.walk_left_2_image),
            pygame.image.load(path.walk_left_3_image),
            pygame.image.load(path.walk_left_1_image)]


AttackAnimation = [pygame.image.load(path.attack_left_image),
                   pygame.image.load(path.attack_right_image),
                   pygame.image.load(path.attack_up_image),
                   pygame.image.load(path.attack_down_image)]

clone = pygame.image.load(path.player_shadow_image)
Player_getHit = pygame.image.load(path.player_hurt_image)

# load sound
Attack_Sound = pygame.mixer.Sound(path.attack_sound)
Sound_Move = pygame.mixer.Sound(path.move_sound)
Sound_Hurt = pygame.mixer.Sound(path.hurt_sound)
Attack_Sound.set_volume(0.2)
Sound_Move.set_volume(0.3)
Sound_Hurt.set_volume(0.2)

x = 0
y = 400
clone_x = 0
clone_y = 439
width = 64
height = 92
speed = 7
isJump = False
jumpCount = 8
walk = False

# kiểm tra xem có va chạm với đá trên map không


def inRock(x, y):
    if x >= 35 and x <= 277 and y >= 80 and y <= 200:
        return True
    return False


class Player(object):
    def __init__(self, x, y):
        # transform
        self.x = x
        self.y = y
        self.width = idle[0].get_width()
        self.height = idle[0].get_height()
        self.clone_x = x
        self.clone_y = y + 39
        # properties
        self.HP = PLAYER["HP"]
        self.MP = PLAYER["MP"]
        self.speed = 8
        self.isJump = False
        self.walk = False
        self.direction = "left"
        self.walkYCount = 0
        self.walkXCount = 0
        self.idleCount = 0
        self.jumpCount = 8
        self.Attacks = []
        self.Recover = []
        self.cooldown = 0
        self.isAttacking = False
        self.AtCount = 0
        self.hitBox = idle[0].get_rect()
        self.getHitCooldown = 0

        # slide
        self.slideCooldown = 0
        self.slideDirection = "left"

    def controller(self):
        keys = pygame.key.get_pressed()

        # reset animation walk
        self.walk = False

        # slide
        if keys[pygame.K_a]:
            self.slide()

        # attack
        if keys[pygame.K_d]:
            self.attack()

        # move
        self.move(keys)

        # jump
        if keys[pygame.K_SPACE]:
            self.isJump = True
        self.jump()

        # update
        self.updateCooldown()
        self.updateHitBox()
        self.updateShadow()

    def draw(self, screen):

        # Health bar
        self.updateHealthBar(screen)

        # Character animation
        if self.slideCooldown <= 20:
            screen.blit(clone, (self.clone_x, self.clone_y))
            if not (self.isAttacking):

                if self.idleCount + 1 >= 48:
                    self.idleCount = 0
                if self.walkYCount + 1 >= 20:
                    self.walkYCount = 0
                if self.walkXCount + 1 >= 20:
                    self.walkXCount = 0
                    
                if not (self.walk):
                    screen.blit(idle[self.idleCount//12], (self.x, self.y))
                    self.idleCount += 1
                else:
                    if self.direction == "down":
                        screen.blit(
                            walkDown[self.walkYCount//10], (self.x, self.y))
                        self.walkYCount += 1
                    elif self.direction == "up":
                        screen.blit(
                            walkUp[self.walkYCount//10], (self.x, self.y))
                        self.walkYCount += 1
                    elif self.direction == "right":
                        screen.blit(
                            walkRight[self.walkXCount//5], (self.x, self.y))
                        self.walkXCount += 1
                    elif self.direction == "left":
                        screen.blit(
                            walkLeft[self.walkXCount//5], (self.x, self.y))
                        self.walkXCount += 1
                    # Sound_Move.play()
            else:

                if self.direction == "left":
                    screen.blit(AttackAnimation[0], (self.x, self.y))
                if self.direction == "right":
                    screen.blit(AttackAnimation[1], (self.x, self.y))
                if self.direction == "up":
                    screen.blit(AttackAnimation[2], (self.x, self.y))
                if self.direction == "down":
                    screen.blit(AttackAnimation[3], (self.x, self.y))
                self.AtCount += 1

                if self.AtCount == 4:
                    self.isAttacking = False
                    self.AtCount = 0
        else:
            if self.slideDirection == "left":
                self.x -= self.speed * 3
                self.clone_x = self.x
                screen.blit(clone, (self.clone_x, self.clone_y))
                screen.blit(walkLeft[2], (self.x, self.y))
            elif self.slideDirection == "right":
                self.x += self.speed * 3
                self.clone_x = self.x
                screen.blit(clone, (self.clone_x, self.clone_y))
                screen.blit(walkRight[2], (self.x, self.y))
            elif self.slideDirection == "up":
                self.y -= self.speed * 3
                self.clone_y = self.y + 39
                screen.blit(clone, (self.clone_x, self.clone_y))
                screen.blit(walkUp[1], (self.x, self.y))
            elif self.slideDirection == "down":
                self.y += self.speed * 3
                self.clone_y = self.y + 39
                screen.blit(clone, (self.clone_x, self.clone_y))
                screen.blit(walkDown[1], (self.x, self.y))

        self.drawHitEffect(screen)

        if COLLIDER_DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

        self.updateProjectile(screen)

        self.updateOrb(screen)

        # limit player in screen
        utils.limit_screen(self)

    def getHit(self, dame):
        if (self.getHitCooldown == 0):         
            self.HP -= dame
            self.getHitCooldown = PLAYER["GetHitCooldown"]
            pygame.mixer.Channel(3).play(Sound_Hurt)

    def attack(self):
        if self.cooldown == 0 and self.MP > 0:
            self.isAttacking = True
            self.MP -= PLAYER["AttackManaCost"]
            self.Attacks.append(
                Projectile(
                    round(self.x + self.width // 2),
                    round(self.y + self.height//2),
                    self.direction
                )
            )
            self.cooldown = PLAYER["AttackCooldown"]
            pygame.mixer.Channel(0).play(Attack_Sound)  # Play sound

    # khi nhấn phím D thì sẽ gọi hàm attack
    # hàm này chỉ thực thi khi thỏa mãn điều kiện về cooldown attack và MP
    # attack method sẽ đưa player vào trạng thái attack, tiêu hao MP, đặt lại cooldown attack 
    # sau đó tạo ra 1 projectile theo hướng của player 
    # và đưa vào list Attacks để phục vụ check hitBox với enemy và boss ở play_scene
    # cuối cùng nó phát ra sound attack ở kênh 0 nhăm phân biệt với sound khác


    def slide(self):
        if self.slideCooldown == 0:
            self.slideCooldown = PLAYER["SlideCooldown"]
            self.slideDirection = self.direction

    def move(self, keys):
        velocity = pygame.Vector2(0, 0)

        if keys[pygame.K_LEFT]:
            self.direction = "left"
            velocity.x = -1
        if keys[pygame.K_RIGHT]:
            self.direction = "right"
            velocity.x = 1
        if keys[pygame.K_UP]:
            self.direction = "up"
            velocity.y = -1
        if keys[pygame.K_DOWN]:
            self.direction = "down"
            velocity.y = 1

        if velocity.x != 0 or velocity.y != 0:
            self.walk = True
            # Chuẩn hóa vector trong trường hợp di chuyển chéo
            velocity = velocity.normalize() * self.speed
            self.x += velocity.x
            self.y += velocity.y

    def jump(self):
        if self.isJump == False:
            return
        
        if self.jumpCount >= -8: # sử dụng hàm parabol để nhảy
            if self.jumpCount > 0:
                self.y -= (self.jumpCount ** 2) / 2
            else:
                self.y += (self.jumpCount ** 2) / 2

            self.jumpCount -= 1
        else: # reset jump
            self.jumpCount = 8
            self.isJump = False

    def updateCooldown(self):
        if self.slideCooldown > 0:
            self.slideCooldown -= 1

        if self.getHitCooldown > 0:
            self.getHitCooldown -= 1

    def updateHealthBar(self, screen):
        utils.drawBar(screen)
        # draw mask HP
        pygame.draw.rect(screen, (50, 50, 50), (0, 3, self.HP * 2, 20))
        # draw mask MP
        pygame.draw.rect(screen, (128, 128, 128), (0, 25, self.MP * 2, 20))

    def updateShadow(self):
        self.clone_x = self.x
        self.clone_y = self.y + 39

    def updateOrb(self, screen):
        # draw orb and check hit
        for orb in self.Recover:
            orb.draw(screen)
            if orb.hit():
                if orb.tag == "MP":
                    self.MP += 1
                    self.MP = min(self.MP, PLAYER["MP"])
                if orb.tag == "HP":
                    self.HP += 2
                    self.HP = min(self.HP, PLAYER["HP"])
                self.Recover.remove(orb)

    def updateProjectile(self, screen):
        # remove projectile out of screen
        for projectile in self.Attacks:
            projectile.draw(screen)
            if projectile.x < 1500 and projectile.x > 0 and projectile.y > 150 and projectile.y < 800:
                pass
            else:
                self.Attacks.pop(self.Attacks.index(projectile))

    def updateHitBox(self):
        self.hitBox.x = self.x
        self.hitBox.y = self.y

    def createManaOrb(self, x, y):
        # mana orb limit
        if (len(self.Recover) > 5):
            return
        self.Recover.append(ManaOrb(x, y, self))

    def createHpOrb(self, x, y):
        self.Recover.append(HpOrb(x, y, self))

    def drawHitEffect(self, screen):
        # Hiệu ứng nhấp nháy khi nhận sát thương
        if (self.getHitCooldown % 20 == 0 and self.getHitCooldown > 0): 
            screen.blit(Player_getHit, (self.x, self.y))
    