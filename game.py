import pygame
import path
from modules.ui.menu import *

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1540, 800
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = path.font_name
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self) # khởi tạo menu chính
        self.options = OptionsMenu(self)
        self.tutorial = TutorialMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def check_events(self):
        """
        Hàm kiểm tra các sự kiện
        VD: bấm nút ESC để thoát game, phím mũi tên lên xuống, ...
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        """
        Hàm reset các phím về False
        """
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        """
        Hàm vẽ chữ lên màn hình
        text: nội dung cần vẽ
        size: kích thước chữ
        x, y: tọa độ của chữ
        """
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

g = Game()
icon = pygame.image.load(path.icon_image)
pygame.display.set_icon(icon)
pygame.display.set_caption("Wizard's disciple") 
music = pygame.mixer.music.load(path.menu_theme_sound)
pygame.mixer.music.play(-1)
while g.running:
    g.curr_menu.display_menu() # hiển thị menu và dieu hướng den các menu con hoặc game