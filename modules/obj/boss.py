import random
import pygame
import sys
import utils
import path
from pygame.locals import *
from modules.obj.enemy import *
from modules.obj.projectile import *

pygame.init()
pygame.mixer.init()

# load image
Boss = pygame.image.load(path.boss_image) #hình ảnh boss
Boss = pygame.transform.scale(Boss, (250, 250)) # xét kích thước cho hình ảnh
Boss_getHit = pygame.image.load(path.boss_gethit_image) # hình ảnh khi bị đánh
Boss_getHit = pygame.transform.scale(Boss_getHit, (250, 250)) # xét kích thước cho hình ảnh
Boss_shadow = pygame.image.load(path.boss_shadow_image) # hình ảnh bóng của boss
Boss_shadow = pygame.transform.scale(Boss_shadow, (230, 250/6)) # xét kích thước cho hình ảnh
Boss_side = pygame.image.load(path.boss_side_image) # hình ảnh boss khi đánh
Boss_side = pygame.transform.scale(Boss_side, (250, 250)) # xét kích thước cho hình ảnh
Boss_s1Ac = pygame.image.load(path.boss_skill1ac_image) # hình ảnh boss khi dùng skill 1
Boss_s1Ac = pygame.transform.scale(Boss_s1Ac, (250, 250)) # xét kích thước cho hình ảnh
# load sound
Skill1Sound = pygame.mixer.Sound(path.boss_skill1_sound)
Skill1Sound.set_volume(0.5)
BSound_hurt = pygame.mixer.Sound(path.boss_hurt_sound)
BSound_hurt.set_volume(0.6)


class boss(object):
    def __init__(self, x, y, target):
        self.x = x # vị trí x của boss
        self.y = y # vị trí y của boss
        self.sha_x = x # vị trí bóng x của boss
        self.sha_y = y + 250 # vị trí bóng y của boss
        self.width = 250 # chiều rộng của boss
        self.height = 250 # chiều cao của boss
        self.HP = 100 # máu của boss
        self.hitBox = pygame.Rect(x + 10, y, 230, 250) # collider của boss
        self.GetHit = 0 # biến để xét khi boss bị đánh
        self.floatCount = 0 # biến để xét khi boss đang bay
        self.Attacks = [] # list chứa các đạn của boss
        self.Cooldown = 0 # thời gian cooldown
        self.Acskill = False # xét khi boss dùng skill
        self.facing = -1 # hướng của boss
        self.target = target # target của boss

        # skill 1
        self.s1Active = 0 # biến để xét khi boss dùng skill 1, có active hay không
        self.s1_Speed = 0 # tốc độ của boss khi dùng skill 1
        self.s1_Cd = 0 # thời gian cooldown của skill 1
        # skill 2
        self.s2_Cd = 0 # thời gian cooldown của skill 2
        # skill 3
        self.s3_cd = 0 # thời gian cooldown của skill 3

    def draw(self, screen): # hàm vẽ boss
        # Cooldown
        if self.Cooldown > 0: # nếu cooldown > 0 thì giảm cooldown
            self.Cooldown -= 1
        if self.s1_Cd > 0: # nếu thời gian hồi chiêu của chiêu 1 > 0 thì giảm thời gian hồi chiêu của chiêu 1
            self.s1_Cd -= 1
        if self.s2_Cd > 0: # nếu thời gian hồi chiêu của chiêu 2 > 0 thì giảm thời gian hồi chiêu của chiêu 2
            self.s2_Cd -= 1
        if self.s3_cd > 0: # nếu thời gian hồi chiêu của chiêu 3 > 0 thì giảm thời gian hồi chiêu của chiêu 3
            self.s3_cd -= 1

        if not (self.Acskill): # nếu đang không ra chiêu, tức là đứng yên
            if self.floatCount >= -1:
                self.y -= (self.floatCount * abs(self.floatCount)) * 0.5
                self.floatCount -= 0.1
            else:
                self.floatCount = 1

            if self.GetHit > 0: # nếu bị đánh thì hiển thị hình ảnh bị đánh
                screen.blit(Boss_getHit, (self.x, self.y))
                self.GetHit -= 1 # giảm biến GetHit
            else: # nếu không bị đánh thì hiển thị hình ảnh bình thường
                screen.blit(Boss, (self.x, self.y))
        else: #nếu đang tấn công
            # Skill 1
            if (self.s1Active > 0): # nếu đang tấn công skill1
                if self.s1Active > 30: # nếu thời gian tấn công skill1 > 30
                    if self.y + 250 != self.target.y + 92: # nếu tạo độ y + 250 khác tọa độ đích y + 92, tức là check mục tiêu có di chuyển hay không
                        if self.y + 250 > self.target.y + 92: # nếu lớn hơn thì di chuyển lại gần mục tiêu theo trục y
                            self.y -= self.s1_Speed
                        else:
                            self.y += self.s1_Speed
                    screen.blit(Boss, (self.x, self.y)) # vẽ boss tại vị trí x, y
                elif self.s1Active > 25: # nếu thời gian tấn công skill1 > 25
                    screen.blit(Boss_s1Ac, (self.x, self.y)) # nháy mắt đỏ
                else: # di chuyển đến vị trí của mục tiêu
                    # Skill1Sound.play()
                    self.x += 30*self.facing #facing là hướng mặt của boss
                    #vẽ boss theo hướng mặt
                    if self.facing == -1:
                        screen.blit(Boss_side, (self.x, self.y))
                    else:
                        screen.blit(pygame.transform.flip(
                            Boss_side, True, False), (self.x, self.y))
                self.s1Active -= 1
            else: #nếu không tấn công skill1
                self.Acskill = False
            # đặt vị trí bóng luôn nằm dưới chân boss
            self.sha_x = self.x
            self.sha_y = self.y + 250

        for At in self.Attacks: # duyệt qua tất cả các đạn trong list Attacks
            At.draw(screen) # vẽ nó lên màn hình

        utils.limit_screen(self) # giới hạn vị trí trong màn hình
        screen.blit(Boss_shadow, (self.sha_x, self.sha_y)) # vẽ bóng của boss

        # HP
        pygame.draw.rect(screen, (10, 10, 10), (1480, 200, 50, 100*5 + 4)) # vẽ hình chữ nhật đen nền của máu ở dưới
        pygame.draw.rect(screen, (200, 200, 200), (1480 + 2,
                         200 + 2 + (100 - self.HP)*5, 50 - 4, self.HP*5)) # vẽ thanh máu

        # ColiderBox
        self.hitBox = pygame.Rect(self.x + 10, self.y, 230, 250) # vẽ collider của boss
        if COLLIDER_DEBUG: # nếu bật chế độ debug
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

    def getHit(self, dame): # hàm xét khi boss bị đánh
        pygame.mixer.Channel(2).play(BSound_hurt) #bật âm thanh
        self.HP -= dame # giảm máu
        self.GetHit = 2 # set biến GetHit = 2 để hiển thị hình ảnh bị đánh

    def hit(self): # hàm xét khi boss có va chạm
        if self.hitBox.colliderect(self.target.hitBox): # nếu collider của boss chạm vào collider của mục tiêu
            return True
        return False

    def Attack(self, Player): # hàm tấn công

        if self.s1_Cd == 0: # nếu thời gian hồi chiêu của chiêu 1 = 0
            self.skill1() # dùng chiêu 1
            self.s1_Cd = 120 # set thời gian hồi chiêu của chiêu 1 = 120

        if self.s2_Cd == 0 and self.HP < 30: # nếu thời gian hồi chiêu của chiêu 2 = 0 và máu < 30
            self.skill2() # dùng chiêu 2
            self.s2_Cd = 50 # set thời gian hồi chiêu của chiêu 2 = 50

        if self.Cooldown == 0: # nếu thời gian cooldown = 0
            # self.skill1()
            self.Attacks.append(Skull(self.x, self.y, 64, 64, Player)) # thêm đạn vào list Attacks
            self.Cooldown = 100 # set thời gian cooldown = 100

        if self.s3_cd == 0 and self.HP < 60: # nếu thời gian hồi chiêu của chiêu 3 = 0 và máu < 60
            self.skill3() # dùng chiêu 3
            self.s3_cd = 150 # set thời gian hồi chiêu của chiêu 3 = 150

    def skill1(self): # hàm chiêu 1

        if self.x - self.target.x > 0: # nếu mục tiêu nằm bên trái boss
            self.facing = -1 # hướng mặt của boss là -1
        else:
            self.facing = 1 # hướng mặt của boss là 1
        pygame.mixer.Channel(1).play(Skill1Sound) # bật âm thanh
        self.s1_Speed = abs(self.target.y + 92 - self.y - 250)/10 # tốc độ của boss khi dùng skill 1
        self.s1Active = 40 # set thời gian tấn công của chiêu 1 = 40
        self.Acskill = True # set biến Acskill = True
        self.s1_Cd = 10 # set thời gian hồi chiêu của chiêu 1 = 10

    def skill2(self): # hàm chiêu 2
        x = random.randrange(-100, 100) # random vị trí x
        if self.facing == 1: # nếu hướng mặt của boss là 1
            self.Attacks.append(SkeHand(0, 200 + x, 1, self.target)) # thêm các khúc xương vào list Attacks
            self.Attacks.append(SkeHand(100, 450 + x, 1, self.target))
            self.Attacks.append(SkeHand(0, 700 + x, 1, self.target))
        else: # nếu hướng mặt của boss là -1
            self.Attacks.append(SkeHand(1500, 200 + x, -1, self.target)) # thêm các khúc xương vào list Attacks
            self.Attacks.append(SkeHand(1400, 450 + x, -1, self.target))
            self.Attacks.append(SkeHand(1300, 700 + x, -1, self.target))

    def skill3(self): # hàm chiêu 3
        self.Attacks.clear() # xóa tất cả các đạn trong list Attacks
        self.Attacks.append(FloatingSkull(self, self.target, 0)) # thêm ác đầu nâu vào list Attacks
        self.Attacks.append(FloatingSkull(self, self.target, 1))
        self.Attacks.append(FloatingSkull(self, self.target, 2))
        self.Attacks.append(FloatingSkull(self, self.target, 3))
