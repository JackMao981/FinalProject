# grab the pygame library
import pygame

# grab some system libraries for dealing with sprite files
import sys
import os
import math
import random

from map import Map

# !!SPRITE HANDLING!!

# Define where objects are in our sprite file.
# Each sprite is 4x4 pixels in size, and the
# image is 32x32 pixels in size, to allow for
# future expansion in our tileset.
# transparent content in the sprite sheet is
# the traditional pink. this decision was made
# because I looked at lots of spritesheets and
# they all used pink pretty much
WALL_TILE = [(0, 0)]
FLOOR_TILE = [(1, 0)]
PLAYER_TILE = [(0, 2)]

SPRITE_PATH = "sprites/sprites_simple.bmp"


# Sprite class to handle common sprite operations
class SpriteHandler:
    def __init__(self):
        # load the texture file into a surface
        # the beginner guide on pygame told me
        # that .convert increases render speed
        self.tilemap = pygame.image.load(SPRITE_PATH).convert()
        self.tilemap_width, self.tilemap_height = self.tilemap.get_size() # 32 x 32

        # set per-tile size
        self.tile_width = 4
        self.tile_height = 4

        # make a coordinate system in terms of tile size
        # e.g. 32x32 divided into 4x4 tiles
        self.tileset_width = int(self.tilemap_width / self.tile_width)
        self.tileset_height = int(self.tilemap_height / self.tile_height)

        self.tile_count = self.tileset_height * self.tileset_width

        # initialize a list of the right size of sprites
        self.sprites = [None for _ in range(self.tile_count)]

        # loop through the coordinates of the tileset, e.g. 32/4
        for x in range(self.tileset_height):
            for y in range(self.tileset_width):
                # set the sprite at a given position to the corresponding
                # position this is like reshaping a matrix into a 1D vector
                # of "pixels" where the "pixels" are instead our tiles

                # Later, we can define where the wall or item tiles are and
                # fetch them using this system,
                print("Adding a new sprite!")
                self.sprites[y * self.tileset_width + x] = self.imageHandler((x * self.tile_width,
                                                                             y * self.tile_height), 32)
        print("finished loading sprites!")

    def imageHandler(self, position, sprite_size):
        # returns a pygame surface containing the
        # tile at the given x,y position in terms
        # of sprite size

        # new surface sized to the tile size
        image = pygame.Surface((self.tile_width, self.tile_height))
        # combine new surface to the tilemap, selecting only the right position
        # in terms of the tile-oriented coordinate system
        image.blit(self.tilemap, (0, 0), (position[0],
                                          position[1],
                                          self.tile_width,
                                          self.tile_height))
        # ignore the pink color, treat as transparent
        image.set_colorkey((255, 0, 255))
        return pygame.transform.scale(image, (32, 32))

    def get_sprite(self, pos):
        """We reshaped the tileset into a list, but we
        can still fetch data at an x,y position because
        we know how we encoded the data"""
        return self.sprites[pos[1] * self.tileset_width + pos[0]]


class FloorSprite(pygame.sprite.Sprite):
    """Class Representing a floor tile,
    inherits pygame's sprite, extending it
    with method for loading from the sprite file"""

    def __init__(self, layer, sprite_sheet, position):
        # based on the pygame docs,
        # we have to also initialize
        # the parent class
        self.group = layer["TILE_FLOOR"]
        pygame.sprite.Sprite.__init__(self, self.group)

        # load the images from the tileset
        # uses list comprehension to grab
        # locations from my const and fetches
        # images for those locations
        self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in FLOOR_TILE]
        self.tile = self.tiles[0]

        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 32
        print("made a new floor tile")


class WallSprite(pygame.sprite.Sprite):
    """Class Representing a wall tile,
    inherits pygame's sprite, extending it
    with method for loading from the sprite file"""

    def __init__(self, layer, sprite_sheet, position):
        # based on the pygame docs,
        # we have to also initialize
        # the parent class
        self.group = layer["TILE_WALL"]
        pygame.sprite.Sprite.__init__(self, self.group)

        # load the images from the tileset
        # uses list comprehension to grab
        # locations from my const and fetches
        # images for those locations
        self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in WALL_TILE]
        self.tile = self.tiles[0]

        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 32
        print("made a new wall tile")


class HeroSprite:
    """Class Representing the player,
    inherits pygame's sprite, extending it
    with the method for loading fromt e sprite file
    """
    def __init__(self, layer, sprite_sheet, position):
        self.group = layer["TILE_HERO"]
        pygame.sprite.Sprite.__init__(self,self.group)
        self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in PLAYER_TILE]
        self.tile = self.tiles[0]
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 32

        print("added a new hero tile")
#    def update(self): #handles pixels

#    def move(self): #handles tiles

class Character:
    def __init__(self, health, vel, pos):
        self.health = health
        self.vel = vel
        self.pos = pos


    def is_collision(self, char1, char2):
        pass

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

<<<<<<< HEAD
=======
    WallSprite(tile_layers, sprite_handler, (4,4))
    HeroSprite(tile_layers, sprite_handler, (5,5))
>>>>>>> hero_logic
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
