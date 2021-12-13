####################################################
#  Network Programming - Unit 6 Remote Procedure Call          
#  Program Name: 6-MultiThreadRPCClient.py                                                  
#  This program demos a simple RPC client                   
#  2021.08.12                                                                                  
####################################################
import xmlrpc.client
import time

# ip
ip = '10.22.70.109'
PORT = 8888

class ClientSocket:
    def __init__(self):
        self.server = xmlrpc.client.ServerProxy('http://' + ip + ':' + str(PORT))
        # regist flag
        self.logflag = 0
        self.c1flag = None

    def regist(self, new_user, new_password):
        print('Add new user')
        # new_user = input('User name: ')
        # new_password = input('Password:')
        self.c1flag = self.server.register(new_user,new_password)
        if self.c1flag==1:
            print("\nResgist successfully!\n")
        else:
            print("\nRegist failed!Duplicate username\n")
    
    def login(self, user_name, user_password):
        if self.c1flag == 1:
            print('log in')
            # user_name = input('Your name: ')
            # user_password = input('Your password:')
            creat_time = time.strftime("%H:%M:%S")
            c2flag = self.server.login(user_name,user_password)
            if c2flag==0:
                print("\nCount not found!\nPlease input correct count's name\n")
            elif c2flag==1:
                print("\nLogin success!\nLogin time:",creat_time,"\n")
                self.logflag=1
            elif c2flag==2:
                print("\nWrong password!\nPlease try again\n")
            return c2flag
        elif self.c1flag == 0:
            print("Please register first!")
    
    def send2Server(self, buf):
        id = buf
        self.server.server_receive_data(id)
    
    def recvfromServer(self):
        return self.server.server_send_data()

    def get_game_room(self):
        return self.server.get_game_room()
    
    def clear_dataid(self):
        self.server.clear_dataid()

if __name__ == '__main__':
    print("Hello")
