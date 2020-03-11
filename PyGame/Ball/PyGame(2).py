import os
import pygame
import numpy as np
from PIL import Image, ImageDraw
import time

### CONSTANTS ###

# Windows
WIN_HEIGHT = 800
WIN_WIDTH = 1000
g = 7


# Framerate
FPS = 30
TIME_DELAY = int(1000 / FPS)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = GREEN

score = 0
### METHODS ###

def draw_bmp_circle(radius, color, path):
    """
    creates circle image and saves on disk
    """
    img = Image.new('RGBA', (radius, radius), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, radius - 1, radius - 1), fill=color)
    img.save(path, 'PNG')


### CLASSES ###

class Ball(pygame.sprite.Sprite):
    def __init__(self, xy_center, v, radius, mass, color):
        super().__init__()  # call __init__ of parent class (i.e. of pygame.sprite.Sprite)

        # CREATE BALL IMAGE (if does not exist yet)
        file_path = f"data/ball_r={radius}_col={str(color).replace(' ', '').replace(',', '_')}.png"
        if not os.path.isfile(file_path):
            draw_bmp_circle(radius, color, file_path)  # draw image and save on disk if doesnt exist yet

        # ASSIGN CLASS ATTRIBUTES
        self.image = pygame.image.load(file_path)  # load image
        self.rect = self.image.get_rect()  # create rectangle containing ball image
        self.rect.center = (int(xy_center[0]), int(xy_center[1]))  # set center coords of ball
        self.mass = mass  # is relevant for realistic collisions
        self.color = color
        self.vx = v[0]  # velocity
        self.vy = v[1]
        self.mask = pygame.mask.from_surface(
            self.image)  # creates a mask, used for collision detection (see manual about pygame.sprite.collide_mask())
        self.radius = radius

    def update(self):
        """
        determines motion of particles:

        """
        # TODO:
        # 1. General motion of particles



        self.vy = self.vy + g



        self.rect.y += self.vy
        self.rect.x += self.vx

        # 2. Bouncing off walls

        if(self.rect.y >= WIN_HEIGHT - self.radius or self.rect.y <= 0):
            print("Jetzt")
            if(self.rect.y < WIN_HEIGHT/2):
                self.vy = abs(self.vy)
                self.rect.y += self.vy

            else:
                self.vy = -abs(self.vy)
                self.rect.y += self.vy

        if(self.rect.x >= WIN_WIDTH - self.radius or self.rect.x <= 0):
            if (self.rect.x < WIN_WIDTH / 2):
                self.vx = abs(self.vx)
                self.rect.x += self.vx
            else:
                self.vx = -abs(self.vx)
                self.rect.x += self.vx





        # do NOT deal with collisions in here

    def collide(self, ball_hit_list):
        """
        ball self collides with other ball, given as argument
        this method updates velocities of BOTH balls
        """
        # TODO
        # 1. two balls (self and ball) collide -> deal with collision
        v1 = np.array([ball_hit_list[0].vx, ball_hit_list[0].vy]).reshape(1,-1)
        v2 = np.array([ball_hit_list[1].vx, ball_hit_list[1].vy]).reshape(1,-1)
        x1 = ball_hit_list[0].rect.center
        x1 = np.asarray(x1)
        x2 = ball_hit_list[1].rect.center
        x2 = np.asarray(x2)
        x1 = x1.reshape(1,-1)
        x2 = x2.reshape(1,-1)
        m1 = ball_hit_list[0].mass
        m2 = ball_hit_list[1].mass

        v1new = v1 - 2 * m2 / (m1+m2) * np.vdot((v1 - v2), (x1 - x2)) / np.vdot((x1 - x2), (x1 - x2)) * (x1 - x2)
        v2new = v2 - 2 * m1 / (m1 + m2) * np.vdot((v2 - v1), (x2 - x1)) / np.vdot((x2 - x1), (x2 - x1)) * (x2 - x1)
        v1new = v1new.reshape(-1, 1)
        v2new = v2new.reshape(-1, 1)
        ball_hit_list[0].vx = v1new[0]
        ball_hit_list[0].vy = v1new[1]
        ball_hit_list[1].vx = v2new[0]
        ball_hit_list[1].vy = v2new[1]




        # Theory of collision btw two balls: https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional (last formula)

        # 2. try to avoid 'ball dances'


class Game:
    """
    Main GAME class
    """

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.time_delay = TIME_DELAY
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # create screen which will display everything
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Bouncing Balls")  # Game title
        self.bool = False
        self.seconds = time.time()

    def realsleep(self, pause):
        if time.time() - self.seconds > pause:
            self.seconds = time.time()
            k = True
        else:
            k = False
        return k

    def play(self):
        # CREATE GAME GROUPS
        Balls = pygame.sprite.Group()

        # CREATE OBJECTS AND ASSIGN TO GROUPS
        balls_list = [
            Ball([0.25 * WIN_WIDTH, 0.75 * WIN_HEIGHT], [0, 0], 100, 1, BLUE),
            Ball([0.25 * WIN_WIDTH, 0.50 * WIN_HEIGHT], [0, 0], 100, 1, BLACK)
            #, Ball([0.50 * WIN_WIDTH, 0.75 * WIN_HEIGHT], [7, -7], 100, 1, WHITE)
            #, Ball([0.50 * WIN_WIDTH, 0.25 * WIN_HEIGHT], [-4, 7], 100, 1, RED)
        ]


        Balls.add(balls_list)

        # GAME PERMANENT LOOP
        while True:
            pygame.time.delay(TIME_DELAY)

            # KEY EVENTS
            for event in pygame.event.get():
                # Exit app if click quit button
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                print("W")

            if keys[pygame.K_ESCAPE]:
                self.exit()

            self.screen.fill(BG_COLOR)  # draw empty screen

            # COLLISION DETECTION
            # see manual for all types of collisions: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollide
            # TODO: check for collisions between any two balls. If there is any, call the collision() method of the Ball class.
            for k in Balls:
                ball_hit_list = pygame.sprite.spritecollide(k, Balls, False, pygame.sprite.collide_circle_ratio(0.55))
                if len(ball_hit_list) > 1:
                    if self.realsleep(TIME_DELAY / 500) == False:
                        if self.realsleep(TIME_DELAY/500) == True:
                            Ball.collide(self, ball_hit_list)
                    else:
                        Ball.collide(self, ball_hit_list)







            # DRAW
            Balls.draw(self.screen)

            # UPDATE
            Balls.update()

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    Game().play()

