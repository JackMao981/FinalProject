import pygame
import random

# Define where objects are in our sprite file.
# Each sprite is 16x16 pixels in size, and the
# image is 256x256 pixels in size, to allow for
# future expansion in our tileset.
# transparent content in the sprite sheet is
# the traditional pink. this decision was made
# because I looked at lots of spritesheets and
# they all used pink pretty much
WALL_TILE = [(0, 0)]
FLOOR_TILE = [(1, 0)]
PLAYER_TILE = [(2, 0)]
DOOR_TILE = [(3, 0)]
ITEM_POTION_TILE = [(4,0)]
ITEM_HEART_TILE = [(5,0)]
ITEM_SHEILD_TILE = [(0,2)]
ENEMY_TILE = [(0,1)]
SPRITE_PATH = "sprites/mousesheet.bmp"


class SpriteHandler:
    """Sprite class to handle common sprite operations"""
    def __init__(self):
        # load the texture file into a surface
        # the beginner guide on pygame told me
        # that .convert increases render speed
        self.tilemap = pygame.image.load(SPRITE_PATH).convert()
        self.tilemap_width, self.tilemap_height = self.tilemap.get_size() # 1024 x 1024

        # set per-tile size
        self.tile_width = 16
        self.tile_height = 16

        # make a coordinate system in terms of tile size
        # e.g. 256x256 divided into 16x16 tiles
        self.tileset_width = int(self.tilemap_width / self.tile_width)
        self.tileset_height = int(self.tilemap_height / self.tile_height)

        self.tile_count = self.tileset_height * self.tileset_width

        # initialize a list of the right size of sprites
        self.sprites = [None for _ in range(self.tile_count)]

        # loop through the coordinates of the tileset, e.g. 256/16
        for x in range(self.tileset_height):
            for y in range(self.tileset_width):
                # set the sprite at a given position to the corresponding
                # position this is like reshaping a matrix into a 1D vector
                # of "pixels" where the "pixels" are instead our tiles

                # Later, we can define where the wall or item tiles are and
                # fetch them using this system,
                self.sprites[y * self.tileset_width + x] = self.imageHandler((x * self.tile_width,
                                                                             y * self.tile_height), 256)

    def imageHandler(self, position, sprite_size):
        """returns a pygame surface containing the
        tile at the given x,y position in terms
        of sprite size
        position: tuple with the position coordinates, order is x,y
        sprite_size: size of sprite sheet in pixels"""

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
        return pygame.transform.scale(image, (256, 256))

    def get_sprite(self, pos):
        """We reshaped the tileset into a list, but we
        can still fetch data at an x,y position because
        we know how we encoded the data
        pos: position tuple ordered x, y"""
        return self.sprites[pos[1] * self.tileset_width + pos[0]]


class FloorSprite(pygame.sprite.Sprite):
    """Class Representing a floor tile,
    inherits pygame's sprite, extending it
    with method for loading from the sprite file"""

    def __init__(self, layer, sprite_sheet, position):
        """Create new floor sprite instance
        layer: the layer dictionary
        sprite_sheet: the sprite handler
        position: the desired position of the sprite"""
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
        self.rect.topleft = self.pos * 256


class WallSprite(pygame.sprite.Sprite):
    """Class Representing a wall tile,
    inherits pygame's sprite, extending it
    with method for loading from the sprite file"""

    def __init__(self, layer, sprite_sheet, position):
        """Create new wall sprite instance
        layer: the layer dictionary
        sprite_sheet: the sprite handler
        position: the desired position of the sprite"""
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
        self.rect.topleft = self.pos * 256


class DoorSprite(pygame.sprite.Sprite):
    """Class Representing a wall tile,
    inherits pygame's sprite, extending it
    with method for loading from the sprite file"""

    def __init__(self, layer, sprite_sheet, position):
        """Create new door sprite instance
        layer: the layer dictionary
        sprite_sheet: the sprite handler
        position: the desired position of the sprite"""

        # based on the pygame docs,
        # we have to also initialize
        # the parent class
        self.group = layer["TILE_DOOR"]
        pygame.sprite.Sprite.__init__(self, self.group)

        # load the images from the tileset
        # uses list comprehension to grab
        # locations from my const and fetches
        # images for those locations
        self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in DOOR_TILE]
        self.tile = self.tiles[0]

        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 256


class HeroSprite(pygame.sprite.Sprite):
    """Class Representing the player,
    inherits pygame's sprite, extending it
    with the method for loading fromt e sprite file
    """

    def __init__(self, layer, sprite_sheet, position, characteristics):
        """Create new hero sprite instance
        layer: the layer dictionary
        sprite_sheet: the sprite handler
        position: the desired position of the sprite
        characteristics: characteristics instance"""
        self.group = layer["TILE_HERO"]
        pygame.sprite.Sprite.__init__(self, self.group)
        self.characteristics = characteristics
        self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in PLAYER_TILE]
        self.tile = self.tiles[0]
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 256

    def update(self):
       """handles sprite rect location in terms of pixels"""
       self.rect.x = self.pos.x * 256
       self.rect.y = self.pos.y * 256

    def posReset(self, position):
        """reset the position of the player on level change
        position: a tuple with x and y values respectively"""

        pygame.sprite.Sprite.__init__(self, self.group)
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 256

    def move(self, delta):
       """handles tiles
       delta: tuple with dx and dy, respectively"""
       self.pos.x += delta[0]
       self.pos.y += delta[1]


    def collide(self, layer, delta):
        """check if character will collide with the given layer:
        layer: group of sprites
        delta: tuple with dx and dy, respectively"""
        for tile in layer:
            if (tile.pos.x == self.pos.x + delta[0] and tile.pos.y == self.pos.y + delta[1]):
                print("wall or enemy collision")
                return tile
        return False

    def doorCollide(self, layer, delta):
        """check if character will collide with the given layer:
        layer: group of sprites
        delta: tuple with dx and dy, respectively"""
        for tile in layer:
            if (tile.pos.x == self.pos.x + delta[0] and tile.pos.y == self.pos.y + delta[1]):
                print("You're done!")
                return True
        return False

    def collisionHandler(self, rogue, delta):
        """Handles movement events for the player
        rogue: main roguelike game instance
        delta: tuple with dx and dy, respectively"""
        if self.doorCollide(rogue.tile_layers["TILE_DOOR"], delta):
            print("level done!")
            rogue.generate_level()
        if self.collide(rogue.tile_layers["TILE_ENEMY"], delta):
            # handle damage chance / attach interaction
            self.attack(self.collide(rogue.tile_layers["TILE_ENEMY"], delta))
            print("Health: ", self.characteristics.curr_health, "/", self.characteristics.max_health)
        if self.collide(rogue.tile_layers["TILE_ITEM"], delta):
            # handle damage chance / attach interaction
            print("item get", self.collide(rogue.tile_layers["TILE_ITEM"], delta).item.name)
            self.characteristics.add_item(self.collide(rogue.tile_layers["TILE_ITEM"], delta).item)
            self.collide(rogue.tile_layers["TILE_ITEM"], delta).kill()
        if not self.collide(rogue.tile_layers["TILE_WALL"], delta) and not self.collide(rogue.tile_layers["TILE_ENEMY"], delta) :
            self.move(delta)

    def attack(self, enemy):
        """
        Handles the subtraction of hero's and enemy's current hp
        enemy: a tile instance of the enemy
        """
        hero_damage_taken = self.characteristics.damage_taken(enemy.characteristics.damage_output())
        enemy_damage_taken = self.characteristics.damage_taken(self.characteristics.damage_output())
        self.characteristics.curr_health -= hero_damage_taken
        enemy.characteristics.curr_health -= enemy_damage_taken
        if (enemy.characteristics.curr_health <= 0):
            enemy.kill()
        print("I'm attacking")

class EnemySprite(pygame.sprite.Sprite):
    """Class Representing the player,
    inherits pygame's sprite, extending it
    with the method for loading from the sprite file
    """

    def __init__(self, layer, sprite_sheet, position, characteristics):
        """Create new enemy sprite instance
        layer: the layer dictionary
        sprite_sheet: the sprite handler
        position: the desired position of the sprite
        characteristics: characteristics instance"""

        self.group = layer["TILE_ENEMY"]
        pygame.sprite.Sprite.__init__(self, self.group)
        self.characteristics = characteristics
        self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in ENEMY_TILE]
        self.tile = self.tiles[0]
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 256

    def update(self):
       """handles sprite rect location in terms of pixels"""
       self.rect.x = self.pos.x * 256
       self.rect.y = self.pos.y * 256

    def posReset(self, position):
        """reset the position of the player on level change
        position: a tuple with x and y values respectively"""

        pygame.sprite.Sprite.__init__(self, self.group)
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 256

    def move(self, delta):
       """handles tiles
       delta: tuple with dx and dy, respectively"""
       self.pos.x += delta[0]
       self.pos.y += delta[1]

#    def collide(self, layer, delta):
#        """check if character will collide with the given layer:
#        layer: group of sprites
#        delta: tuple with dx and dy, respectively"""
#        for tile in layer:
#            if (tile.pos.x == self.pos.x + delta[0] and tile.pos.y == self.pos.y + delta[1]):
#                print("wall collision")
#                return tile
#        return False

class ItemSprite(pygame.sprite.Sprite):
    """Class Representing a floor tile,
    inherits pygame's sprite, extending it
    with method for loading from the sprite file"""

    def __init__(self, layer, sprite_sheet, position):
        # based on the pygame docs,
        # we have to also initialize
        # the parent class
        self.group = layer["TILE_ITEM"]
        pygame.sprite.Sprite.__init__(self, self.group)

        # load the images from the tileset
        # uses list comprehension to grab
        # locations from my const and fetches
        # images for those locations
        list_of_items = [Potion(), Sheild(), Heart()]
        rand = random.randint(0,2)
        if(rand == 0):
            self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in ITEM_POTION_TILE]
        elif(rand == 1):
            self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in ITEM_SHEILD_TILE]
        elif(rand == 2):
            self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in ITEM_HEART_TILE]
        self.tile = self.tiles[0]
        self.item = list_of_items[rand]
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 256
        print("made a new item tile")

# Defining the stats of the hero and enemy
class Characteristics:

    def __init__(self, curr_health, max_health, mana, max_mana, atk, true_damage, armor, spd, items):
        """creates a Characteristics object
        curr_health: number, stores current health
        max_health: number, stores the maximum health
        mana: number, stores the current mana
        max_mana: number, stores the maximum mana
        atk: number, stores the attack stat
        true_damage: number, stores the true damage stat
        armor: number, stores the true damage stats
        spd: number, stores the number of attacks per move stat
        items: list of strings, stores the string of the item inside a list"""
        self.curr_health = curr_health
        self.max_health = max_health
        self.mana = mana
        self.atk = atk
        self.armor = armor
        self.spd = spd
        self.true_damage = true_damage
        self.items = items


    # a function used to check your current health
    def print_health(self):
        """prints health on the terminal"""
        print("health: " + str(self.curr_health) + "/" + str(self.max_health))
    # checks if you are dead
    def is_dead(self):
        """returns if the character is dead"""
        if(self.curr_health <= 0):
            return True
        return False

    # checks if you have enough mana to cast a spell
    def has_enough_mana(self, mana_cost):
        """
        checks if the character has enough mana left
        mana_cost: number, the amount of mana required to do something
        """
        if(self.mana > mana_cost):
            self.mana -= mana_cost
            return True
        return False

    def damage_output(self):
        """
        returns the amount of damage dealt to the enemy before armor reduction
        """
        return self.spd * self.atk, self.true_damage

    def damage_taken(self, input_damage):
        """
        returns the damage that the character takes
        input_damage: tuple with damage and true damage, respectively
        """
        damage = input_damage[0]
        true_damage = input_damage[1]
        if (self.armor <= 0):
            return (2 - (100/(100-self.armor))) * damage + true_damage
        else:
            return (100/(100+self.armor)) * damage + true_damage

    def add_item(self, item):
        """
        adds the string of the item to the items list
        item: Item, the object that modifies your stats
        """
        for key in item.modifiers:
            if (key == "atk"):
                self.atk += item.modifiers[key]
            if (key == "health"):
                self.curr_health += item.modifiers[key]
                if(self.curr_health > self.max_health):
                    self.curr_health = self.max_health
            if (key == "max_health"):
                self.max_health += item.modifiers[key]
                self.curr_health += item.modifiers[key]
            if (key == "armor"):
                self.armor += item.modifiers[key]
            if (key == "mana"):
                self.mana += item.modifiers[key]
        self.items.append(item.name)

class Item:
    def __init__(self, modifiers, name):
        """
        creates an Item object
        modifiers: dictionary, stores the attributes of the item
        name: string, stores the name of the item
        """
        self.modifiers = modifiers
        self.name = name
class Potion(Item):
    def __init__(self, modifiers = {"health":80}, name = "Doran's Shield"):
        """
        creates Doran_sheild, an item that modifies max_health and armor
        Doran sheild be initialized by its default values only
        modifiers: dictionary, stores the attributes of the item
        name: string, stores the name of the item
        """
        Item.__init__(self, modifiers, name)
        self.modifiers = modifiers
        self.name = name

class Sheild(Item):
    def __init__(self, modifiers = {"armor": 10}, name = "Doran's Shield"):
        """
        creates Doran_sheild, an item that modifies max_health and armor
        Doran sheild be initialized by its default values only
        modifiers: dictionary, stores the attributes of the item
        name: string, stores the name of the item
        """
        Item.__init__(self, modifiers, name)
        self.modifiers = modifiers
        self.name = name

class Heart(Item):
    def __init__(self, modifiers = {"max_health": 10}, name = "Doran's Shield"):
        """
        creates Doran_sheild, an item that modifies max_health and armor
        Doran sheild be initialized by its default values only
        modifiers: dictionary, stores the attributes of the item
        name: string, stores the name of the item
        """
        Item.__init__(self, modifiers, name)
        self.modifiers = modifiers
        self.name = name
