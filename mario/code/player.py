import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particle):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.05
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        #dust particle
        self.import_dust_run_particle()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particle = create_jump_particle

        #Player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 9
        self.gravity = 0.8
        self.jump_speed = -16

        #Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    #Making the posture of player along the level
    def animate(self):
        animation = self.animations[self.status]

        #loop the running frame
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.facing_right == True:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image



            #set rect
            '''
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)'''
    
    def import_dust_run_particle(self):
        self.dust_run_particle = import_folder('../graphics/character/dust_particle/run')

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particle):
                self.dust_frame_index = 0
            
            dust_particle = self.dust_run_particle[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(0,10)
                self.display_surface.blit(dust_particle, pos)
            else:
                reverse_dust_particle = pygame.transform.flip(dust_particle, True, False)
                pos = self.rect.bottomleft - pygame.math.Vector2(-60,10)
                self.display_surface.blit(reverse_dust_particle, pos)


    #Import all player posture from png file
    def import_character_assets(self):
        character_path = '../graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    #Receive the input button and set speed of the player
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if self.on_ground == True:
                self.direction.y = self.jump_speed
                self.create_jump_particle(self.rect.midbottom)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0


    #Check the posture of player
    def get_status(self):
        if self.direction.y < 0:    #jump
            self.status = 'jump'
        elif self.direction.y > 1:  #fall
            self.status = 'fall'
        elif self.direction.x == 0: #y=0 and x=0 is stand still
            self.status = 'idle'
        else:                       #y=0 but x!=0 is run
            self.status = 'run'

    #Create the gravity speed
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y




    def update(self):
        self.get_input()
        self.animate()
        self.get_status()
        self.run_dust_animation()
