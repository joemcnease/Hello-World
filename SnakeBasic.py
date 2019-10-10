import sys
import random
import pygame

class Snake:
    """ Initialize Snake class with starting dimensions, position,
    and velocity of the snake. """

    snake_body = []

    def __init__(self, x, y, width, height, velocity, color=(0,255,0), score=0):
        """
        (x, y): denotes always positive postion from top left (0,0).
        (width, height): describes height and width of snake.
        velocity: defines how much (x, y) values change with each move.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.color = color
        # self.hitbox = (self.x, self.y, self.width, self.height)
        self.score = score

    def draw_snake(self):
        """ Redraws rectangles that are the "Snake". """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # self.hitbox = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(screen, (0, 0, 255), self.hitbox, 2)

    # Basic movement function
    def move_left(self):
        if self.x > 0:
            self.x -= self.velocity

    def move_right(self):
        if self.x < win.width - player1.width:
            self.x += self.velocity

    def move_up(self):
        if self.y > 0:
            self.y -= self.velocity

    def move_down(self):
        if self.y < win.height - player1.height:
            self.y += self.velocity

    # Functions to make game competitive
    def death(self):
        """ If the snake meets the boundary of the screen, he/she will die. """
        death_sound.play()
        Snake.snake_body = []
        Food.food = []
        player1.x, player1.y = 400, 400

    def add_score(self):
        score_sound.play()
        self.score += 1

class Food:
    """ Food class. """

    food = []

    def __init__(self, x, y, radius, color=(255,0,0)):
        """ Gives food basic pygame rect attributes. """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw_food(self):
        """ Redraws circles (Food) to screen. """
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Window:
    """ Sets basic window parameters. """
    def __init__(self, width, height):
        self.width = width
        self.height = height

# Should probably put this in Window class
def redraw_game_window():
    """
    Main graphics function.
    1.) Screen is filled black
    2.) Player1's "head" is drawn
    3.) Player1's "body" is drawn
    4.) Food is drawn
    """
    screen.fill((0,0,0))
    player1.draw_snake()
    for s in Snake.snake_body:
        s.draw_snake()
    for f in Food.food:
        f.draw_food()

    pygame.display.update()

# Initialize pygame and mixer (sounds)
pygame.mixer.pre_init(44100, -16, 2, 64)
pygame.mixer.init()
pygame.init()

# Vital objects and variables to instantiate and initialize
win = Window(800, 800)
screen = pygame.display.set_mode((win.width, win.height))
pygame.display.set_caption("Snake")

# Create instance of sound
death_sound = pygame.mixer.Sound('WallHit.ogg')
score_sound = pygame.mixer.Sound('ScoreUpSound.ogg')

player1 = Snake(400, 400, 20, 20, 10)

# Delay time for Main Loop
game_speed = 30

run = True

# Extra Screens for score, etc...
# Not sure how to do this. Maybe increase window size and keep player boundary the
# same. Then print score to unused area of window.

# This can be added to Snake class, but should have a default value.
# The default value (currently 'left') can also be randomly chosen, 
# you just have to make a list and use random.choice(list)
direction = ['left']

# Main Loop
# This is where most of the game logic lies
while run:
    pygame.time.delay(game_speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Checks if player hits edge of window and if that is True, the player1.death() fucntion is called.
    if player1.x == win.width - player1.width or player1.x == 0 or player1.y == win.height - player1.height or player1.y == 0:
        player1.death()

    # If there is no food, add a piece.
    # If there is check if snake head is touching, if True empty food list and add another item to snake_list.
    if Food.food == []:
        Food.food.append(Food(random.randrange(0, win.width - 5), random.randrange(0, win.height -5), 5))
    else:
        for f in Food.food:
            if f.x + f.radius > player1.x - (player1.width/2) and f.x - f.radius < player1.x + player1.width:
                if f.y + f.radius > player1.y - (player1.height/3) and f.y - f.radius < player1.y + player1.height:
                    Food.food.remove(f)
                    player1.add_score()
                    print(player1.score)

                    # Add segment to snake
                    tail = Snake(player1.x, player1.y, player1.width, player1.height, player1.velocity)
                    Snake.snake_body.append(tail)

    # Move segments in reverse order
    for index in range(len(Snake.snake_body) - 1, 0, -1):
        x = Snake.snake_body[index - 1].x
        y = Snake.snake_body[index - 1].y
        Snake.snake_body[index].x = x
        Snake.snake_body[index].y = y

    # If length of snake > 0, then move only snake_body item to previous head position
    if len(Snake.snake_body) > 0:
        x = player1.x
        y = player1.y
        Snake.snake_body[0].x = x
        Snake.snake_body[0].y = y

    # Calls Snake.move() methods if direction list contains 'direction'.
    if direction[-1] == 'left':
        player1.move_left()

    elif direction[-1] == 'right':
        player1.move_right()

    elif direction[-1] == 'up':
        player1.move_up()

    elif direction[-1] == 'down':
        player1.move_down()

    # This is how you check for keypresses in Pygame.
    # pygame.key.get_pressed() is a dictionary with boolean values.
    # If key == K_LEFT, K_RIGHT, K_UP, K_DOWN then it executes code.
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        direction.append('left')
        del direction[:-1]

    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        direction.append('right')
        del direction[:-1]

    elif pygame.key.get_pressed()[pygame.K_UP]:
        direction.append('up')
        del direction[:-1]

    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        direction.append('down')
        del direction[:-1]

    redraw_game_window()

pygame.quit()
