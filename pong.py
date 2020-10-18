# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400   

BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
vel = [3, -1]

paddle1_pos = [0,HEIGHT / 2]
paddle2_pos = [595, HEIGHT / 2]

paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction): #helper
    global ball_pos, ball_vel, vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == "LEFT":
        vel = [-3, -1]
    elif direction == "RIGHT": 
        vel = [3, -1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)
    
def draw(canvas):    
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += vel[0]
    ball_pos[1] += vel[1]

    # draw paddles
    paddle1_a = paddle1_pos
    paddle1_b = (paddle1_pos[0], paddle1_pos[1] - PAD_HEIGHT)
    paddle1_c = (paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1] - PAD_HEIGHT)
    paddle1_d = (paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1])
    canvas.draw_polygon([paddle1_a, paddle1_b, paddle1_c, paddle1_d], 2, "White", "White")

    paddle2_a = paddle2_pos
    paddle2_b = (paddle2_pos[0], paddle2_pos[1] - PAD_HEIGHT)
    paddle2_c = (paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1] - PAD_HEIGHT)
    paddle2_d = (paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1])
    canvas.draw_polygon([paddle2_a, paddle2_b, paddle2_c, paddle2_d], 2, "White", "White")
  
    #boundary collision
    if ball_pos[0] <= BALL_RADIUS: 
        vel[0] = -vel[0]
    elif ball_pos[0] >= WIDTH - BALL_RADIUS:
        vel[0] = -vel[0]
    elif ball_pos[1] <= BALL_RADIUS:
        vel[1] = -vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        vel[1] = -vel[1]
    
    #gutter collision
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        if ball_pos[1] <= paddle1_d[1] and ball_pos[1] >= paddle1_c[1]:
            vel[0] = -vel[0]
            vel[0] = vel[0] + 1
        else: 
            spawn_ball("RIGHT")

    elif ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        if ball_pos[1] <= paddle2_d[1] and ball_pos[1] >= paddle2_c[1]:
            vel[0] = -vel[0]
            vel[0] = vel[0] - 1

        else:
            spawn_ball("LEFT")
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] = paddle1_pos[1] - paddle1_vel
    paddle2_pos[1] = paddle2_pos[1] + paddle2_vel
   
    # determine whether paddle and ball collide    

    
    # draw scores
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 2
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = -2
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -2
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 2
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
