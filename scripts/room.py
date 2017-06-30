import pyglet
from resources import resource_loader
from scripts import constants
from scripts.monsters import gremlin

class Room(object):
    def __init__(self, number):
        self.background_tile = pyglet.image.load(resource_loader.files['Background.png'])
        self.wall_tile = pyglet.image.load(resource_loader.files['Wall.png'])
        self.wall_tile_right = pyglet.image.load(resource_loader.files['WallRight.png'])
        self.wall_tile_down = pyglet.image.load(resource_loader.files['WallDown.png'])
        self.wall_tile_left = pyglet.image.load(resource_loader.files['WallLeft.png'])
        self.wall_tile_block = pyglet.image.load(resource_loader.files['WallBlock.png'])
        self.wall_tile_down_left = pyglet.image.load(resource_loader.files['WallDownLeft.png'])
        self.wall_tile_down_right = pyglet.image.load(resource_loader.files['WallDownRight.png'])
        self.wall_tile_left_right = pyglet.image.load(resource_loader.files['WallLeftRight.png'])
        
        self.batch = pyglet.graphics.Batch()
        self.map = []
        self.mons = []
        self.mapSprites = []
        self.freeProjectiles = []
        self.saveMap(number)

        self.leftRoom = None
        self.rightRoom = None
        self.upRoom = None
        self.downRoom = None

    def left(self, room):
        if room.rightRoom != None or self.leftRoom != None:
            return
        self.leftRoom = room
        room.rightRoom = self

    def right(self, room):
        if room.leftRoom != None or self.rightRoom != None:
            return
        self.rightRoom = room
        room.leftRoom = self

    def up(self, room):
        if room.downRoom != None or self.upRoom != None:
            return
        self.upRoom = room
        room.downRoom = self

    def down(self, room):
        if room.upRoom != None or self.downRoom != None:
            return
        self.downRoom = room
        room.upRoom = self

    def checkWall(self, y, x):
        return self.map[int(y // constants.tileHeight)][int(x // constants.tileWidth)] == 1

    def checkMove(self, y, x, height, width):
        if x <= 2 or x+width >= constants.roomWidth - 2 or y <= 2 or y + height >= constants.roomHeight - 2:
            return True
        return self.checkWall(y, x) or self.checkWall(y + height, x) or self.checkWall(y, x + width) or self.checkWall(y + height, x + width)

    def checkPlayer(self, y, x, height, width, hero):
        check = False
        for i, j in [(x, y),(x + width, y),(x, y + height),(x + width, y + height)]:
            if (i > hero.x and j > hero.y and i < hero.x + constants.playerWidth and j < hero.y + constants.playerHeight):
                check = True
        return check

    def saveMap(self, mapa = 1):
        if mapa == 1:
            for y in range(20):
                row = []
                for x in range(20):
                    if (y == 0 or y == 19):
                        row.append(1)
                    elif (x == 0):
                        row.append(1)
                    elif (x == 19):
                        if (y == 1):
                            row.append(0)
                        else:
                            row.append(1)
                    elif (x == 10 and y == 1):
                        row.append(1)
                    else:
                        row.append(0)
                self.map.append(row)

        elif mapa == 2:
            for y in range(20):
                row = []
                for x in range(20):
                    if (y == 0 or y == 19):
                        row.append(1)
                    elif (x == 19):
                        row.append(1)
                    elif (x == 0):
                        if (y == 1):
                            row.append(0)
                        else:
                            row.append(1)
                    elif (x == 10 and y == 3) or (x == 11 and y == 3):
                        row.append(1)
                    else:
                        row.append(0)
                self.map.append(row)
        else:
            self.map = mapa
            
        
        self.addMapImages()

    def addMapImages(self):
        for x in range(20):
            for y in range(20):
                if self.map[y][x] == 0:
                    self.mapSprites.append(pyglet.sprite.Sprite(self.background_tile, x=x*30, y=y*24, batch=self.batch))
                else:
                    if x == 19:
                        xp = True
                    else:
                        xp = self.map[y][x+1] == 1
                    if x == 0:
                        xm = True
                    else:
                        xm = self.map[y][x-1] == 1
                    if y == 0:
                        ym = True
                    else:
                        ym = self.map[y-1][x] == 1
                    if xp and xm and ym:
                        self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile, x=x*30, y=y*24, batch=self.batch))
                    elif xp and xm and not ym:
                        self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_down, x=x*30, y=y*24, batch=self.batch))
                    elif xp and not xm and ym:
                        self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_left, x=x*30, y=y*24, batch=self.batch))
                    elif not xp and xm and ym:
                        self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_right, x=x*30, y=y*24, batch=self.batch))
                    elif not xp and not xm and ym:
                        self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_left_right, x=x*30, y=y*24, batch=self.batch))
                    elif not xp and xm and not ym:
                        self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_down_right, x=x*30, y=y*24, batch=self.batch))
                    elif xp and not xm and not ym:
                        self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_down_left, x=x*30, y=y*24, batch=self.batch))
                    else:
                        self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_block, x=x*30, y=y*24, batch=self.batch))
                        
##                if (y == 0 or y == 19):
##                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile, x=x*30, y=y*24, batch=self.batch))
##                elif (x == 0):
##                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_right, x=x*30, y=y*24, batch=self.batch))
##                elif (x == 19):
##                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_left, x=x*30, y=y*24, batch=self.batch))
##                elif (x == 10 and y == 1):
##                    self.mapSprites.append(pyglet.sprite.Sprite(self.wall_tile_block, x=x*30, y=y*24, batch=self.batch))
##                else:
##                    self.mapSprites.append(pyglet.sprite.Sprite(self.background_tile, x=x*30, y=y*24, batch=self.batch))
