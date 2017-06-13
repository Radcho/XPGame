import pyglet
from resources import resource_loader

class Room:
    def __init__(self):
        self.background_tile = pyglet.image.load(resource_loader.files['Background.png'])
        self.wall_tile = pyglet.image.load(resource_loader.files['Wall.png'])
        self.wall_tile_right = pyglet.image.load(resource_loader.files['WallRight.png'])
        #self.wall_tile_down = pyglet.image.load(resource_loader.files['WallDown.png'])
        self.wall_tile_left = pyglet.image.load(resource_loader.files['WallLeft.png'])
        #self.wall_tile_block = pyglet.image.load(resource_loader.files['WallBlock.png'])
        
        self.batch = pyglet.graphics.Batch()
        self.map = []
        self.mapSprites = []
        self.saveMap()

    def saveMap(self):
        for x in range(20):
            row = []
            for y in range(29):
                if (y == 0 or y == 19):
                    row.append(1)
                elif (x == 0):
                    row.append(1)
                elif (x == 19):
                    row.append(1)
                else:
                    row.append(0)
            self.map.append(row)

        self.addMapImages()

    def addMapImages(self):
        for x in range(20):
            for y in range(29):
                if (y == 0 or y == 19):
                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile, x=x*30, y=y*24, batch=self.batch))
                elif (x == 0):
                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_right, x=x*30, y=y*24, batch=self.batch))
                elif (x == 19):
                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_left, x=x*30, y=y*24, batch=self.batch))
                else:
                    self.mapSprites.append(pyglet.sprite.Sprite(self.background_tile, x=x*30, y=y*24, batch=self.batch))