import pygame, os, csv
from my_state import State
from spritesheet import Spritesheet
from player import Player

asset_dir = os.path.join(os.getcwd(), "asset")
class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,surface,size=32,csv_id=-1):
        pygame.sprite.Sprite.__init__(self)
        self.csv_value = csv_id
        self.image = surface
        # self.image = pygame.Surface((size,size))
        # self.image.fill("gray")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y

    def setcsvvalue(self, value):
        self.csv_value = value
        
    
    # def draw(self, surface):
    #     surface.blit(self.image, (self.rect.x, self.rect.y))

class Level(State):
    def __init__(self,game):
        State.__init__(self,game)
        self.background = pygame.image.load(os.path.join(os.getcwd(), "asset","lobby.png"))
        self.background.set_colorkey((255,255,255))
        self.player = pygame.sprite.GroupSingle()
        
        player_sprite = Player(self.game)
        player_sprite.position.x, player_sprite.position.y = 0, 0
        self.player.add(player_sprite)
        # self.background = pygame.transform.scale(self.background, (int(width * (480/width)), int(height * (270/height))))
        self.level = list()
        with open(os.path.join(os.getcwd(), "asset","lobby_level.csv")) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                self.level.append(list(row))
        self.map = list()
        
        self.setup_level(self.level)

    def setup_level(self,layout):
        asset_dir = os.path.join(os.getcwd(), "asset")
        sheet_dir = os.path.join(asset_dir, "sheet_32.png")
        sheet_object = Spritesheet(sheet_dir)
        self.mapsheet = sheet_object.map_parse_sprite(32,32)
        self.tiles = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                cell_value = int(cell)
                if cell_value>-1 and cell_value!= 109 and cell_value!=92 and cell_value!=75:
                    x = int(column_index * 32)
                    y = int(row_index * 32)
                    tile = Tile(x,y,self.mapsheet[cell_value],cell_value)
                    
                    self.map.append(tile)
                    self.tiles.add(tile)
    
    def update(self, delta_time, actions):
        self.player.update(delta_time, actions, self.map)

    def render(self, display):
        display.fill((255,255,255))
        display.blit(self.background,(0,0))
        self.tiles.draw(display)
        self.player.draw(display)
        


