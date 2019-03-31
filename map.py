import pygame
from sprite import SpriteHandler, WallSprite, FloorSprite, HeroSprite
import random

# Map Generator Class, for randomly generating a map
# or for a constant map!
class Map:
    def __init__(self):
        self.viewport = pygame.Rect(0, 0, 400, 400)
        self.width = 400
        self.height = 400
        self.xset = int((400 - 32) / 2)
        self.yset = int((400 - 32) / 2)
    
    def animator(self, tile):
        return tile.rect.move(self.viewport.topleft)

    def viewport_update(self, tile):
        self.viewport.x = -tile.rect.x + self.xset
        self.viewport.y = -tile.rect.y + self.xset

    def generate(self, rogue):
        """Generate the map"""
        print("generating the map!")
        for i in range(4, 20):
            FloorSprite(rogue.tile_layers, rogue.sprite_handler, (i, 1))
        for i in range(6, 10):
            WallSprite(rogue.tile_layers, rogue.sprite_handler, (4,i))
        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (1, 1))
        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (1, 2))
        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (1, 3))

        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (4, 1))
        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (4, 2))
        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (4, 3))

        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (3, 1))
        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (3, 3))
        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (2, 3))

        WallSprite(rogue.tile_layers, rogue.sprite_handler, (4,4))
