from gamemap import *
roommap =[
        [1,1,1,1,1,1],
        [1,0,0,0,0,1],
        [1,0,0,0,0,1],
        [1,0,0,0,0,1],
        [1,0,0,1,0,1],
        [1,0,0,0,0,1],
        [1,1,1,1,1,1]
]
WIDTH = 800
HEIGHT = 600
topleftx = 100
toplefty = 150
OBJECT_LIST = [images.floor,images.pillar]
roomheight = 0
roomwidth = 0
def draw():
    roomheight = len(roommap)
    roomwidth = len(roommap[0])

    for y in range(roomheight):
        for x in range(roomwidth):
            item = roommap[y][x]
            drawimage = OBJECT_LIST[item]
            screen.blit(drawimage,(topleftx+ x*30,toplefty + y*30-drawimage.get_height()))

def autogenroom(roomnum):
    temproommap = []
    temprow = []
    width = GAME_MAP[roomnum][2]
    height = GAME_MAP[roomnum][1]
    exittop = GAME_MAP[roomnum][3]
    exitright = GAME_MAP[roomnum][4]
    #top row
    if exittop:
        temprow = [1] * int(width / 2)
        temprow = temprow + [0]
        temprow = temprow + [1] * (width - len(temprow))
        temproommap.append(temprow)
    else:
        temprow = [1] * width
        temproommap.append(temprow)
    for i in range(height -2):
        temprow = [1]
        temprow = temprow + [0] * (width - 2)
        temprow = temprow + [1]
        temproommap.append(temprow)
    temprow = [1] * width
    temproommap.append(temprow)
    roommap = temproommap
autogenroom(40)
draw()

#print(GAME_MAP[40][2])