from gamemap import *
from objects import *
from scenery import *
from player import *
import time
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
#OBJECT_LIST = [images.floor,images.pillar,images.soil]
roomheight = 0
roomwidth = 0
currentroom = 32
#########################
#### Player Variables ###
#########################
playerx = 5
playery = 2
playerframe = 0
fromplayerx = 5
fromplayery = 2
playerimage = ""
playerdirection = "down"
playeroffsetx = 0
playeroffsety = 0

def draw():
    global roomheight
    global roomwidth
    roomheight = len(roommap)
    roomwidth = len(roommap[0])

    screen.clear()
    for y in range(roomheight):
        for x in range(roomwidth):
            item = roommap[y][x]
            drawimage = OBJECT_LIST[item][0]
            screen.blit(drawimage,(topleftx+ x*30,toplefty + y*30-drawimage.get_height()))
    drawplayer()

def drawplayer():
    #print (playerframe)
    playerimage = PLAYER[playerdirection][playerframe]
    screen.blit(playerimage,(topleftx+ playerx*30,toplefty + playery*30-playerimage.get_height()))
def autogenroom(roomnum):
    global roommap
    temproommap = []
    temprow = []
    width = GAME_MAP[roomnum][2]
    height = GAME_MAP[roomnum][1]
    exittop = GAME_MAP[roomnum][3]
    exitright = GAME_MAP[roomnum][4]
    exitbottom = False
    exitleft = False
    #bottom exit
    if roomnum < 46:
        if GAME_MAP[roomnum+5][3]:
            exitbottom = True

    #left exit
    if roomnum %5 != 1:
        if GAME_MAP[roomnum-1][4]:
            exitleft = True

    #rooms 1-25
    if roomnum < 26:
        if roomnum < 6:
            #draws top fence
            temprow = [31] * width
            temproommap.append(temprow)


            for i in range(height-1):
                #draws left fence
                if roomnum %5 == 0:
                    temprow = [2] * (width-1)
                    temprow = temprow + [31]
                    temproommap.append(temprow)
                #draws right fence
                elif roomnum %5 == 1:
                    temprow = [31]
                    temprow = temprow + [2] * (width-1)
                    temproommap.append(temprow)
                #draws soil
                else:
                    temprow = [2] * (width)
                    temproommap.append(temprow)

        else:

            for i in range(height):
                if roomnum %5 == 0:
                    temprow = [2] * (width-1)
                    temprow = temprow + [31]
                    temproommap.append(temprow)
                elif roomnum %5 == 1:
                    temprow = temprow + [31]
                    temprow = temprow + [2] * (width-1)
                    temproommap.append(temprow)
                else:
                    temprow = temprow + [2] * (width)
                    temproommap.append(temprow)
            if roomnum > 20:
                #makes row next to building
                for m in range(width):
                    temproommap[height-1][m] = 1

    else:
        #top row
        if exittop:
            temprow = [1] * int(width / 2-1)
            temprow = temprow + [0]*2
            temprow = temprow + [1] * (width - len(temprow))
            temproommap.append(temprow)
        else:
            temprow = [1] * width
            temproommap.append(temprow)
        if exitright:
            rightexit = int(height/2)
        else:
            rightexit = -99
        if exitleft:
            leftexit = int(height/2)
        else:
            leftexit = -99
        for i in range(height -2):
            if i == leftexit or i == leftexit - 1 or i == leftexit + 1:
                temprow = [0]
            else:
                temprow = [1]
            temprow = temprow + [0] * (width - 2)
            if i == rightexit or i == rightexit - 1 or i == rightexit + 1:
                temprow = temprow + [0]
            else:
                temprow = temprow + [1]
            temproommap.append(temprow)
        #bottom row
        if exitbottom:
            temprow = [1] * int(width / 2-1)
            temprow = temprow + [0]*2
            temprow = temprow + [1] * (width - len(temprow))
            temproommap.append(temprow)
        else:
            temprow = [1] * width
            temproommap.append(temprow)
    #########################
    ##     Add Scenery     ##
    #########################
    if roomnum in scenery:
        roomscenery =  scenery[roomnum]
        for b in roomscenery:
            temproommap[b[1]][b[2]] = b[0]


    roommap = temproommap
    global roomheight
    global roomwidth
    roomheight = len(roommap)
    roomwidth = len(roommap[0])
def gameLoop():
    global currentroom
    global playerx, playery, playerdirection, playerframe, playerimage, playeroffsetx, playeroffsety, fromplayerx
    global fromplayery
    global roomwidth
    if playerframe > 0:
        playerframe += 1
        if playerframe == 5:
            playerframe = 0
            time.sleep(0.05)
            playeroffsetx = 0
            playeroffsety = 0
    #store original x and y
    fromplayerx = playerx
    fromplayery = playery

    if playerframe == 0:

        if keyboard.right:
            playerx += 1
            playerdirection = "right"
            playerframe = 1
        elif keyboard.left:
            playerx -= 1
            playerdirection = "left"
            playerframe = 1
        elif keyboard.up:
            playery -= 1
            playerdirection = "up"
            playerframe = 1
        elif keyboard.down:
            playery += 1
            playerdirection = "down"
            playerframe = 1
        #print(roommap)
        #print(playerx)
        #print(playery)

        #moving between rooms
        #print(playerx, playery, roomwidth, roomheight)
        if playerx == roomwidth:
            currentroom += 1
            autogenroom(currentroom)
            playerx = 0 #zero once left side doors
            playery = int(roomheight / 2)
            #print("HI")
            playerframe = 0
        if playerx == -1:
            currentroom -= 1
            autogenroom(currentroom)
            playerx = roomwidth-1
            playery = int(roomheight / 2)
            #print("HI")
            playerframe = 0
        if playery == -1:
            currentroom -= 5
            autogenroom(currentroom)
            playerx = int(roomwidth / 2)
            playery = roomheight - 1
            playerframe = 0
        if playery == roomheight:
            currentroom += 5
            autogenroom(currentroom)
            playerx = int(roomwidth / 2)
            playery = 1
            print(playery)
            playerframe = 0
        if roommap[playery][playerx] not in items_player_may_stand_on:

            playery = fromplayery
            playerx = fromplayerx
            playerframe = 0

    if playerdirection == "right":
        playeroffsetx = -1 + 0.25 * playerframe
    if playerdirection == "left":
        playeroffsetx = 1 - 0.25 * playerframe
    if playerdirection == "up":
        playeroffsety = 1 - 0.25 * playerframe
    if playerdirection == "down":
        playeroffsety = -1 + 0.25 * playerframe








autogenroom(currentroom)
clock.schedule_interval(gameLoop, 0.03)