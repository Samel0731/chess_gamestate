import pygame
from states.my_state import State

class chessboard(State):
    def __init__(self, game):
        State.__init__(self,game)
        