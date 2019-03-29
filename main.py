# grab the pygame library
import pygame

# grab some system libraries for dealing with sprite files
import sys
import os
import math
import random

from map import Map
from sprite import SpriteHandler, WallSprite, FloorSprite, HeroSprite

# Game Class, for handling game loop eventually
class RogueLike():
    def __init__(self):
        """Initialize the roguelike game"""
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        self.clock = pygame.time.Clock()
        
        # load the sprite image set
        self.sprite_handler = SpriteHandler()
        self.map = Map()

        # define layers
        self.tile_layers = {
            "TILE_WALL": pygame.sprite.Group(),
            "TILE_FLOOR": pygame.sprite.Group(),
            "TILE_HERO": pygame.sprite.Group()}

    def spriteRender(self):
        """Reblit all sprites onto the main screen"""
        # fill the screen with bg color
        self.screen.fill(pygame.Color(0,0,0))

        # iterate through all tile layers,
        # drawing the tile specified in sprite
        # object locations
        for layer in self.tile_layers:
            for tile in self.tile_layers[layer]:
                self.tile_layers["TILE_WALL"].update()
                self.tile_layers["TILE_FLOOR"].update()
                self.tile_layers["TILE_HERO"].update()
                self.screen.blit(tile.tile, tile.rect.move(0, 0))

        # write changes to screen
        pygame.display.flip()

    def gameloop(self):
        """Run the main game loop"""
        # place some floor!

        # call map.generate() here
        FloorSprite(self.tile_layers, self.sprite_handler, (1, 1))
        FloorSprite(self.tile_layers, self.sprite_handler, (1, 2))
        FloorSprite(self.tile_layers, self.sprite_handler, (1, 3))

        FloorSprite(self.tile_layers, self.sprite_handler, (4, 1))
        FloorSprite(self.tile_layers, self.sprite_handler, (4, 2))
        FloorSprite(self.tile_layers, self.sprite_handler, (4, 3))

        FloorSprite(self.tile_layers, self.sprite_handler, (3, 1))
        FloorSprite(self.tile_layers, self.sprite_handler, (3, 3))
        FloorSprite(self.tile_layers, self.sprite_handler, (2, 3))

        WallSprite(self.tile_layers, self.sprite_handler, (4,4))

        self.hero = HeroSprite(self.tile_layers, self.sprite_handler, (5,5))

        # run the game loop forever (for now just force quit)
        run = True
        while run:
            # need to get this to stop program
            # from freezing
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.hero.move((-1,0))
                    if event.key == pygame.K_RIGHT:
                        self.hero.move((1,0))
                    if event.key == pygame.K_UP:
                        self.hero.move((0,-1))
                    if event.key == pygame.K_DOWN:
                        self.hero.move((0,1))
            self.spriteRender()
        pygame.quit()



if __name__ == "__main__":
    rogue = RogueLike()
    rogue.gameloop()
