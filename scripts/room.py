import pyglet
from resources import resource_loader
from scripts import constants

class Room(object):
    def __init__(self):
        self.background_tile = pyglet.image.load(resource_loader.files['Background.png'])
        self.wall_tile = pyglet.image.load(resource_loader.files['Wall.png'])
        self.wall_tile_right = pyglet.image.load(resource_loader.files['WallRight.png'])
        self.wall_tile_down = pyglet.image.load(resource_loader.files['WallDown.png'])
        self.wall_tile_left = pyglet.image.load(resource_loader.files['WallLeft.png'])
        self.wall_tile_block = pyglet.image.load(resource_loader.files['WallBlock.png'])
        
        self.batch = pyglet.graphics.Batch()
        self.map = []
        self.mapSprites = []
        self.saveMap()

    def checkWall(self, y, x):
        return self.map[int(y // constants.tileHeight)][int(x // constants.tileWidth)] == 1

    def checkMove(self, y, x, height, width):
        return self.checkWall(y, x) or self.checkWall(y + height, x) or self.checkWall(y, x + width) or self.checkWall(y + height, x + width)

    def saveMap(self):
        for x in range(20):
            row = []
            for y in range(20):
                if (y == 0 or y == 19):
                    row.append(1)
                elif (x == 0):
                    row.append(1)
                elif (x == 19):
                    row.append(1)
                elif (y == 10 and x == 1):
                    row.append(1)
                else:
                    row.append(0)
            self.map.append(row)

        self.addMapImages()

    def addMapImages(self):
        for x in range(20):
            for y in range(20):
                if (y == 0 or y == 19):
                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile, x=x*30, y=y*24, batch=self.batch))
                elif (x == 0):
                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_right, x=x*30, y=y*24, batch=self.batch))
                elif (x == 19):
                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_left, x=x*30, y=y*24, batch=self.batch))
                elif (x == 10 and y == 1):
                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_block, x=x*30, y=y*24, batch=self.batch))
                else:
                    self.mapSprites.append(pyglet.sprite.Sprite(self.background_tile, x=x*30, y=y*24, batch=self.batch))
