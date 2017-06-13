from scripts import constants

def checkWall(y, x, room):
    return room.map[int(y // constants.tileHeight)][int(x // constants.tileWidth)] == 1

def checkMove(y,x,height,width, room):
    return checkWall(y, x, room) or checkWall(y + height, x, room) or checkWall(y, x + width, room) or checkWall(y + height, x + width, room)
