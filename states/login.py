import pygame
import re
from states.my_state import State
from states.tile import Level


class LoginMenu(State):
    def __init__(self, game):
        State.__init__(self,game)
        self.username = InputBox(self, self.game, self.game.GAME_W*.5, self.game.GAME_H*.3, 200, 25, 'username')
        self.password = InputBox(self, self.game, self.game.GAME_W*.5, self.game.GAME_H*.5, 200, 25, 'password')
        self.username.active = True
        self.cursor_pos_x, self.cursor_pos_y  = self.username.rect.x-20, self.username.rect.y
        self.cursor_rect_x, self.cursor_rect_y = self.cursor_pos_x, self.cursor_pos_y
        self.menu_options = {0:"username", 1:"password", 2:"login", 4:"regist"}
        self.index = 0
        self.user_txt = ''
        self.psd_txt = ''

    def render(self, display):
        BLACK, WHITE = (0,0,0), (255,255,255)
        display.fill(WHITE)
        self.game.draw_text(display, "*", BLACK, self.cursor_rect_x, self.cursor_rect_y)
        self.game.draw_text(display, "login", BLACK, self.game.GAME_W*.3, self.game.GAME_H*.7)
        self.game.draw_text(display,"regist", BLACK, self.game.GAME_W*.7, self.game.GAME_H*.7)
        self.username.render(display)
        self.password.render(display)
    
    def update(self, delta_time, actions):
        self.start_update(actions)
        self.register_update(actions)
        self.update_cursor(actions)
        self.inputbox_active(actions)
        self.user_txt = self.username.update(actions)
        self.psd_txt = self.password.update(actions)
        self.game.reset_keys()

    
    def update_cursor(self, actions):
        if actions['down']:
            self.index = (self.index + 1) % len(self.menu_options)
            self.username.active ,self.password.active = False, False
        if actions['up']:
            self.index = (self.index - 1) % len(self.menu_options)
            self.username.active ,self.password.active = False, False
        if self.index==0 or self.index==1:
            self.cursor_rect_x = self.cursor_pos_x
            self.cursor_rect_y = self.cursor_pos_y + (self.index * (self.game.GAME_H*.5-self.game.GAME_H*.3))
        elif self.index==2:
            self.cursor_rect_x, self.cursor_rect_y = self.game.GAME_W*.3-80, self.game.GAME_H*.7
        elif self.index==3:
            self.cursor_rect_x, self.cursor_rect_y = self.game.GAME_W*.7-90, self.game.GAME_H*.7


    def inputbox_active(self, actions):
        if actions['action1']:
            self.username.active ,self.password.active = (False, True) if self.index else (True, False)
        if actions['action2']:
            self.username.active ,self.password.active = False, False

    def start_update(self, actions):
        if actions['start'] and self.index==2:
            self.game.client_socket.connect()
            c2flag = self.game.client_socket.login(self.user_txt, self.psd_txt)
            new_state = Level(self.game)
            new_state.enter_state()

    def register_update(self, actions):
        if actions['start'] and self.index==3:
            c2flag = self.game.client_socket.regist(self.user_txt, self.psd_txt)
            

class InputBox():
    def __init__(self, loginmenu, game, x, y, w, h, text=''):
        pygame.init()
        self.loginmenu = loginmenu
        self.game = game
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.FONT = pygame.font.Font(None, 20)
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.center = (x, y)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def update(self,actions):
        # Resize the box if the text is too long.
        # width = max(150, self.txt_surface.get_width()+10)
        # self.rect.w = width
        self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if self.loginmenu.index==0 or self.loginmenu.index==1:
            if actions['start']:
                temp = self.text
                print(self.text)
                self.text = ''
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)
                return temp
            if self.active:
                if actions['backspace']:
                    self.text = self.text[:-1]
                elif re.match(r'\w',self.game.word) and len(self.text)<9:
                    self.text += self.game.word
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def render(self, display):
        # Blit the text.
        self.game.draw_text(display, self.text, self.color, self.rect.centerx, self.rect.centery)
        # display.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(display, self.color, self.rect, 2)