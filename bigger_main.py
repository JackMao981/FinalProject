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
import bigger_map as map
from bigger_map import Map
import bigger_sprite as sprite
from bigger_sprite import SpriteHandler, WallSprite, FloorSprite, HeroSprite, Characteristics

# Game Class, for handling game loop eventually
class RogueLike():
    def __init__(self):
        """Initialize the roguelike game instance. Handles
        utility functions necessary for pygame and the
        main game loop"""
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 1024))
        self.clock = pygame.time.Clock()

        # load the sprite image set
        self.sprite_handler = SpriteHandler()
        self.map = Map()

        # define layers
        self.tile_layers = {
            "TILE_WALL": pygame.sprite.Group(),
            "TILE_FLOOR": pygame.sprite.Group(),
            "TILE_HERO": pygame.sprite.Group(),
            "TILE_DOOR": pygame.sprite.Group(),
            "TILE_ITEM": pygame.sprite.Group(),
            "TILE_ENEMY": pygame.sprite.Group()}

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
                self.tile_layers["TILE_DOOR"].update()
                self.tile_layers["TILE_ITEM"].update()
                self.tile_layers["TILE_ENEMY"].update()
                self.map.viewport_update(self.hero)
                self.screen.blit(tile.tile, self.map.animator(tile))
                self.display_health()

        # write changes to screen
        pygame.display.flip()


    def display_health(self):
        curr_health = self.hero.characteristics.curr_health
        max_health = self.hero.characteristics.max_health
        x_location = 10
        y_location = 10
        height = 50
        total_bar = pygame.Rect(x_location, y_location,height, max_health+10)
        pygame.draw.rect(self.screen,(255,255,255),total_bar)
        curr_bar = pygame.Rect(x_location+5,y_location+5, height-10, curr_health)
        pygame.draw.rect(self.screen,(255,0,0),total_bar)


    def generate_level(self):
        """Delete all tiles in desired layer"""
        for layer in self.tile_layers:
            for tile in self.tile_layers[layer]:
                tile.kill()

        #characteristics = Characteristics(616,616,350,66,0,36,1.6, [])
        #self.hero = HeroSprite(self.tile_layers, self.sprite_handler, (10,10), characteristics)
        self.hero.posReset((10,10))
        self.map = Map()

        # place sprites/tiles
        self.map.generate(self)
        self.display_health()

    def start_screen(self):
        pass

    def end_screen(self):
        pass

    def gameloop(self):
        """Run the main game loop"""

        # place map related tiles
        self.map.generate(self)

        # create the hero!
        characteristics = Characteristics(616,616,350, 350, 66,0,36,1.6, [])
        self.hero = HeroSprite(self.tile_layers, self.sprite_handler, (10,10), characteristics)

        # run the game loop until program is quit
        run = True
        while run:
            # fetch all events such as keypressed
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    # print the health on every turn
                    #self.hero.characteristics.print_health()

                    # collision handler changes reaction based on
                    # touched tile. Delta change according to
                    # the direction pressed and is the desired
                    # movement in units of tiles
                    if event.key == pygame.K_LEFT:
                        delta = (-1, 0)
                        self.hero.collisionHandler(self, delta)
                    if event.key == pygame.K_RIGHT:
                        delta = (1, 0)
                        self.hero.collisionHandler(self, delta)
                    if event.key == pygame.K_UP:
                        delta = (0, -1)
                        self.hero.collisionHandler(self, delta)
                    if event.key == pygame.K_DOWN:
                        delta = (0, 1)
                        self.hero.collisionHandler(self, delta)
            self.spriteRender()

            # quit the game when the hero's health is 0
            if(self.hero.characteristics.curr_health <= 0):
                print("You died.")
                pygame.quit()
                run = False
        pygame.quit()


if __name__ == "__main__":
    # create the main object and run the loop function
    rogue = RogueLike()
    rogue.gameloop()
