import pygame, os
from states.spritesheet import Spritesheet
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.import_character_asset()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.current_frame, self.last_frame_update = 0,0
        self.image = self.walk_animations[0]
        self.rect = self.image.get_rect()
        self.is_jumping, self.on_ground = False, False
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0,0)
        self.gravity = 0.35
        self.friction = -.13
        self.acceleration = pygame.math.Vector2(0,self.gravity)
        self.jump_speed = -16
        
    
    def import_character_asset(self):
        asset_dir = os.path.join(os.getcwd(), "assets")
        sheetimg_dir = os.path.join(asset_dir, "four_walk.png")
        walk = Spritesheet(sheetimg_dir)
        self.walk_animations = walk.character_parse_sprite(32,32)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.walk_animations):
            self.frame_index = 0
        self.image = self.walk_animations[int(self.frame_index)]

    def horizontal_movement(self, delta_time, actions):
        delta_time *= 270
        self.acceleration.x = 0
        if actions['left']:
            self.acceleration.x -= .5
        elif actions['right']:
            self.acceleration.x += .5
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x = self.acceleration.x * delta_time
        self.position.x += self.velocity.x * delta_time + (self.acceleration.x * .5) * (delta_time * delta_time)
        self.rect.x = self.position.x

    def vertical_movement(self, delta_time, actions):
        if actions['space']:
            self.jump()
        else:
            if self.is_jumping:
                self.velocity.y *= .25
                self.is_jumping = False
        delta_time *= 120
        self.velocity.y += self.acceleration.y * delta_time
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += self.velocity.y * delta_time + (self.acceleration.y * .5) * (delta_time * delta_time)
        self.rect.bottom = self.position.y

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 15
            self.on_ground = False

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def checkCollisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:  # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y


    def update(self, delta_time, actions, tiles):
        self.horizontal_movement(delta_time, actions)
        self.checkCollisionsx(tiles)
        self.vertical_movement(delta_time, actions)
        self.checkCollisionsy(tiles)
        # Get the direction from inputs
        self.animate()
    
    

        


