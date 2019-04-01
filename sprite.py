import pygame

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
PLAYER_TILE = [(2, 0)]
DOOR_TILE = [(6, 0)]
ITEM_TILE = [(3,0)]
ENEMY_TILE = [(1,1)]
SPRITE_PATH = "sprites/sprites_simple.bmp"


class SpriteHandler:
    """Sprite class to handle common sprite operations"""
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
                self.sprites[y * self.tileset_width + x] = self.imageHandler((x * self.tile_width,
                                                                             y * self.tile_height), 32)

    def imageHandler(self, position, sprite_size):
        """returns a pygame surface containing the
        tile at the given x,y position in terms
        of sprite size"""

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


class DoorSprite(pygame.sprite.Sprite):
    """Class Representing a wall tile,
    inherits pygame's sprite, extending it
    with method for loading from the sprite file"""

    def __init__(self, layer, sprite_sheet, position):
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
        self.rect.topleft = self.pos * 32


class HeroSprite(pygame.sprite.Sprite):
    """Class Representing the player,
    inherits pygame's sprite, extending it
    with the method for loading fromt e sprite file
    """

    def __init__(self, layer, sprite_sheet, position, characteristics):
        """Create a new 'hero' character.
        position: a tuple with x and y values respectively"""
        self.group = layer["TILE_HERO"]
        pygame.sprite.Sprite.__init__(self, self.group)
        self.characteristics = characteristics
        self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in PLAYER_TILE]
        self.tile = self.tiles[0]
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 32

    def update(self):
       """handles sprite rect location in terms of pixels"""
       self.rect.x = self.pos.x * 32
       self.rect.y = self.pos.y * 32

    def posReset(self, position):
        """reset the position of the player on level change
        position: a tuple with x and y values respectively"""

        pygame.sprite.Sprite.__init__(self, self.group)
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 32

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
                print("wall collision")
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

    #

class EnemySprite(pygame.sprite.Sprite):
    """Class Representing the player,
    inherits pygame's sprite, extending it
    with the method for loading from the sprite file
    """

    def __init__(self, layer, sprite_sheet, position, characteristics):
        """Create a new 'hero' character.
        position: a tuple with x and y values respectively"""
        self.group = layer["TILE_ENEMY"]
        pygame.sprite.Sprite.__init__(self, self.group)
        self.characteristics = characteristics
        self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in ENEMY_TILE]
        self.tile = self.tiles[0]
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 32

    def update(self):
       """handles sprite rect location in terms of pixels"""
       self.rect.x = self.pos.x * 32
       self.rect.y = self.pos.y * 32

    def posReset(self, position):
        """reset the position of the player on level change
        position: a tuple with x and y values respectively"""

        pygame.sprite.Sprite.__init__(self, self.group)
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 32

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
                print("wall collision")
                return tile
        return False

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
        self.tiles = [sprite_sheet.get_sprite(tiles) for tiles in ITEM_TILE]
        self.tile = self.tiles[0]

        self.item = Doran_sheild()
        self.rect = self.tile.get_rect()
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.rect.topleft = self.pos * 32
        print("made a new item tile")

class Characteristics:
    def __init__(self, curr_health, max_health, mana, atk, true_damage, armor, spd, items):
        self.curr_health = curr_health
        self.max_health = max_health
        self.mana = mana
        self.atk = atk
        self.armor = armor
        self.spd = spd
        self.true_damage = true_damage
        self.items = items

    def print_health(self):
        print("health: " + str(self.curr_health) + "/" + str(self.max_health))

    def is_dead(self):
        if(self.health <= 0):
            return True
        return False

    def has_enough_mana(self, mana_cost):
        if(self.mana > mana_cost):
            self.mana -= mana_cost
            return True
        return False

    def damage_output(self):
        return (agi * atk, true_damage)

    def damage_taken(self, damage, true_damage):
        if (armor <= 0):
            (2 - (100/(100-armor))) * damage + true_damage
        else:
            (100/(100+armor)) * damage + true_damage

    def add_item(self, item):
        for key in item.modifiers:
            if (key == "atk"):
                self.atk += item.modifiers[key]
            if (key == "health"):
                self.health += item.modifiers[key]
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
        self.modifiers = modifiers

class Doran_sheild(Item):
    def __init__(self, modifiers = {"max_health":80, "armor": 10}, name = "Doran's Shield"):
        Item.__init__(self, modifiers, name)
        self.modifiers = modifiers
        self.name = name
