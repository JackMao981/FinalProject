"""
Rogue-like
@author: Jack Mao, Lee Smith, and Melissa Anthony
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
import time

# Game Class, for handling game loop eventually
class RogueLike():
    def __init__(self):
        """Initialize the roguelike game instance. Handles
        utility functions necessary for pygame and the
        main game loop"""

        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((2048, 1224))
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


    def sprite_render(self):
        """Reblit all sprites onto the main screen"""

        # fill the screen with bg color
        self.screen.fill(pygame.Color(0, 0, 0))

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
        ratio = curr_health / max_health
        height = 150
        total_bar = pygame.Rect(x_location, y_location, height, height)
        pygame.draw.rect(self.screen,(255, 255, 255), total_bar)
        curr_bar = pygame.Rect(x_location + 5, y_location + 5 + (1-ratio) * (height - 10),
                            height-10, ratio * (height - 10))
        pygame.draw.rect(self.screen, (255, 0, 0), curr_bar)
        """
        if curr_health<50:
            panic_sound.play(-1)
        else:
            panic_sound.stop()
            """


    def generate_level(self):
        """Delete all tiles in desired layer"""

        # fade in
        display_surface = pygame.display.set_mode((0, 0))
        fade = pygame.image.load("./sprites/sprite_png/fade.png")
        display_surface.blit(fade, (0, 0))
        fade.set_alpha(0)  # make it completely transparent

        for i in range(255):
            fade.set_alpha(i)
            pygame.display.flip()

        for layer in self.tile_layers:
            for tile in self.tile_layers[layer]:
                tile.kill()

        # characteristics = Characteristics(616,616,350,66,0,36,1.6, [])
        # self.hero = HeroSprite(self.tile_layers, self.sprite_handler, (10,10), characteristics)
        self.hero.posReset((10, 10))
        self.map = Map()


        for i in range(255):
            fade.set_alpha(255 - i)
            pygame.display.flip()

        # place sprites/tiles
        self.map.generate(self)
        self.display_health()


    def gameloop(self):
        """Run the main game loop"""

        # place map related tiles
        self.map.generate(self)

        # create the hero!
        characteristics = Characteristics(616,616,350, 350, 66,0,36,1.6, [])
        self.hero = HeroSprite(self.tile_layers, self.sprite_handler, (10, 10), characteristics)
        deadmau = pygame.image.load('./sprites/sprite_png/deadmau.png')
        # starts the game
        start = True
        while start:
            startscreen = pygame.image.load('./sprites/sprite_png/startscreen.png')
            display_surface = pygame.display.set_mode((0, 0))
            display_surface.blit(startscreen, (0, 0))
            pygame.display.update()
            time.sleep(1)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    start = False
                    revive = False
                    intro = True
        # introduction screen
        current_image = 0
        introwords1 = pygame.image.load("./sprites/sprite_png/storywords1.png")
        introwords2 = pygame.image.load("./sprites/sprite_png/storywords2.png")
        introwords3 = pygame.image.load("./sprites/sprite_png/storywords3.png")
        introwords4 = pygame.image.load("./sprites/sprite_png/storywords4.png")
        intropic1 = pygame.image.load("./sprites/sprite_png/intro1.png")
        intropic2 = pygame.image.load("./sprites/sprite_png/intro2.png")
        intropic3 = pygame.image.load("./sprites/sprite_png/intro3.png")
        intropic4 = pygame.image.load("./sprites/sprite_png/intro4.png")
        instructions = pygame.image.load("./sprites/sprite_png/instructions.png")
        itemguide = pygame.image.load("./sprites/sprite_png/itemguide.png")
        introorder = [introwords1, intropic1, introwords2, intropic2, introwords3, intropic3, introwords4, intropic4
                , instructions, itemguide]
        while intro:
            display_surface = pygame.display.set_mode((0, 0))
            events = pygame.event.get()
            for event in events:
                time.sleep(.1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_image += 1
            display_surface.blit(introorder[current_image], (0, 0))
            pygame.display.update()
            if current_image >= 9:
                time.sleep(2)
                intro = False
                run = True
        # run the game loop until program is quit
        dead = False
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
                    #move_sound.play()
                    if event.key == pygame.K_LEFT:
                        delta = (-1, 0)
                    if event.key == pygame.K_RIGHT:
                        delta = (1, 0)
                    if event.key == pygame.K_UP:
                        delta = (0, -1)
                    if event.key == pygame.K_DOWN:
                        delta = (0, 1)
                    self.hero.collisionHandler(self, delta)
                    # quit the game when the hero's health is 0
                    dead = self.hero.characteristics.curr_health <= 0
                    if dead:
                        run = False
            self.sprite_render()
        deadmau = pygame.image.load('./sprites/sprite_png/deadmau.png')
        display_surface = pygame.display.set_mode((0, 0))
        display_surface.blit(deadmau, (0, 0))
        pygame.display.update()

        while dead:
            print("dead")
            events = pygame.event.get()
            for event in events:
                print(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("quit")
                        pygame.quit()
                        return
                    if event.key == pygame.K_SPACE:
                        revive = True
                        print("revive")
                        dead = False
                        run = False

        if revive:
            pygame.quit()
            print("revived")
            RogueLike().gameloop()

if __name__ == "__main__":
    # create the main object and run the loop function
    rogue = RogueLike()
    rogue.gameloop()
