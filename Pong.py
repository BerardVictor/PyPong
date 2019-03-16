import random
import sys
import pygame
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

fenetre= pygame.display.set_mode((640, 480))
pygame.display.set_caption("pypong")
BLACK= (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE= (255,255,255)

#terrain= pygame.Surface (fenetre.get_size())
#terrain.fill (BLACK)
#pygame.draw.rect(terrain, WHITE, Rect((5, 5), (630, 470)), 2)
#pygame.draw.aaline(terrain, WHITE, (350, 5), (330, 475))


WIDTH = 640
HEIGHT = 480
BALL_RADIUS = 20
ball_pos = [0,0]
ball_vel = [0,0]


PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

pause = False
menu = False

score1 = 0 
score2 = -1

music = pygame.mixer.Sound("D:/PyPong/PyPong/music.wav")
music.play(-1)

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH//2,HEIGHT//2]
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)
    
#    if right == False:
#        horz = - horz

    ball_vel = [horz,-vert]

    # define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)




#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, score1, score2

    canvas.fill(BLACK)
    
    fenetre.blit(canvas, (0,0))
    background = pygame.image.load("D:/PyPong/PyPong/terraintennis.jpg")
    fenetre.blit(background, (0,0))

    #son
    rebond = pygame.mixer.Sound("D:/PyPong/PyPong/rebond.wav")
    frappe = pygame.mixer.Sound("D:/PyPong/PyPong/frappe.wav")

     # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel

    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

        #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    pygame.draw.circle(canvas, green, ball_pos, 10, 0)
    pygame.draw.polygon(canvas, blue, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, red, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        rebond.play()

    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        rebond.play()

       
    
    if int(ball_pos[0]) > 640 or int(ball_pos[0]) < 0 :
        ball_vel[0] = -ball_vel[0]
        rebond.play()

    if int(ball_pos[1]) > 480 or int(ball_pos[1]) < 0 :
        ball_vel[1] = -ball_vel[1]
        rebond.play()


    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.5
        ball_vel[1] *= 1.5
        frappe.play()


    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
    
        ball_init(True)
        score2 +=1
    

    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
        frappe.play()

    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
      
        ball_init(False)
        score1 +=1
    
    #affichage score
    font = pygame.font.SysFont('Calibri', 40, True, False)
    scorep1 = font.render(''+str(score1),True,blue)
    fenetre.blit(scorep1, [10,25])

    scorep2 = font.render(''+str(score2),True,red)
    fenetre.blit(scorep2, [610,25])

    #menu
    fontmenu = pygame.font.SysFont('Calibri', 25, False,False)
    textmenu = fontmenu.render('Press X for Menu', True, white)
    fenetre.blit(textmenu, [70,10])
   

    #keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel,pause, menu

    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8
    elif event.key == pygame.K_p : 
        pause = True
        paused()
    elif event.key == pygame.K_SPACE : 
        pause = False
    elif event.key == pygame.K_x : 
        pause = True
        menu()

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel, pause

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0



def paused():
    global pause
    font = pygame.font.SysFont('Calibri', 100, True, False)
    textpause = font.render('PAUSE', True, white)
    fenetre.blit(textpause,[174,200])
    

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.key == K_p : 
                pause=True
            if event.key == K_SPACE :
                pause=False
            pygame.display.update()

def menu():
    global menu
    menu = pygame.image.load("D:/PyPong/PyPong/menu.jpg").convert()
    fenetre.blit(menu, (40,40))

    while menu : 
        for event in pygame.event.get() :

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.key == K_x :
                menu = True
            if event.key == K_ESCAPE : 
                menu = False
            pygame.display.update()



#game loop
while True:

    draw(fenetre)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)

        elif event.type == KEYUP:
            keyup(event)

        elif event.type == pygame.K_p : 
            pause = True
            paused()

        elif event.type == pygame.K_x :
            pause = True
            menu()

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps.tick(60)
