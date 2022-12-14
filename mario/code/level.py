import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect


#Class for setting up the level of the game
class Level:
    def __init__(self, level_data, surface):
        #Setup the level
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

        #Set up dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    #Method for creating the jumping dust particle
    def create_jump_particle(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    #These two methods check whether
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    #Method to place blocks and origin of the player
    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index,row in enumerate(layout):
            for column_index,cell in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    player_Sprite = Player((x,y), self.display_surface, self.create_jump_particle)
                    self.player.add(player_Sprite)


    #Method to scroll background and stop player
    #when player is at the edge of background
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < (screen_width/3) and direction_x < 0:
            self.world_shift = 9
            player.speed = 0
        elif player_x > (screen_width - screen_width/3)and direction_x > 0:
            self.world_shift = -9
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 9

    #Move player horizontally with collision detected
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:      #left
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:    #right
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False

        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
                    

    #Move player vertically with collision detected
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 1:      #down
                    player.rect.bottom = sprite.rect.top
                    player.on_ground = True
                elif player.direction.y < 0:    #up
                    player.rect.top = sprite.rect.bottom
                    player.on_ceiling = True
                player.direction.y = 0
        
        if player.on_ground and (player.direction.y < 0 or player.direction.y > 1):
            player.on_ground = False
        
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False


    def run(self):
        #draw dust particle
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)


        #draw tile block
        self.tiles.draw(self.display_surface)
        #scrolling the camera
        self.tiles.update(self.world_shift)
        #Scroll background and stop player
        self.scroll_x()

        #draw player
        self.player.draw(self.display_surface)
        #Update position of player
        self.player.update()
        #horizontal movement and collision
        self.horizontal_movement_collision()
        #Check whether player is on ground or not
        self.get_player_on_ground()
        #vertical movement and collision
        self.vertical_movement_collision()
        #Check whether player is on ground or not
        self.create_landing_dust()
