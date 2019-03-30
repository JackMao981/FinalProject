import pygame
from sprite import SpriteHandler, WallSprite, FloorSprite, HeroSprite
import random

# Map Generator Class, for randomly generating a map
# or for a constant map!
class Map:
    def __init__(self):
        pass

    def generate(self, rogue):
        """Generate the map"""
        print("generating the map!")
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
