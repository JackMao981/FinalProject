"""
Rogue-like
@author: Jack Mao and Dieter Brehm
"""

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
        """Initialize the roguelike game instance. Handles
        utility functions necessary for pygame and the 
        main game loop"""
        pygame.init()
        self.screen = pygame.display.set_mode((700, 700))
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
                self.map.viewport_update(self.hero)
                self.screen.blit(tile.tile, self.map.animator(tile))

        # write changes to screen
        pygame.display.flip()

    def gameloop(self):
        """Run the main game loop"""

        # place map related tiles
        self.map.generate(self)

        # create the hero!
        self.hero = HeroSprite(self.tile_layers, self.sprite_handler, (5,5))

        # run the game loop until program is quit
        run = True
        while run:
            # fetch all events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        delta = (-1, 0)
                        if not self.hero.collide(self.tile_layers["TILE_WALL"], delta):
                            self.hero.move(delta) 
                    if event.key == pygame.K_RIGHT:
                        delta = (1, 0)
                        if not self.hero.collide(self.tile_layers["TILE_WALL"], delta):
                            self.hero.move(delta)
                    if event.key == pygame.K_UP:
                        delta = (0, -1)
                        if not self.hero.collide(self.tile_layers["TILE_WALL"], delta):
                            self.hero.move(delta)
                    if event.key == pygame.K_DOWN:
                        delta = (0, 1)
                        if not self.hero.collide(self.tile_layers["TILE_WALL"], delta):
                            self.hero.move(delta)
            self.spriteRender()
        pygame.quit()


if __name__ == "__main__":
    rogue = RogueLike()
    rogue.gameloop()
