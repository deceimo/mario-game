import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #Player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 9
        self.gravity = 0.8
        self.jump_speed = -16
    
    #Making the posture of player along the level
    def animate(self):
        animation = self.animations['jump']

        #loop the running frame
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]


    #Import all player posture from png file
    def import_character_assets(self):
        character_path = '../graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    #Receive the input button of the player
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.jump()
        else:
            self.direction.x = 0

    #Create the gravity speed
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    #Set the jump speed
    def jump(self):
        self.direction.y = self.jump_speed


    def update(self):
        self.get_input()
        self.animate()
