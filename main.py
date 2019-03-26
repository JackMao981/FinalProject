# grab the pygame library
import pygame

# grab some system libraries for dealing with sprite files
import sys
import os
import math
import random

from map import Map
from sprite import *

# Game Class, for handling game loop eventually
class RogueLike:
    pass


if __name__ == "__main__":

    # initialize pygame with some boilerplate stuff
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    # load the sprite image set
    sprite_handler = SpriteHandler()

    tile_layers = {
        "TILE_WALL": pygame.sprite.Group(),
        "TILE_FLOOR": pygame.sprite.Group(),
        "TILE_HERO": pygame.sprite.Group()}

    # place some floor!
    FloorSprite(tile_layers, sprite_handler, (1, 1))
    FloorSprite(tile_layers, sprite_handler, (1, 2))
    FloorSprite(tile_layers, sprite_handler, (1, 3))

    FloorSprite(tile_layers, sprite_handler, (4, 1))
    FloorSprite(tile_layers, sprite_handler, (4, 2))
    FloorSprite(tile_layers, sprite_handler, (4, 3))

    FloorSprite(tile_layers, sprite_handler, (3, 1))
    FloorSprite(tile_layers, sprite_handler, (3, 3))
    FloorSprite(tile_layers, sprite_handler, (2, 3))

    WallSprite(tile_layers, sprite_handler, (4,4))
    #HeroSprite(tile_layers, sprite_handler, (5,5))
    # run the game loop forever (for now just force quit)
    run = True
    while run:
        # need to get this to stop program
        # from freezing
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        # fill the screen with bg color
        screen.fill(pygame.Color(0,0,0))

        # iterate through all tile layers,
        # drawing the tile specified in sprite
        # object locations
        for layer in tile_layers:
            for tile in tile_layers[layer]:
                tile_layers["TILE_WALL"].update()
                tile_layers["TILE_FLOOR"].update()
                screen.blit(tile.tile, tile.rect.move(0, 0))
        pygame.display.flip()
    pygame.quit()
