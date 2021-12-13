from Client_Program import ClientSocket
from View import ChessBoard
from View import LoginMenu
from View import StartExit
from Data import Data
import pygame


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


def main():
    # Variables
    FPS = 120
    HEIGHT = 600
    WIDTH = 890
    titleName = "Gomoku"
    backgroundColor = (202, 228, 241)
    onlineflag = True
    onlineplayer = 0
    myturn = True
    login_username = ''
    iwanttoplaygame = False
    
    # State window control
    show_chessboard = True
    show_loginmenu = True
    show_startexit = True

    # pygame init, pygame setting 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(titleName)
    pygame.mouse.set_visible(1)

    # Object
    clock = pygame.time.Clock()
    singledata = Data()
    loginmenu = LoginMenu()
    startexit = StartExit()
    client_socket = None
    if onlineflag:
        client_socket = ClientSocket()
        onlineplayer = client_socket.get_game_room()
        if onlineplayer==0:
            myturn = True
        elif onlineplayer==1:
            myturn = False
        print("onlineplayer: {}myturn: {}".format(onlineplayer, myturn))


    # Sprites
    all_sprites = pygame.sprite.Group()
    chessboard = ChessBoard()
    all_sprites.add(chessboard)

    # Game
    running = True
    while running:
        clock.tick(FPS)
        # handle Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if show_loginmenu:
                for box in loginmenu.input_boxes:
                    box.handle_event(event,(10, 75))

        
        # design game surface
        screen.fill(backgroundColor)
        # login window
        if show_loginmenu:
            loginmenu.draw(screen)
            if loginmenu.registclickevent():
                username = loginmenu.input_boxes[0].gettext()
                password = loginmenu.input_boxes[1].gettext()
                print(username, password)
                client_socket.regist(username, password)
                print("regist click")
            if loginmenu.loginclickevent():
                username = loginmenu.input_boxes[0].gettext()
                password = loginmenu.input_boxes[1].gettext()
                print(username, password)
                c2flag = client_socket.login(username, password)
                if c2flag==1:
                    login_username = username
                    show_loginmenu = False
                print("login click")
        if login_username != '':
            draw_text(screen, username, 30, 100, 10)
        if iwanttoplaygame:
            # start & exit button
            if show_startexit:
                startexit.draw(screen)
                if startexit.startclickevent():
                    print("start clicked")
                    singledata.reset()
                    chessboard.drawboard()
                    chessboard.drawallpoints()
                    if onlineflag:
                        client_socket.clear_dataid()
                    show_startexit = False
                if startexit.exitclickevent():
                    print("exit clicked")
                    running = False
                    show_startexit = False
            # chessboard (game start)
            if show_chessboard:
                if not show_startexit:
                    if not onlineflag:# 單機
                        pos = chessboard.chessEvent(singledata.player)
                        if pos != None:
                            if singledata.update(pos):
                                chessboard.drawOpponentChess(singledata.player, pos)
                                win = singledata.judge(pos)
                                if win == 1:
                                    print("win=1")
                                    show_startexit = True
                    if onlineflag:# 線上
                        if myturn:
                            pos = chessboard.chessEvent(onlineplayer)
                            if pos != None:
                                if singledata.update(pos,onlineplayer):
                                    chessboard.drawOpponentChess(onlineplayer, pos)
                                    client_socket.send2Server(pos)
                                    win = singledata.judge(pos,onlineplayer)
                                    if win == 1:
                                        print("win=1")
                                        show_startexit = True
                                    myturn = False
                        elif not myturn:
                            pos = client_socket.recvfromServer()
                            print(pos)
                            if len(pos):
                                pos = tuple(pos)
                                if singledata.update(pos,(onlineplayer+1)%2):
                                    chessboard.drawOpponentChess((onlineplayer+1)%2, pos)
                                    win = singledata.judge(pos,(onlineplayer+1)%2)
                                    if win == 1:
                                        print("win=1")
                                        show_startexit = True
                                    myturn = True

            # show Points click range
            chessboard.drawallpoints()
            all_sprites.draw(screen)

        pygame.display.update()
    pygame.quit()
# end of main

if __name__ == '__main__':
    main()