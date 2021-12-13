from TextBar import InputBox
import os
import pygame
pygame.init()


font_name = pygame.font.match_font('font.ttf')
def draw_text(surf, text, size, x, y):
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


class Chess():
    def __init__(self):
        self.WHITE = (230, 230, 230)
        self.BLACK = (0, 0, 0)
    # end of Chess __init__()

    def draw(self, surf, center, player=0):
        radius = 20
        if player == 0:
            rect = pygame.draw.circle(surf, self.BLACK, center, radius)
        else:
            rect = pygame.draw.circle(surf, self.WHITE, center, radius)
    # end of Chess draw()
# end of class Chess

class Point(pygame.sprite.Sprite):
    def __init__(self, id, centerx, centery):
        pygame.sprite.Sprite.__init__(self)
        length = 20
        width = 20
        self.image = pygame.Surface((width, length))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.id = id
    # end of Point __init__()

    def chk_click(self, originx=0, originy=0):
        action = False
        mousex, mousey = pygame.mouse.get_pos()
        newpos = (mousex - originx, mousey - originy)
        bool_in = self.rect.collidepoint(newpos)
        if bool_in == True:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                # print('Click')
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action
    # end of Point chk_click()
# end of class Point

class ChessBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        BLACK = (0,0,0)
        length = 450
        width = 450
        self.UNIT = 45
        self.origin = (220, 75)
        self.image = pygame.Surface((width, length))
        self.image.fill((187, 199, 80))
        self.rect = self.image.get_rect()
        for i in range(1, 10):
            pygame.draw.line(self.image, BLACK, ((self.UNIT * i), 0), ((self.UNIT * i), length))
            pygame.draw.line(self.image, BLACK, (0, (self.UNIT * i)), (width, (self.UNIT * i)))
        self.points = []
        x = self.UNIT
        y = self.UNIT
        for i in range(1, 10):
            for j in range(1, 10):
                p = Point((i - 1, j - 1), x * j, y * i)
                self.points.append(p)
        self.rect.x = self.origin[0]
        self.rect.y = self.origin[1]
    # end of ChessBoard __init__()

    def chessEvent(self, player=0):
        for p in self.points:
            if p.chk_click(self.origin[0], self.origin[1]):
                chess = Chess()
                # draw chess on chessboard 0:BLACK 1(else):WHITE
                # chess.draw(self.image, p.rect.center, player)
                return p.id
    # end of ChessBoard chessEvent()

    def drawOpponentChess(self, player=0, pos=(0,0), size=9):
        index = (pos[0]*size + pos[1])
        print("index: ", index)
        chess = Chess()
        chess.draw(self.image, self.points[index].rect.center, player)
    # end of ChessBoard drawOpponentChess()

    def drawboard(self):
        BLACK = (0, 0, 0)
        self.image.fill((187, 199, 80))
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image,(192,80,80), self.rect.center,10)
        for i in range(1, 10):
            pygame.draw.line(self.image, BLACK, ((self.UNIT * i), 0), ((self.UNIT * i), self.rect.height))
            pygame.draw.line(self.image, BLACK, (0, (self.UNIT * i)), (self.rect.width, (self.UNIT * i)))
        self.rect.x = self.origin[0]
        self.rect.y = self.origin[1]
    # end of ChessBoard drawboard()
 
    def drawallpoints(self):
        color = (255, 255, 255)
        lineThickness = 1
        for p in self.points:
            self.pos = pygame.draw.rect(self.image, color, [p.rect.x, p.rect.y, p.rect.width, p.rect.height], lineThickness)
    # end of ChessBoard drawallpoints()
# end of class 

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self,surf):
        surf.blit(self.image, (self.rect.x, self.rect.y))

    def chk_click(self, originx=0, originy=0):
        action = False
        mousex, mousey = pygame.mouse.get_pos()
        newpos = (mousex - originx, mousey - originy)
        bool_in = self.rect.collidepoint(newpos)
        if bool_in == True:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                # print('Click')
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action


class StartExit():
    def __init__(self):
        start_img = pygame.image.load(os.path.join("img",'start_btn.png')).convert_alpha()
        exit_img = pygame.image.load(os.path.join("img",'exit_btn.png')).convert_alpha()
        self.start_button = Button(700, 150, start_img, 0.5)
        self.exit_button = Button(700, 350, exit_img, 0.5)

    def draw(self, surf):
        self.start_button.draw(surf)
        self.exit_button.draw(surf)
    
    def startclickevent(self):
        return self.start_button.chk_click()
    
    def exitclickevent(self):
        return self.exit_button.chk_click()


class LoginMenu():
    def __init__(self):
        length = 200
        width = 200
        self.origin = (10, 75)
        self.image = pygame.Surface((width, length))
        self.image.fill((120, 79, 70))
        # inputbar one
        username = InputBox(10, 10, 10, 32, 'username')
        # inputbar two
        password = InputBox(10, 70, 10, 32, 'password')
        self.input_boxes = [username, password]
        self.rect = self.image.get_rect()
        regist_img = pygame.image.load(os.path.join("img",'regist.png')).convert_alpha()
        login_img = pygame.image.load(os.path.join("img",'login.png')).convert_alpha()
        self.regist_button = Button(20, 130, regist_img, 0.7)
        self.login_button = Button(100, 130, login_img, 0.7)
        self.rect.x = self.origin[0]
        self.rect.y = self.origin[1]
    # end of LoginMenu __init__()

    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y))
        
        for box in self.input_boxes:
            box.update()
        self.image.fill((255, 255, 255))
        for box in self.input_boxes:
            box.draw(self.image)
        self.regist_button.draw(self.image)
        self.login_button.draw(self.image)

    def registclickevent(self):
        return self.regist_button.chk_click(self.rect.x, self.rect.y)
    
    def loginclickevent(self):
        return self.login_button.chk_click(self.rect.x, self.rect.y)
# end of LoginMenu draw()