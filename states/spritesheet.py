import pygame

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((255,255,255))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        width, height = sprite.get_width(), sprite.get_height()
        scale = 1
        sprite = pygame.transform.scale(sprite,(int(width*scale), int(height*scale)))
        return sprite

    def character_parse_sprite(self, w, h):
        surface_list = []
        num = 4
        for i in range(num):
            x = w * i
            image = self.get_sprite(x, 0, 32, 32)
            surface_list.append(image)
        return surface_list
    
    def map_parse_sprite(self, w, h):
        surface_list = []
        height = self.sprite_sheet.get_height()
        width = self.sprite_sheet.get_width()
        for i in range(height//h):
            for j in range(width//w):
                x = w * j
                y = h * i
                image = self.get_sprite(x, y, 32, 32)
                image.set_colorkey((255,255,255))
                surface_list.append(image)
        return surface_list