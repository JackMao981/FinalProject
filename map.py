import pygame
from sprite import SpriteHandler, WallSprite, FloorSprite, HeroSprite
import random

# Map Generator Class, for randomly generating a map
# or for a constant map!
class Map:
    def __init__(self):
        """Create a new handler for map related interactions"""
        self.viewport = pygame.Rect(0, 0, 700, 700)
        self.width = 700
        self.height = 700
        self.xset = int((700 - 32) / 2)
        self.yset = int((700 - 32) / 2)
    
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

        # randomly place floors
        for x in range(0, 20):
            for y in range(0,20):
                if random.random() > 0.2:
                    FloorSprite(rogue.tile_layers, rogue.sprite_handler, (x, y))

        # place walls wherever there isn't a floor
        self.wall_placer(rogue)

    def wall_placer(self, rogue):
        """place walls wherever there isn't floor"""
        for x in range(-5,25):
            for y in range(-5, 25):
                overlap = False
                for tile in rogue.tile_layers["TILE_FLOOR"]:
                    if tile.pos.x == x and tile.pos.y == y:
                        overlap = True

                if not overlap:
                    WallSprite(rogue.tile_layers, rogue.sprite_handler, (x, y))
