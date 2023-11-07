import pygame
import path
from constants import *

background = pygame.transform.scale(pygame.image.load(path.background_image), (GAME_WIDTH, GAME_HEIGHT))

# run file game
def run(runfile):
    with open(runfile, "r", encoding="utf8") as rnf:
        exec(rnf.read())

# tọa độ menu
menuPosX = GAME_WIDTH / 2
menuPosY = GAME_HEIGHT / 2

class Menu():
    def __init__(self, game):
        self.game = game
        self.run_display = True # có đang chạy game hay không
        self.cursor_rect = pygame.Rect(0,0,0,0) # set kich thuoc và vẽ viền cho con trỏ
        self.offset = -150

    def draw_cursor(self):
        cursor = (self.cursor_rect.x, self.cursor_rect.y - 20, 300, 80)
        pygame.draw.rect(self.game.display, (0, 0, 0), cursor, 2)
        #vẽ khung này trên display, màu đen, kích thước là cursor, độ dày là 2
    # vẽ lại menu trên màn hình
    def blit_screen(self): # hiển thị màn hình
        self.game.window.blit(self.game.display, (0, 0)) # hiển thị màn hình, vị trí là (0,0)
        pygame.display.update() #gọi hàm update
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game) # khởi tạo class cha
        self.state = "Start" # set trạng thái ban đầu là Start
        self.startx, self.starty = menuPosX, menuPosY  # set tọa độ cho button Start
        self.optionsx, self.optionsy = menuPosX, menuPosY + 65 # set tọa độ cho button Options
        self.tutorialx, self.tutorialy = menuPosX, menuPosY + 130# set tọa độ cho button Tutorial
        self.creditsx, self.creditsy = menuPosX, menuPosY + 195 # set tọa độ cho button Credits
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty - 20) # set tọa độ cho con trỏ

    def display_menu(self):
        self.run_display = True
        while self.run_display:  # khi mà đang chạy chương trình
            self.game.check_events()  # hàm check event để kiểm tra sự kiện bấm nút
            self.check_input()
            self.game.display.blit(background,(0,0))
            self.game.draw_text('Main Menu', 70, menuPosX, menuPosY - 80) #set kích thước chữ và vị trí của nó
            self.game.draw_text("Start Game", 50, self.startx, self.starty) # set kích thước chữ và vị trí của start Game
            self.game.draw_text("Options", 50, self.optionsx, self.optionsy) # set kích thước chữ và vị trí của Options
            self.game.draw_text("Tutorial", 50, self.tutorialx, self.tutorialy) # set kích thước chữ và vị trí của Tutorial
            self.game.draw_text("Credits", 50, self.creditsx, self.creditsy) # set kích thước chữ và vị trí của Credits
            self.draw_cursor() # vẽ con trỏ (ô vuông ở chỗ chọn menu)
            self.blit_screen() # hiển thị màn hình

    def move_cursor(self): # hàm di chuyển con trỏ
        if self.game.DOWN_KEY: # nếu bấm nút mũi tên xuống sẽ thay đổi các trạng thái và tọa độ của con trỏ
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy - 20)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy - 20)
                self.state = 'Tutorial'
            elif self.state == 'Tutorial':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy - 20)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty - 20)
                self.state = 'Start'
        elif self.game.UP_KEY: # nếu bấm nút mũi tên lên thì sẽ thay đổi các trạng thái và tọa độ của con trỏ
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy - 20)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty - 20)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy - 20)
                self.state = 'Tutorial'
            elif self.state == 'Tutorial':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy   - 20)
                self.state = 'Options'

    def check_input(self):  #kiểm tra đầu vào
        self.move_cursor() # gọi hàm di chuyển con trỏ, đọc xem là có bấm nút nào để con trỏ di chuyển không
        if self.game.START_KEY: # nếu bấm nút enter
            if self.state == 'Start': # nếu đang ở trạng thái Start
                self.game.playing = True # băt đầu chơi
                run(".\modules\play_scene.py") #chạy file play_scene.py
            elif self.state == 'Options': # nếu đang ở trạng thái Options
                self.game.curr_menu = self.game.options # chuyển sang menu Options
            elif self.state == 'Tutorial': # nếu đang ở trạng thái Tutorial
                self.game.curr_menu = self.game.tutorial # chuyển sang menu Tutorial
            elif self.state == 'Credits': # nếu đang ở trạng thái Credits
                self.game.curr_menu = self.game.credits # chuyển sang menu Credits
            self.run_display = False # dừng hiển thị menu


class OptionsMenu(Menu): # class OptionsMenu kế thừa class Menu
    def __init__(self, game):
        Menu.__init__(self, game) # khởi tạo lớp cha Menu
        self.volx, self.voly = self.game.DISPLAY_W/2-20, self.game.DISPLAY_H/2-40 # set tọa độ cho ô Volume
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly) # set tọa độ cho con trỏ

    def display_menu(self): # hiển thị menu trong Options
        self.run_display = True # hiển thị màn hình
        self.volume = 1 # volume = 1
        while self.run_display: # nếu đang chạy scene Options này
            self.game.check_events() # kiểm tra sự kiện
            self.check_input() # kiểm tra input xem có bấm nút nào không
            self.game.display.blit(background,(0,0)) # hiển thị menu, vị trí là (0,0)
            self.game.draw_text('Options', 40, self.game.DISPLAY_W/2-20, self.game.DISPLAY_H/2 - 90)# set kích thước chữ và vị trí của nó
            self.game.draw_text("Volume", 25, self.volx, self.voly) # set kích thước chữ và vị trí của Volume
            pygame.draw.rect(self.game.display,(0,0,0),(self.cursor_rect.x-135, self.cursor_rect.y+30,500,30),2) # vẽ viền cho ô Volume
            pygame.draw.rect(self.game.display,(100,100,100),(self.cursor_rect.x-135+2, self.cursor_rect.y+30+2,500*self.volume-4,30-4))
            self.blit_screen() # hiển thị màn hình

    def check_input(self):
        if self.game.BACK_KEY: # nếu bấm nút back
            self.game.curr_menu = self.game.main_menu # hiển thị màn hình chính
            self.run_display = False # không hiển thị màn này nữa
        elif self.game.START_KEY: # nếu bấm nút enter
            pass
        keys = pygame.key.get_pressed() # lấy ra danh sách nút đc bấm
        if keys[pygame.K_RIGHT] and self.volume <= 0.9:
            self.volume += 0.1 # tăng giảm âm lượng
        if keys[pygame.K_LEFT] and self.volume >= 0.1:
            self.volume -= 0.1


class CreditsMenu(Menu): # màn hình Credits
    def __init__(self, game):
        Menu.__init__(self, game) # khởi tạo cha

    def display_menu(self):
        self.run_display = True # khởi tạo là đang chạy màn hình
        while self.run_display: #khi mà đang chạy màn hình thì
            self.game.check_events() #kiểm tra các sự kiện
            if self.game.START_KEY or self.game.BACK_KEY: # nếu bấm nút là nút enter hoặc nút back
                self.game.curr_menu = self.game.main_menu # chuyển màn hiện tại là màn menu
                self.run_display = False #trạng thái không chạy game
            self.game.display.blit(background, (0, 0)) # hiển thị back, vị trí là (0,0)
            #set text cho tiêu đề và intro
            self.game.draw_text(
                'Credits', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 110)
            self.game.draw_text("Made by team 3:", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text("Le Quy Long - B21DCCN076", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.game.draw_text("Nguyen Anh Quan - B21DCCN103", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50)
            self.game.draw_text("Duong Van Toan - B21DCCN715", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 +100)
            self.game.draw_text("Kieu Linh Trang - B21DCCN716", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 +150)
            self.game.draw_text("Le Van Duy - B21DCCN296", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 +200)
            self.blit_screen()


class TutorialMenu(Menu): #màn hình tutorial
    def __init__(self, game):
        Menu.__init__(self, game) #khởi tạo lớp cha

    def display_menu(self):
        self.run_display = True # đang chạy màn hình
        while self.run_display: # nếu đang chạy màn hình thì
            self.game.check_events() #đọc các sự kiện
            if self.game.START_KEY or self.game.BACK_KEY: # nếu bấm nút enter hoặc nút back
                self.game.curr_menu = self.game.main_menu # chuyển về màn hình menu
                self.run_display = False
            #load ảnh tutorial lên màn hình
            self.game.display.blit(
                pygame.image.load(path.tutorial_image), (0, 0))
            self.blit_screen()
