WIDTH = 800
HEIGHT = 600

player_x = 100
player_y = 100

def draw():
    global player_x, player_y
    screen.blit(images.backdrop, (0,0))
    screen.blit(images.astronaut, (player_x,player_y))
    
def gameloop():
    global player_x, player_y
    if keyboard.right:
        player_x += 5
    elif keyboard.up:
        player_y += -5
    elif keyboard.down:
        player_y += 5
    elif keyboard.left:
        player_x += -5
clock.schedule_interval(gameloop,0.03)