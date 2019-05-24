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
ball_vel = [0, 0]
# ball speed increase with each paddle reflection
ball_vel_multiplier = 1.1
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
# fixed paddle speed
paddle_speed = 5
score_left = 0
score_right = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel = [random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]
    elif direction == LEFT:
        ball_vel = [-random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score_left, score_right  # these are ints
    score_left = 0
    score_right = 0
    
    r = random.randrange(0, 1000)
    if r < 500:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)

def reset_h():
    new_game()
    
def draw(canvas):
    global score_left, score_right, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update ball
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        # Reflection from left paddle
        if ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT \
        and ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * ball_vel_multiplier
        else:
            score_right += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        # Reflection from right paddle
        if ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT \
        and ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * ball_vel_multiplier
        else:
            score_left += 1
            spawn_ball(LEFT)
    
    # Vertical reflection
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos + paddle1_vel > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle1_pos += paddle1_vel
    
    if paddle2_pos + paddle2_vel < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos + paddle2_vel > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos - HALF_PAD_HEIGHT),
                         (PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),
                         (PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT),
                         (0, paddle1_pos + HALF_PAD_HEIGHT)],
                        1, "White", "White")
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT),
                         (WIDTH, paddle2_pos - HALF_PAD_HEIGHT),
                         (WIDTH, paddle2_pos + HALF_PAD_HEIGHT),
                         (WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)],
                        1, "White", "White")
    
    # draw scores
    canvas.draw_text(str(score_left), [WIDTH / 2 - 60, HEIGHT / 2 - 50], 50, "Red", "sans-serif")
    canvas.draw_text(str(score_right), [WIDTH / 2 + 30, HEIGHT / 2 - 50], 50, "Red", "sans-serif")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -paddle_speed
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = paddle_speed
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -paddle_speed
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = paddle_speed
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    # doublechecking for speed to avoid situations such as
    # "releasing 'w' key happens after pressing 's' and stops the paddle"
    if key == simplegui.KEY_MAP['w'] and paddle1_vel == -paddle_speed:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s'] and paddle1_vel == paddle_speed:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up'] and paddle2_vel == -paddle_speed:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down'] and paddle2_vel == paddle_speed:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", reset_h, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
