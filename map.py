import pygame
from sprite import SpriteHandler, WallSprite, FloorSprite, HeroSprite
import random

# Map Generator Class, for randomly generating a map
# or for a constant map!
class Map:
    def __init__(self):
        """Create a new handler for map related interactions"""
        self.viewport = pygame.Rect(0, 0, 400, 400)
        self.width = 400
        self.height = 400
        self.xset = int((400 - 32) / 2)
        self.yset = int((400 - 32) / 2)
    
    def animator(self, tile):
        """Moves tiles according to the top left of the view port
        which has the offset applied. By changing the viewport 
        when the hero location changes, we can take that and 
        reposition all the other tiles relative to the hero."""
        return tile.rect.move(self.viewport.topleft)

    def viewport_update(self, tile):
        """Update the position of the viewport. Note that 
        reassigning any of the location attributes of pygame
        rectangles adjusts all the other attributes and does
        not resize the rectangle."""
        self.viewport.x = -tile.rect.x + self.xset
        self.viewport.y = -tile.rect.y + self.xset

    def generate(self, rogue):
        """Places map sprites"""

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

        FloorSprite(rogue.tile_layers, rogue.sprite_handler, (4, 1))

        # # place walls wherever there isn't floor
        # for x in range(0,30):
        #     for y in range(0, 30):
        #         overlap = False
        #         for tile in rogue.tile_layers["TILE_FLOOR"]:
        #             if tile.pos.x == x and tile.pos.y == y:
        #                 overlap = True

        #         if not overlap:
        #             WallSprite(rogue.tile_layers, rogue.sprite_handler, (x, y))
