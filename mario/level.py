import pygame
from tiles import Tile
from settings import tile_size


#TClass for setting up the shape of the block
class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0


    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()

        for row_index,row in enumerate(layout):
            for column_index,cell in enumerate(row):
                if cell == 'X':
                    x = column_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)


    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)