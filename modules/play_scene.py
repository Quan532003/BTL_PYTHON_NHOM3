import pygame
import sys
import path
from pygame.locals import *
from modules.obj.player import *
from modules.obj.enemy import *
from modules.obj.boss import *
from modules.obj.projectile import *

pygame.init()
pygame.mixer.init()

FPS = 30
fpsClock = pygame.time.Clock()  # đồng hồ đếm FPS
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), 0, 32)
pygame.display.set_caption("Death War")
background = pygame.transform.scale(pygame.image.load(path.background_image), (GAME_WIDTH, GAME_HEIGHT))
icon = pygame.image.load(path.icon_image)
pygame.display.set_icon(icon)
lose = pygame.image.load(path.lose_image)
lose = pygame.transform.scale(lose, (GAME_WIDTH, GAME_HEIGHT)) # thay đổi kích thước hình ảnh thua về kích thước màn hình game
win = pygame.transform.scale(pygame.image.load(path.win_image), (GAME_WIDTH, GAME_HEIGHT))

music = pygame.mixer.music.load(path.background_sound)
pygame.mixer.music.set_volume(1)


Wiz = Player(x, y)
Boss = boss(1300, 200, Wiz)
running = True
pygame.mixer.music.play(-1) # chạy nhạc nền vô hạn lần

my_font = pygame.font.SysFont('Comic Sans MS', 200)
text_surface = my_font.render('READY?', False, (0, 0, 0)) # tạo chữ READY?

pre_time = 60 # thời gian chờ trước khi bắt đầu trận đấu (60 frame = 1s)
help = True # tạo quả cầu máu cho player khi boss còn 50 HP


def run(runfile):
    with open(runfile, "r", encoding="utf8") as rnf:
        exec(rnf.read())

def pause():
    """
    Hàm tạm dừng game
    """
    pause = True
    while (pause):
        screen.blit(pygame.image.load(path.pause_image), (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1540, 800), 2)

        # kiểm tra ấn nút ESC để thoát khỏi menu pause
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and pygame.K_ESCAPE:
                pause = False

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    fpsClock.tick(FPS) # cập nhật màn hình mỗi 1/FPS giây

# main loop
while running:
    screen.blit(background, (0, 0)) # hiển thị background

    if Wiz.HP > 0 and Boss.HP > 0: # nếu cả 2 đều còn sống thì tiếp tục trận đấu
        if pre_time == 0: # nếu hết thời gian chờ thì bắt đầu trận đấu
            # giảm thời gian hồi chiêu của player
            if Wiz.cooldown> 0:
                Wiz.cooldown -= 1

            # boss tấn công trúng player thì player bị mất 5 HP
            if Boss.hit():
                Wiz.getHit(5)

            Wiz.controller() # điều khiển player
            # Wiz.Attack()
            Wiz.draw(screen) # vẽ player
            for At in Wiz.Attacks: # vẽ các đạn của player
                if At.hit(Boss): # nếu đạn của player chạm vào boss
                    Boss.getHit(At.dame) # boss bị mất hp bằng dame của đạn
                    Wiz.Attacks.remove(At) # xóa đạn
                else:
                    for Atb in Boss.Attacks: # kiểm tra đạn chạm vào đạn của boss không
                        if At.hit(Atb): # nếu đạn của player chạm vào đạn của boss
                            Wiz.createManaOrb(Atb.x, Atb.y) # tạo quả cầu mana cho player
                            Boss.Attacks.remove(Atb) # xóa đạn của boss
                            Wiz.Attacks.remove(At) # xóa đạn của player

            if Boss.HP == 50 and help == True: # nếu boss còn 50 HP thì tạo quả cầu máu cho player 1 lần
                Wiz.createHpOrb(Boss.x, Boss.y)
                help = False 

            Boss.Attack(Wiz) # boss tấn công
            Boss.draw(screen) # vẽ boss
            for Atb in Boss.Attacks: # vẽ các đạn của boss
                if Atb.hit(): # nếu đạn của boss chạm vào player
                    Wiz.getHit(Atb.dame) # player bị mất hp bằng dame của đạn
                    Boss.Attacks.remove(Atb) # xóa đạn của boss

        else: # chưa hết thời gian chờ
            # vẽ trước vị trí ban đầu của player và boss
            Wiz.draw(screen)
            Boss.draw(screen)

            if pre_time > 30: # nếu thời gian chờ còn nhiều hơn 30 frame thì hiển thị chữ READY?
                screen.blit(text_surface, (400, 250))

            else: # nếu thời gian chờ ít hơn 30 frame thì hiển thị chữ FIGHT!
                screen.blit(my_font.render(
                    'FIGHT!', False, (0, 0, 0)), (400, 250))
            pre_time -= 1

    else: # nếu 1 trong 2 bị chết thì hiển thị màn hình thua hoặc thắng
        pygame.mixer.music.stop()
        if Wiz.HP <= 0:
            screen.blit(lose, (0, 0))
        if Boss.HP <= 0:
            screen.blit(win, (0, 0))

        my_font = pygame.font.SysFont('Comic Sans MS', 50)
        text_surface = my_font.render('PRESS ENTER TO CONTINUE', False, (0, 0, 0))
        screen.blit(text_surface, (350, 500))


    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1540, 800), 1)

    # kiểm tra thoát khỏi game
    for event in pygame.event.get():
        if Wiz.HP <= 0 or Boss.HP <= 0:
            # neeus baam enter thi tieep tuwc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                run(".\game.py")
                running = False
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update() # cập nhật màn hình
    fpsClock.tick(FPS) # cập nhật màn hình mỗi 1/FPS giây
