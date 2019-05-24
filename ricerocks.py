# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
last_score = 0
lives = 3
time = 0.5
started = False
msg_gameover = "Game over"

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroids_img = [asteroid_image,
                 simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png"),
                 simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")
                 ]

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(canvas, sprite_group):
    for sp in set(sprite_group):
        sp.draw(canvas)
        if sp.update():
            sprite_group.discard(sp)
        
# takes a set of objects and an object and removes all elements that collide with object
def group_collide(group, obj, both_explode = False):
    global explosions
    col = False
    for e in set(group):
        if e.collides(obj):
            explosions.add(Sprite(e.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            group.discard(e)
            col = True
    if col and both_explode:
        explosions.add(Sprite(obj.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
        obj.destroy()        
    return col

def group_group_collide(gr1, gr2):
    cols = 0
    for e1 in set(gr1):
        if group_collide(gr2, e1):
            gr1.discard(e1)
            cols += 1
    return cols

def new_game():
    global started, score, lives, my_ship, rocks, missiles, explosions
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    rocks = set([])
    missiles = set([])
    explosions = set([])
    if not started:
        score = 0
        lives = 3
        soundtrack.rewind()
        soundtrack.play()
        started = True

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.destroyed = False
        self.death_time = 0
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_death_time(self):
        return self.death_time
    
    def is_destroyed(self):
        return self.destroyed
    
    def destroy(self):
        self.thrusters(False)
        self.destroyed = True
        self.death_time = time
        
    def change_angle(self, angle):
        self.angle_vel = angle
    
    def turn_right(self):
        self.change_angle(0.05)
    
    def turn_left(self):
        self.change_angle(-0.05)
    
    def stop_turning(self):
        self.change_angle(0)
        
    def thrusters(self, state=True):
        if self.destroyed:
            return
        self.thrust = state
        if state: # thrusters on
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else: # thrusters off
            ship_thrust_sound.pause()
            
    def shoot(self):
        global missiles
        if self.destroyed:
            return
        vect = angle_to_vector(self.angle)
        missiles.add(Sprite([self.pos[0] + vect[0]*self.radius, self.pos[1] + vect[1]*self.radius],
                            [self.vel[0] + 10*vect[0], self.vel[1] + 10*vect[1]],
                            self.angle, 0,
                            missile_image, missile_info, missile_sound))
    
    def draw(self,canvas):
        if self.destroyed:
            return
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        if self.destroyed:
            return
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update angle
        self.angle += self.angle_vel
        # update velocity
        if self.thrust:
            acc_vector = angle_to_vector(self.angle)
            self.vel[0] += 0.05 * acc_vector[0]
            self.vel[1] += 0.05 * acc_vector[1]
        # friction
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.destroyed = False
        if sound:
            sound.rewind()
            sound.play()
            
    def is_destroyed(self):
        return self.destroyed
    
    def destroy(self):
        self.destroyed = True
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if self.destroyed:
            return
        
        if self.animated:
            index = (self.age % 24) // 1
            center = [self.image_center[0] + index * self.image_size[0], self.image_center[1]]
        else:
            center = self.image_center
        canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        if self.destroyed:
            return
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update angle
        self.angle += self.angle_vel
        # update age
        self.age += 1
        if self.age <= self.lifespan:
            return False
        else:
            return True
        
    def collides(self, other_object):
        return dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius()

           
def draw(canvas):
    global time, started, lives, score, last_score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if started:
        # draw and update ship and sprites
        process_sprite_group(canvas, rocks)
        process_sprite_group(canvas, explosions)
        # user interface
        canvas.draw_text("lives: "+str(lives), [WIDTH-150, 30], 14, "White")
        canvas.draw_text("score: "+str(score), [WIDTH-70, 30], 14, "White")
        # checking lives
        if lives <= 0:
            if time >= my_ship.get_death_time() + 240:
                started = False
            else:
                x = WIDTH / 2 - (frame.get_canvas_textwidth(msg_gameover, 60, "monospace") / 2)
                y = HEIGHT / 2 + 20
                canvas.draw_text("Game over", [x - 1, y - 1], 60, "#c00", "monospace")
                canvas.draw_text("Game over", [x, y], 60, "#ccc", "monospace")
        if not my_ship.is_destroyed():
            my_ship.draw(canvas)
            my_ship.update()
            process_sprite_group(canvas, missiles)
            # update score
            score += group_group_collide(missiles, rocks)
            # update lives
            if group_collide(rocks, my_ship, True):
                lives -= 1
        else:
            if time >= my_ship.get_death_time() + 120:
                new_game()
    else: # draw splash screen if not started
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        canvas.draw_text("Last score: "+str(score), [WIDTH / 2 - 80, HEIGHT / 2 - 100], 26, "White")
        soundtrack.pause()

# timer handler that spawns a rock    
def rock_spawner():
    global rocks
    if not started or len(rocks) >= 12:
        return
    pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    # not spawning rocks too close to the ship
    if dist(pos, my_ship.get_position()) <= 150:
        return
    vel = [random.randrange(-100, 100) / 50.0, random.randrange(-100, 100) / 50.0]
    # speed increases with score
    vel[0] += (1 + score) / 100
    vel[1] += (1 + score) / 100
    ang = random.randrange(62) / 10.0
    ang_v = (abs(vel[0]) + abs(vel[1])) / 50.0 # the faster it moves the faster it turns
    ang_v *= random.choice([-1, 1]) # random spinning direction
    rocks.add(Sprite(pos, vel, ang, ang_v, random.choice(asteroids_img), asteroid_info))

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives
    if started:
        return
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    
    if inwidth and inheight: # new game
        new_game()

def keydown(key):
    if not started:
        return
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn_left()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.turn_right()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusters()
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
    
def keyup(key):
    if not started:
        return
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        my_ship.stop_turning()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusters(False)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
