import pygame
from states.my_state import State

class ChessGame(State):
    def __init__(self, game):
        State.__init__(self,game)
        self.game = game
        self.chessboard = ChessBoard()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.chessboard)
        self.onlineplayer = 0
        
 
    def render(self, display):
        display.fill((255,255,255))
        # self.game.draw_text(display, "PARTY MENU GOES HERE", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2 )
        
        # self.chessboard.drawboard()
        self.chessboard.drawallpoints()
        # self.chessboard.drawOpponentChess()
        self.all_sprites.draw(display)

    def update(self, delta_time, actions):
        pos = self.chessboard.chessEvent(self.onlineplayer)
        if pos != None:
            self.chessboard.drawOpponentChess(self.onlineplayer, pos)
        self.game.reset_keys()

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