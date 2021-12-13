####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 6-MultiThreadRPCServer.py                                                  
#  This program demos a multithreaded RPC server                   
#  2021.08.12                                                                                     
####################################################
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading
import random
import numpy as np


PORT = 8888
EnableCS = True
namelist = []
first = False
second = False
gameroom = [0,1]
room_id = 0
roomlist = []

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# class GameLobby:
#     def __init__(self):
#         self.lobby = list()
    
#     def create_room(self, name1, name2):
#         room = dict()
#         room['playermove'] = list()
#         room['player1-name'] = name1
#         room['player2-name'] = name2
#         room['player1-role'], room['player2-role'] = self.decide_black_white()
#         self.lobby.append(room)
#         return len(self.lobby)-1
    
#     def decide_black_white(self):
#         player1 = random.randint(0,500) % 2
#         player2 = 1 - player1
#         return player1, player2

class Room:
    def __init__(self):
        global room_id
        self.id = room_id
        room_id+=1
        self.player1_name = []
        self.player2_name = []
        self.coord = []
    def addPlayer(self,player_name):
        if not self.player1_name:
            self.player1_name = player_name
            return 1
        elif not self.player2_name:
            self.player2_name = player_name
            return 1
        else:
            return -1   
    def rmovPlayer(self,player_name):
        if self.player1_name == player_name:
            self.player1_name = []
        elif self.player2_name == player_name:
            self.player2_name = []
        else:
            flag=-1
for i in range(10):
    temp_room = Room()
    roomlist.append(temp_room)

class client_methods:
    def __init__(self):
        self.shared_variable = 0
        if(EnableCS):
            self.lock = threading.Lock()
    def register(self,name,password):
        i = 0
        flag = 0
        for i in namelist:
            if i[1]==name:
                flag=1    
        if flag==0:
            namelist.append(["name",name," password",password])
            return 1
        else:
            return 0
    def login(self,name,password):
        # flag: 0(count not found),1(login success),2(wrong password)
        flag=0
        for i in namelist:
            if name == i[1]:
                if password == i[3]:
                    flag = 1
                else:flag=2
        return flag
    def server_receive_data(self,roomid,id):
        print("recv",id)
        roomlist[roomid].coord = id
        return False
    def server_send_data(self,roomid):
        return roomlist[roomid].coord
    def clear_dataid(self,roomid):
        roomlist[roomid].coord = []
        return len(roomlist[roomid].coord)
    def get_game_room(self):
        global first, second
        if first != True:
            first = True
            return gameroom[0]
        elif second != True:
            second = True
            return gameroom[1]
    
    def enterroom(self,name,roomid):
        flag = roomlist[roomid].addPlayer(name)
        return flag
    def exitroom(self,name,roomid):
        flag = roomlist[roomid].rmovPlayer(name)
        return flag



def main():
    obj = client_methods()
    # server = SimpleXMLRPCServer(('localhost', PORT))
    server = SimpleXMLRPCServer(('10.22.70.109', PORT))
    # server = ThreadXMLRPCServer(('10.21.15.175', PORT))    
    server.register_instance(obj)
    print('Listen on port  %d' % PORT)
    try:
        print('Use Control-C to exit!')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server exit')
# end of main

if __name__ == '__main__':
    main()
