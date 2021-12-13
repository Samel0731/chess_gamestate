import numpy as np


class Data():
    def __init__(self):
        self.size = 9
        self.ds = np.zeros([self.size, self.size])
        self.ds.fill(-1)
        self.round_count = 0
        self.win = 0
        self.player = 0

    def update(self, pos, player):
        if self.ds[pos] < 0:
            assert player==0 or player==1, f"player number wrong{player}"
            self.ds[pos] = player
            print("update: ", self.ds[pos])
            return True
        else:
            print("already exist chess!")
            return False

    def reset(self):
        self.ds.fill(-1)
        self.round_count = 0
        self.win = 0
        self.player = 0
        self.win = 0

    def judge(self, pos, player):
        (r, c) = pos
        # self.round_count += 1
        # self.player = (self.round_count) % 2
        self.player = player
        # print("self.player:", self.player,"player", self.round_count)
        vicConditions = 5
        # 1 row
        count = 0
        for i in range(self.size):
            if self.ds[r, i] == self.player:
                count += 1
                if count == vicConditions:
                    print("player", self.player, " win!")
                    self.win = 1
                    return 1
            else:
                count = 0

        # 2 col
        count = 0
        for i in range(self.size):
            if self.ds[i, c] == self.player:
                count += 1
                if count == vicConditions:
                    # print("player ", player, " win!")
                    print("player", self.player, " win!")
                    self.win = 1
                    return 1
            else:
                count = 0

        # 3
        count = 0
        i = 0
        while r-i>0 and c-i>0:
            i += 1
        f_i = r - i
        f_j = c - i

        while f_i<self.size and f_j<self.size:
            if self.ds[f_i, f_j] == self.player:
                count += 1
                if count == vicConditions:
                    # print("player ", player, " win!")
                    print("player", self.player, " win!")
                    self.win = 1
                    return 1
            else:
                count = 0
            f_i+=1
            f_j+=1

        # 4
        count = 0
        i = 0
        while r+i<(self.size - 1) and c-i>0:
            i += 1
        f_i = r + i
        f_j = c - i

        while f_i>=0 and f_j<self.size:
            if self.ds[f_i, f_j] == self.player:
                count += 1
                if count == vicConditions:
                    # print("player ", player, " win!")
                    print("player", self.player, " win!")
                    self.win = 1
                    return 1
            else:
                count = 0
            f_i-=1
            f_j+=1





# class Data():
#     def __init__(self):
#         self.size = 9
#         self.ds = np.zeros([self.size, self.size])
#         self.ds.fill(-1)
#         self.round_count = 0
#         self.win = 0
#         self.player = 0

#     def update(self, pos):
#         if self.ds[pos] < 0:
#             self.ds[pos] = (self.round_count+1) % 2
#             print("update: ", self.ds[pos])
#             return True
#         else:
#             print("already exist chess!")
#             return False

#     def reset(self):
#         self.ds.fill(-1)
#         self.round_count = 0
#         self.win = 0
#         self.player = 0
#         self.win = 0

#     def judge(self, pos):
#         (r, c) = pos
#         self.round_count += 1
#         self.player = (self.round_count) % 2
#         # print("self.player:", self.player,"player", self.round_count)
#         vicConditions = 5
#         # 1 row
#         count = 0
#         for i in range(self.size):
#             if self.ds[r, i] == self.player:
#                 count += 1
#                 if count == vicConditions:
#                     print("player", self.player, " win!")
#                     self.win = 1
#                     return 1
#             else:
#                 count = 0

#         # 2 col
#         count = 0
#         for i in range(self.size):
#             if self.ds[i, c] == self.player:
#                 count += 1
#                 if count == vicConditions:
#                     # print("player ", player, " win!")
#                     print("player", self.player, " win!")
#                     self.win = 1
#                     return 1
#             else:
#                 count = 0

#         # 3
#         count = 0
#         i = 0
#         while r-i>0 and c-i>0:
#             i += 1
#         f_i = r - i
#         f_j = c - i

#         while f_i<self.size and f_j<self.size:
#             if self.ds[f_i, f_j] == self.player:
#                 count += 1
#                 if count == vicConditions:
#                     # print("player ", player, " win!")
#                     print("player", self.player, " win!")
#                     self.win = 1
#                     return 1
#             else:
#                 count = 0
#             f_i+=1
#             f_j+=1

#         # 4
#         count = 0
#         i = 0
#         while r+i<(self.size - 1) and c-i>0:
#             i += 1
#         f_i = r + i
#         f_j = c - i

#         while f_i>=0 and f_j<self.size:
#             if self.ds[f_i, f_j] == self.player:
#                 count += 1
#                 if count == vicConditions:
#                     # print("player ", player, " win!")
#                     print("player", self.player, " win!")
#                     self.win = 1
#                     return 1
#             else:
#                 count = 0
#             f_i-=1
#             f_j+=1