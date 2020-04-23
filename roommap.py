from gamemap import *
from objects import *
from scenery import *
from player import *
from props import *
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
HEIGHT = 660
TILESIZE = 30
topleftx = 100
toplefty = 240
#OBJECT_LIST = [images.floor,images.pillar,images.soil]
roomheight = 0
roomwidth = 0
currentroom = 31
firstdraw = True
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
playerimageshadow = PLAYER_SHADOW[playerdirection][playerframe]

#COLORS
RED =(128,0,0)

PILLARS = [images.pillar, images.pillar_95, images.pillar_80, images.pillar_60, images.pillar_50]
wall_transparency_frame = 0

def draw():
    global roomheight, firstdraw
    global roomwidth
    global topleftx
    roomheight = GAME_MAP[currentroom][1]
    roomwidth = GAME_MAP[currentroom][2]

    topleftx = (WIDTH-roomwidth*TILESIZE)/2
    #print(roomheight)
    #print(roomwidth)
    #print(currentroom)
    #screen.clear()
    #make outer window
    box = Rect((0,150),(800,660))
    screen.draw.filled_rect(box, RED)
    box = Rect((0,0),(800,toplefty + (roomheight-1)* TILESIZE))
    screen.surface.set_clip(box)
    #stage 1 - draw the floor and items the player may stand on
    if currentroom < 26:
        floortype = 2
    else:
        floortype = 0
    for y in range(roomheight):
        for x in range(roomwidth):
            #first put tile/dirt down
            drawimage = OBJECT_LIST[floortype][0]
            screen.blit(drawimage,(topleftx+ x*TILESIZE,toplefty + y*TILESIZE-drawimage.get_height()))
            #then add items we can stand on
            if roommap[y][x] in items_player_may_stand_on:
                drawimage = OBJECT_LIST[roommap[y][x]][0]
                screen.blit(drawimage,(topleftx+ x*TILESIZE,toplefty + y*TILESIZE-drawimage.get_height()))

    #special case pressure plate in room 26
    if currentroom == 26:
        drawimage = OBJECT_LIST[39][0]
        screen.blit(drawimage,(topleftx+ 2*TILESIZE,toplefty + 8*TILESIZE-drawimage.get_height()))
        itemonpad = roommap[8][2]
        #print(roommap)
        #print(itemonpad)
        if itemonpad > 0:
            drawimage = OBJECT_LIST[itemonpad][0]
            screen.blit(drawimage,(topleftx+ 2*TILESIZE,toplefty + 8*TILESIZE-drawimage.get_height()))
    #print(roommap)
    for y in range(roomheight):
        for x in range(roomwidth):
            #not go back and add the objects on top of the floor
            #skip 255 to allow for extra wide items
            item_here = roommap[y][x]
            if item_here not in items_player_may_stand_on + [255]:
                drawimage = OBJECT_LIST[item_here][0]
                #transparent front wall
                #WORK IN PROGRESS...
                if y == playery + 1 and x != 0 and x != roomwidth-1 and roommap[y][x] == 1:
                    drawimage = PILLARS[wall_transparency_frame]

                screen.blit(drawimage,(topleftx+ x*TILESIZE,toplefty + y*TILESIZE-drawimage.get_height()))

                #add shadow if there should be one
                if OBJECT_LIST[item_here][1] is not None:
                    shadowimage = OBJECT_LIST[item_here][1]
                    if shadowimage in [images.half_shadow, images.full_shadow]:
                        shadow_width = int(drawimage.get_width()/TILESIZE)
                        #repeat the shadow
                        for i in range(shadow_width):
                            screen.blit(shadowimage,(topleftx+ (x+i)*TILESIZE,toplefty + y*TILESIZE))
                    else:
                        screen.blit(shadowimage,(topleftx+ x*TILESIZE,toplefty + y*TILESIZE))
        if playery == y:
            drawplayer()
    screen.surface.set_clip(None)
    if firstdraw:
        display_inventory()
        startroom()
        firstdraw = False

def drawobject():
    drawimage = OBJECT_LIST[item][0]
    screen.blit(drawimage,(topleftx+ x*TILESIZE,toplefty + y*TILESIZE-drawimage.get_height()))

def drawplayer():
    #print (playerframe)
    playerimage = PLAYER[playerdirection][playerframe]
    screen.blit(playerimage,(topleftx+ (playerx+playeroffsetx)*TILESIZE,toplefty + (playery+playeroffsety)*TILESIZE-playerimage.get_height()))
    playerimageshadow = PLAYER_SHADOW[playerdirection][playerframe]
    screen.blit(playerimageshadow,(topleftx+ (playerx+playeroffsetx)*TILESIZE,toplefty +(playery+playeroffsety)*TILESIZE))

def drawtext(thetext, linenum):
    text_lines = [15,50]
    box = Rect((0,text_lines[linenum]),(800,35))
    screen.draw.filled_rect(box, (0,0,0))
    screen.draw.text(thetext, (20,text_lines[linenum]), color = (255,255,255))


def adjust_wall_transparency():
    global wall_transparency_frame

    #fade wall out
    if playery == roomheight - 2 and roommap[playery + 1][playerx] == 1 and wall_transparency_frame < 4:
        wall_transparency_frame +=1

    #fade wall in
    if (playery != roomheight - 2 or roommap[playery + 1][playerx] != 1) and wall_transparency_frame > 0:
        wall_transparency_frame -= 1

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
            if roomnum > 21:
                #makes row next to building
                for m in range(width):
                    temproommap[height-1][m] = 1
            if roomnum == 21:
                #row next to building with an entrance
                for m in range(width):
                    if m == int(width / 2) or m == int(width/2) + 1:
                        temproommap[height-1][m] = 2
                    else:
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
            temp_img = OBJECT_LIST[b[0]][0]
            temp_width = temp_img.get_width()
            temp_tiles = int(temp_width/TILESIZE)
            for i in range(1, temp_tiles):
                temproommap[b[1]][b[2] + i] = 255

    #############################
    ######## Add Props  #########
    #############################
    for propnum, prop in propslist.items():
        prop_room = prop[0]
        prop_y = prop[1]
        prop_x = prop[2]
        if prop_room == currentroom and temproommap[prop_y][prop_x] in [0,2,39]:
            #does the prop belong in this room and is it going to be on a floor tile
            temproommap[prop_y][prop_x] = propnum
            prop_image = OBJECT_LIST[propnum][0]
            pimage_width = prop_image.get_width()
            pimage_tiles = int(pimage_width / TILESIZE)
            for tnum in range(1, pimage_tiles):
                temproommap[prop_y][prop_x + tnum] = 255


    roommap = temproommap
    global roomheight
    global roomwidth
    roomheight = len(roommap)
    roomwidth = len(roommap[0])
def startroom():
    drawtext("You are here: " + GAME_MAP[currentroom][0],0)
    drawtext("Testing line 2", 1)
def gameLoop():
    global currentroom
    global playerx, playery, playerdirection, playerframe, playerimage, playeroffsetx, playeroffsety, fromplayerx
    global fromplayery
    global roomwidth
    global selected_item
    global item_carrying
    if playerframe > 0:
        playerframe += 1
        time.sleep(0.05)
        if playerframe == 5:
            playerframe = 0
            playeroffsetx = 0
            playeroffsety = 0
    #store original x and y


    if playerframe == 0:
        fromplayerx = playerx
        fromplayery = playery
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

        #moving between rooms
        if playerx == roomwidth:
            #move right
            currentroom += 1
            startroom()
            autogenroom(currentroom)
            playerx = 0 #zero once left side doors
            if currentroom > 25:
                playery = int(roomheight / 2)
            playerframe = 0
        if playerx == -1:
            #room left
            currentroom -= 1
            startroom()
            autogenroom(currentroom)
            playerx = roomwidth-1
            if currentroom > 25:
                playery = int(roomheight / 2)
            #print("HI")
            playerframe = 0
        if playery == -1:
            #room up
            currentroom -= 5
            startroom()
            autogenroom(currentroom)
            if currentroom > 25 or currentroom == 21:
                playerx = int(roomwidth / 2)
            playery = roomheight - 1
            playerframe = 0
        if playery == roomheight:
            #room down
            currentroom += 5
            startroom()
            autogenroom(currentroom)
            if currentroom > 25 or currentroom == 26:
                playerx = int(roomwidth / 2)
            playery = 1
            #print(playery)
            playerframe = 0

        if keyboard.g:
            pick_up_prop()
        if keyboard.d and item_carrying:
            drop_prop(fromplayerx,fromplayery)
            #leave the item behind
        if keyboard.tab and len(in_my_pockets) > 0:
            selected_item += 1
            if selected_item >= len(in_my_pockets):
                selected_item = 0
            item_carrying = in_my_pockets[selected_item]
            display_inventory()
            time.sleep(0.2)
        if keyboard.space:
            examine_prop()


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
    if playerframe == 0:
        playeroffsetx = 0
        playeroffsety = 0

#prop functions
def find_prop_startx():
    tempx = playerx
    while roommap[playery][tempx] == 255:
        tempx -= 1
    return tempx

def get_item_under_player():
    item_x = find_prop_startx()
    itemnum = roommap[playery][item_x]
    return itemnum

def pick_up_prop():
    itemnum = get_item_under_player()
    floortype = 0
    if itemnum in items_player_may_carry:
        if currentroom < 26:
            floortype = 2
        #elif currentroom == 26 and playerx
        add_item_to_pockets(itemnum)
        roommap[playery][playerx] = floortype
        drawtext("Now carrying " + OBJECT_LIST[itemnum][3], 0)
        sounds.pickup.play()
        time.sleep(0.5)
    else:
        drawtext("You can't carry that!", 0)

def drop_prop(xpos, ypos):
    #is there another prop in the way?
    if roommap[ypos][xpos] in [0,2,39]:
        propslist[item_carrying][0] = currentroom
        propslist[item_carrying][1]= ypos
        propslist[item_carrying][2] = xpos
        roommap[ypos][xpos] = item_carrying
        drawtext("You have dropped" + OBJECT_LIST[item_carrying][3], 0)
        sounds.drop.play()
        remove_prop_from_pockets(item_carrying)
        time.sleep(0.5)
    else:
        drawtext("You can't drop that there!", 0)
        time.sleep(0.5)
def remove_prop_from_pockets(propitem):
    global selected_item, item_carrying
    #take the item out of pockets
    in_my_pockets.remove(propitem)
    selected_item -= 1
    if selected_item <0:
        selected_item = 0
    if len(in_my_pockets) == 0:
        item_carrying = False
    else:
        item_carrying = in_my_pockets[selected_item]
    display_inventory()


def add_item_to_pockets(itemnum):
    global selected_item, item_carrying
    in_my_pockets.append(itemnum)
    selected_item = len(in_my_pockets) - 1
    item_carrying = in_my_pockets[selected_item]
    display_inventory()
    print(in_my_pockets)
    propslist[itemnum][0] = 0
def examine_prop():
    itemnum = get_item_under_player()
    item_leftx = find_prop_startx()
    if itemnum in [0,2]:
        #this is just floor dont examine
        return
    examine_text = "You see: " + OBJECT_LIST[itemnum][2]

    #handle hidden items
    for propnum, details in propslist.items():
        if details[0] == currentroom:
            #prop is in the currentroom
            print(propnum, details)
            if (details[1] == playery and details[2] == item_leftx
                and roommap[details[1]][details[2]] != propnum):
                    examine_text = "You found " + OBJECT_LIST[propnum][3]
                    sounds.combine.play()
    drawtext(examine_text, 0)
    for i in range(roomheight):
        print(roommap[i])
    time.sleep(0.5)


def display_inventory():
    box =  Rect((0,45),(800, 105))
    screen.draw.filled_rect(box, (0,0,0))

    if len(in_my_pockets) == 0:
        return

    start_display = (selected_item // 16) * 16
    list_to_show = in_my_pockets[start_display: start_display + 16]
    selected_marker = selected_item % 16

    for i in range(len(list_to_show)):
        itemnum =  list_to_show[i]
        img =  OBJECT_LIST[itemnum][0]
        screen.blit(img, (25 + 46 * i, 90))

    marker_left = selected_marker * 46 - 3
    box = Rect((marker_left + 22, 85), (40,40))
    screen.draw.rect(box, (255,255,255))

    #show description
    desc =  OBJECT_LIST[item_carrying][2]
    screen.draw.text(desc, (20,130), color = "white")

#################################
############ USE OBJECTS ########
#################################

def use_prop():
    use_message = "You fiddle around with it but don't get anywhere."
    standard_responses = {
        4: "Air is running out! You can't take this lying down!",
        6: "This is no time to sit around!",
        7: "This is no time to sit around!",
        32: "It shakes and rumbles, but nothing else happens.",
        34: "Ah! That's better. Now wash your hands.",
        35: "You wash your hands and shake the water off.",
        37: "The test tubes smoke slightly as you shake them.",
        54: "You chew the gum. It's sticky like glue.",
        55: "The yoyo bounces up and down, slightly slower than on Earth",
        56: "It's a bit too fiddly. Can you thread it on something?",
        59: "You need to fix the leak before you can use the canister",
        61: "You try signalling with the mirror, but nobody can see you.",
        62: "Don't throw resources away. Things might come in handy...",
        67: "To enjoy yummy space food, just add water!",
        75: "You are at Sector: " + str(current_room) + " // X: " \
            + str(player_x) + " // Y: " + str(player_y)
        }


#print(currentroom)
autogenroom(currentroom)
clock.schedule_interval(gameLoop, 0.02)
clock.schedule_interval(adjust_wall_transparency, 0.05)