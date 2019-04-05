import pygame
from sprite import *
import random

# Map Generator Class, for randomly generating a map
# or for a constant map!
class Map:
    def __init__(self):
        """Create a new handler for map related interactions"""
        self.viewport = pygame.Rect(0, 0, 1024, 1024)
        self.width = 1024
        self.height = 1024
        self.xset = int((1024 - 256) / 2)
        self.yset = int((1024 - 256) / 2)

    def animator(self, tile):
        """Moves tiles according to the top left of the view port
        which has the offset applied. By changing the viewport
        when the hero location changes, we can take that and
        reposition all the other tiles relative to the hero.
        tile: the sprite object to move"""
        return tile.rect.move(self.viewport.topleft)

    def viewport_update(self, tile):
        """Update the position of the viewport. Note that
        reassigning any of the location attributes of pygame
        rectangles adjusts all the other attributes and does
        not resize the rectangle.
        tile: the sprite object to use to change the viewport"""
        self.viewport.x = -tile.rect.x + self.xset
        self.viewport.y = -tile.rect.y + self.xset

    def generate(self, rogue):
        """Places map sprites
        rogue: the roguelike game instance"""

        # randomly place floors
        for x in range(0, 20):
            for y in range(0,20):
                if random.random() > 0.2:
                    FloorSprite(rogue.tile_layers, rogue.sprite_handler, (x, y))

        # randomly place door
        is_door_placed = False
        for x in range(0, 20):
            for y in range(0, 20):
                if random.random() > 0.5 and not is_door_placed:
                    is_door_placed = True
                    DoorSprite(rogue.tile_layers, rogue.sprite_handler, (x, y))

        # randomly place items
        for x in range(0, 20):
            for y in range(0, 20):
                if random.random() < 0.09:
                    ItemSprite(rogue.tile_layers, rogue.sprite_handler, (x, y))

        # randomly place enemies
        for x in range(0, 20):
            for y in range(0, 20):
                if random.random() < 0.02:
                    characteristics = Characteristics(616,616,350,350, 66,0,36,1.6, [])
                    EnemySprite(rogue.tile_layers, rogue.sprite_handler, (x, y), characteristics)

        # place walls wherever there isn't a floor
        self.wall_placer(rogue)

    def wall_placer(self, rogue):
        """place walls wherever there isn't floor"""
        for x in range(-1,21):
            for y in range(-1, 21):
                overlap = False
                for tile in rogue.tile_layers["TILE_FLOOR"]:
                    if tile.pos.x == x and tile.pos.y == y:
                        overlap = True
                if not overlap:
                    WallSprite(rogue.tile_layers, rogue.sprite_handler, (x, y))
