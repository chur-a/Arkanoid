import pygame


def platform():
    global x_platform
    if keys[pygame.K_LEFT] and x_platform > 0:
        x_platform -= 8
        pygame.draw.rect(screen, (100, 0, 0), (x_platform, y_platform, lenght_platform, height_platform))
    elif keys[pygame.K_RIGHT] and x_platform < 1000 - lenght_platform:
        x_platform += 8
        pygame.draw.rect(screen, (100, 0, 0), (x_platform, y_platform, lenght_platform, height_platform))
    else:
        pygame.draw.rect(screen, (100, 0, 0), (x_platform, y_platform, lenght_platform, height_platform))


def ball_direction(vx, vy):
    global vx_ball, vy_ball, x_ball, y_ball
    vx_ball = vx
    vy_ball = vy
    x_ball += vx_ball
    y_ball -= vy_ball
    pygame.draw.circle(screen, (232, 163, 23), (x_ball, y_ball), radius_ball)


def angle_change():
    if x_platform - radius_ball < x_ball+vx_ball <= x_platform + lenght_platform/4:
        ball_direction(-7, 3)
    elif x_platform + lenght_platform/4 < x_ball+vx_ball <= x_platform + lenght_platform/2:
        ball_direction(-5, 4)
    elif x_platform + lenght_platform/2 < x_ball+vx_ball <= x_platform + 3*lenght_platform/4:
        ball_direction(5, 4)
    elif x_platform + 3*lenght_platform/4 < x_ball+vx_ball <= x_platform + lenght_platform + radius_ball:
        ball_direction(7, 3)


def ball():
    global start_mode, x_ball, y_ball
    if start_mode:
        x_ball = x_platform + lenght_platform//2
        y_ball = y_platform - radius_ball
        pygame.draw.circle(screen, (232, 163, 23), (x_ball, y_ball), radius_ball)
    if keys[pygame.K_SPACE] and start_mode:
        start_mode = False
    elif not start_mode:
        if y_ball - vy_ball < 0:
            ball_direction(vx_ball, -vy_ball)
        elif x_ball + vx_ball > 1000 or x_ball + vx_ball < 0:
            ball_direction(-vx_ball, vy_ball)
        elif (
                x_platform - radius_ball < x_ball+vx_ball < x_platform + lenght_platform + radius_ball and
                y_platform <= y_ball - vy_ball + radius_ball < y_platform+10
        ):
            angle_change()
        elif y_platform - radius_ball < y_ball < y_platform + height_platform + radius_ball:
            if (
                    x_platform - 5 < x_ball + radius_ball <= x_platform + 5 or
                    x_platform + lenght_platform - 5 <= x_ball - radius_ball < x_platform + lenght_platform + 5
            ):
                ball_direction(-vx_ball, vy_ball)
            else:
                ball_direction(vx_ball, vy_ball)
        else:
            ball_direction(vx_ball, vy_ball)


def rectangles_draw():
    for y, x in Rectangles:
        pygame.draw.rect(screen, (100, 100, 50), (2+x*step_x, 2+y*step_y, width_rectangle, height_rectangle))


def coliisions_of_ball_rectangles():
    global Rectangles, y_ball, vy_ball
    Delete_rectangles = []
    for j, i in Rectangles:
        x_rect = 2+i*step_x
        y_rect = 2+j*step_y
        if x_rect - radius_ball < x_ball < x_rect + width_rectangle + radius_ball:
            if (
                    y_rect + height_rectangle - 10 < y_ball - radius_ball <= y_rect + height_rectangle or
                    y_rect + 10 < y_ball + radius_ball <= y_rect
            ):
                ball_direction(vx_ball, -vy_ball)
                Delete_rectangles.append((j, i))
        elif y_rect - radius_ball < y_ball < y_rect+height_rectangle+radius_ball:
            if (
                    x_rect - 15 < x_ball + radius_ball <= x_rect or
                    x_rect + width_rectangle <= x_ball - radius_ball <= x_rect + width_rectangle + 15
            ):
                ball_direction(-vx_ball, vy_ball)
                Delete_rectangles.append((j, i))
    for i in Delete_rectangles:
        Rectangles.remove(i)
                
                
def pause():
    global paused_mode, flag
    if keys[pygame.K_ESCAPE]:
        paused_mode = True
        text = font.render('Game is paused. Press ENTER', True, (0, 0, 0))
    while paused_mode:
        clock.tick(5)
        screen.blit(text, (300, 500))
        keys_local = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                paused_mode = False
        if keys_local[pygame.K_RETURN]:
            paused_mode = False
            
        pygame.display.update()


def check_game_over():
    if y_ball - radius_ball > height:
        return True
    return False


def endgame():
    global endgame_mode, flag
    if len(Rectangles) == 0 or check_game_over():
        endgame_mode = True
        screen.blit(background, (0, 0))
        text = (font.render('You win!!', True, (0, 0, 0)) if len(Rectangles) == 0 else
                font.render('You lose', True, (0, 0, 0)) if check_game_over() else None)
    while endgame_mode:
        clock.tick(5)
        screen.blit(text, (450, 500))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                endgame_mode = False
            
        pygame.display.update()
            

pygame.init()

flag = True
width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
background = pygame.image.load('assets/Fon.jpg.')
font = pygame.font.Font('assets/UniversCondensed.ttf', 40)

x_platform = 300
y_platform = 800
lenght_platform = 400
height_platform = 30

start_mode = True
radius_ball = 30
vx_ball = 0
vy_ball = 3
x_ball = x_platform+lenght_platform//2
y_ball = y_platform-radius_ball

Rectangles = set()
number_of_rectangles_y = 6
number_of_rectangles_x = 8
for i in range(number_of_rectangles_y):
    for j in range(number_of_rectangles_x):
        Rectangles.add((i, j))
        
step_x = 125
step_y = 35
width_rectangle = 120
height_rectangle = 25

paused_mode = False

endgame_mode = False

while flag:
    clock.tick(140)
    keys = pygame.key.get_pressed()
    screen.blit(background, (0, 0))
    
    platform()
    ball()
    rectangles_draw()
    coliisions_of_ball_rectangles()
    
    pause()
    endgame()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
    
    pygame.display.update()

pygame.quit()
