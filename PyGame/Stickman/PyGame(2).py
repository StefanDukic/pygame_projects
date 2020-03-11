import os
import pygame
import numpy as np
from PIL import Image, ImageDraw
import time
import random

### CONSTANTS ###

# Windows
WIN_HEIGHT = 800
WIN_WIDTH = 1500
g = 2


# Framerate
FPS = 30
TIME_DELAY = int(1000 / FPS)
size = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(size)
image = pygame.image.load("data/background.png")
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
BG_COLOR = BLACK

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
        #file_path = f"data/ball_r={radius}_col={str(color).replace(' ', '').replace(',', '_')}.png"
        file_path_pac = f"data/PacMan.png"
        #if not os.path.isfile(file_path):
            #draw_bmp_circle(radius, color, file_path)  # draw image and save on disk if doesnt exist yet

        # ASSIGN CLASS ATTRIBUTES
        self.image = pygame.image.load(file_path_pac)  # load image
        self.rect = self.image.get_rect()  # create rectangle containing ball image
        self.rect.center = (int(xy_center[0]), int(xy_center[1]))  # set center coords of ball
        self.mass = mass  # is relevant for realistic collisions
        self.color = color
        self.vx = v[0]  # velocity
        self.vy = v[1]
        self.mask = pygame.mask.from_surface(
            self.image)  # creates a mask, used for collision detection (see manual about pygame.sprite.collide_mask())
        self.radius = radius
        self.resistence = 0.05
        self.vy_space_holder = self.vy
        self.touching_ground = False
        self.key_a = False
        self.key_d = False
        self.key_w = False
        self.key_s = False
        self.score = 0
        self.g = g

    def update(self):
        """
        determines motion of particles:

        """
        # TODO:
        # 1. General motion of particles
        #VY
        self.vy = self.vy_space_holder + self.g - self.resistence * self.vy
        self.vy_space_holder = self.vy

        #VX
        self.vx = self.vx - self.resistence * self.vx
        if abs(self.vx) < 0.05:
            self.vx = 0

        self.rect.y += self.vy
        self.rect.x += self.vx

        # 2. Bouncing off walls
        #Top_Bottom
        self.touching_ground = False
        if(self.rect.bottom >= WIN_HEIGHT or self.rect.y <= 0):
            if(self.rect.y < WIN_HEIGHT/2):
                self.vy = abs(self.vy)
                self.vy_space_holder = abs(self.vy)
                self.rect.y += self.vy
            else:
                self.touching_ground = True
                self.vy = -abs(self.vy)
                self.rect.y += self.vy
                self.vy_space_holder = -abs(self.vy)
                self.vy_space_holder = -abs(self.g - self.resistence * self.vy)

        #Left_Right
        if(self.rect.right >= WIN_WIDTH or self.rect.left <= 0):
            if (self.rect.x < WIN_WIDTH / 2):
                self.vx = abs(self.vx)
                self.rect.x += self.vx
            else:
                self.vx = -abs(self.vx)
                self.rect.x += self.vx



        #Input Action

        if self.key_d == True:
            self.vx += 6
            self.key_d = False
        if self.key_a == True:
            self.vx -= 6
            self.key_a = False
        if self.key_w == True:
            self.vy_space_holder -= 42
            self.key_w = False
        if self.key_s == True:
            self.vy_space_holder += 42
            self.key_s = False




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

class Coin(pygame.sprite.Sprite):
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
        self.resistence = 0.05
        self.vy_space_holder = self.vy
        self.touching_ground = False

    def update(self):
        """
        determines motion of particles:

        """
        # TODO:
        # 1. General motion of particles
        #VY
        self.vy = self.vy_space_holder - self.resistence * self.vy
        self.vy_space_holder = self.vy

        #VX
        self.vx = self.vx - self.resistence * self.vx
        if abs(self.vx) < 0.05:
            self.vx = 0

        self.rect.y += self.vy
        self.rect.x += self.vx

        # 2. Bouncing off walls
        #Top_Bottom
        self.touching_ground = False
        if(self.rect.bottom >= WIN_HEIGHT or self.rect.y <= 0):
            if(self.rect.y < WIN_HEIGHT/2):
                self.vy = abs(self.vy)
                self.vy_space_holder = abs(self.vy)
                self.rect.y += self.vy
            else:
                self.touching_ground = True
                self.vy = -abs(self.vy)
                self.rect.y += self.vy
                self.vy_space_holder = -abs(g - self.resistence * self.vy)

        #Left_Right
        if(self.rect.right >= WIN_WIDTH or self.rect.left <= 0):
            if (self.rect.x < WIN_WIDTH / 2):
                self.vx = abs(self.vx)
                self.rect.x += self.vx
            else:
                self.vx = -abs(self.vx)
                self.rect.x += self.vx

    def collide(self, coin_hit_list):
        """
        ball self collides with other ball, given as argument
        this method updates velocities of BOTH balls
        """

        # TODO
        # 1. two balls (self and ball) collide -> deal with collision
        v1 = np.array([coin_hit_list[0].vx, coin_hit_list[0].vy]).reshape(1,-1)
        v2 = np.array([coin_hit_list[1].vx, coin_hit_list[1].vy]).reshape(1,-1)
        x1 = coin_hit_list[0].rect.center
        x1 = np.asarray(x1)
        x2 = coin_hit_list[1].rect.center
        x2 = np.asarray(x2)
        x1 = x1.reshape(1,-1)
        x2 = x2.reshape(1,-1)
        m1 = coin_hit_list[0].mass
        m2 = coin_hit_list[1].mass

        v1new = v1 - 2 * m2 / (m1+m2) * np.vdot((v1 - v2), (x1 - x2)) / np.vdot((x1 - x2), (x1 - x2)) * (x1 - x2)
        v2new = v2 - 2 * m1 / (m1 + m2) * np.vdot((v2 - v1), (x2 - x1)) / np.vdot((x2 - x1), (x2 - x1)) * (x2 - x1)
        v1new = v1new.reshape(-1, 1)
        v2new = v2new.reshape(-1, 1)
        coin_hit_list[0].vx = v1new[0]
        coin_hit_list[0].vy = v1new[1]
        coin_hit_list[1].vx = v2new[0]
        coin_hit_list[1].vy = v2new[1]


        coin_hit_list[1].vy = 0

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
        Coins = pygame.sprite.Group()

        # CREATE OBJECTS AND ASSIGN TO GROUPS
        balls_list = [
            Ball([0.1 * WIN_WIDTH, 0.9 * WIN_HEIGHT], [0, 0], 64, 1, BLUE),
            Ball([0.9 * WIN_WIDTH, 0.25 * WIN_HEIGHT], [0, 0], 64, 1, BLACK)
            #Ball([0.50 * WIN_WIDTH, 0.75 * WIN_HEIGHT], [7, -7], 100, 1, WHITE)
            #Ball([0.50 * WIN_WIDTH, 0.25 * WIN_HEIGHT], [-4, 7], 100, 1, RED)
        ]

        random_list_hight = [random.uniform(0.8, 0.75), random.uniform(0.7, 0.65),
                            random.uniform(0.6, 0.55), random.uniform(0.5, 0.45)]
        random.shuffle(random_list_hight)
        coins_list = [
            Coin([random.uniform(0.1, 0.2) * WIN_WIDTH, random_list_hight[0] * WIN_HEIGHT], [0, 0], 18, 1, GOLD),
            Coin([random.uniform(0.3, 0.4) * WIN_WIDTH, random_list_hight[1] * WIN_HEIGHT], [0, 0], 18, 1, GOLD),
            Coin([random.uniform(0.5, 0.6) * WIN_WIDTH, random_list_hight[2] * WIN_HEIGHT], [0, 0], 18, 1, GOLD),
            Coin([random.uniform(0.7, 0.8) * WIN_WIDTH, random_list_hight[3] * WIN_HEIGHT], [0, 0], 18, 1, GOLD),
        ]
        random_list_hight = [random.uniform(0.8, 0.75), random.uniform(0.7, 0.65),
                            random.uniform(0.6, 0.55), random.uniform(0.5, 0.45)]

        Coins.add(coins_list)
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

            if balls_list[0].touching_ground == True:
                if keys[pygame.K_d]:
                    balls_list[0].key_d = True
                if keys[pygame.K_a]:
                    balls_list[0].key_a = True
                if keys[pygame.K_w]:
                    balls_list[0].key_w = True
                if keys[pygame.K_s]:
                    balls_list[0].key_s = True

            if balls_list[1].touching_ground == True:
                if keys[pygame.K_RIGHT]:
                    balls_list[1].key_d = True
                if keys[pygame.K_LEFT]:
                    balls_list[1].key_a = True
                if keys[pygame.K_UP]:
                    balls_list[1].key_w = True
                if keys[pygame.K_DOWN]:
                    balls_list[1].key_s = True

            if keys[pygame.K_ESCAPE]:
                self.exit()

            self.screen.fill(BG_COLOR)  # draw empty screen
            #screen.blit(image, [0, 0])

            # COLLISION DETECTION
            # see manual for all types of collisions: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollide
            # TODO: check for collisions between any two balls. If there is any, call the collision() method of the Ball class.
            for k in Balls:
                ball_hit_list = pygame.sprite.spritecollide(k, Balls, False, pygame.sprite.collide_circle_ratio(0.55))
                if len(ball_hit_list) > 1:
                    if self.realsleep(TIME_DELAY / 50000) == False:
                        if self.realsleep(TIME_DELAY/50000) == True:
                            Ball.collide(self, ball_hit_list)
                    else:
                        Ball.collide(self, ball_hit_list)

            for k in Coins:
                coin_hit_list = pygame.sprite.spritecollide(k, Balls, False, pygame.sprite.collide_circle_ratio(0.55))
                if len(coin_hit_list) >= 1:
                    coin_hit_list.append(k)
                    if self.realsleep(TIME_DELAY / 500) == False:
                        if self.realsleep(TIME_DELAY/500) == True:
                            balls_list[0].score += 1
                            balls_list[1].score += 1
                            Coin.collide(self, coin_hit_list)
                    else:
                        Coin.collide(self, coin_hit_list)
                        balls_list[0].score += 1
                        balls_list[1].score += 1


            # DRAW
            Balls.draw(self.screen)
            Coins.draw(self.screen)
            #PRINT SCORE
            font = pygame.font.Font(None, 36)
            text = font.render(str(balls_list[0].score), 1, (WHITE))
            textpos = text.get_rect(centerx=self.screen.get_width() * 0.25)
            self.screen.blit(text, textpos)

            font = pygame.font.Font(None, 36)
            text = font.render(str(balls_list[1].score), 1, (WHITE))
            textpos = text.get_rect(centerx=self.screen.get_width() * 0.75)
            self.screen.blit(text, textpos)


            # UPDATE
            Balls.update()
            Coins.update()

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    o1 = Game()
    o1.play()

