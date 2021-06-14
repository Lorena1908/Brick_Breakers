import pygame
import random
pygame.font.init()

width, height = 780, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Brick Breakers')
font = pygame.font.SysFont('comicsans', 70)
lives = 5
score = 0

class Brick:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.width = 100
        self.height = 25
    
    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 26, 26)
        self.width = 100
        self.height = 15
    
    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self, paddle):
        self.x = 0
        self.y = 0
        self.radius = 15
        self.color = (26, 26, 255)
        self.xspeds = [-0.3, 0.3]
        self.xspeed = random.choice(self.xspeds)
        self.yspeed = -0.3
        self.still = True
        self.paddle = paddle
        self.out_of_lives = False
        self.win = False
    
    def draw(self):
        if self.still:
            self.reset()

        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def reset(self):
        self.still = True
        self.x = self.paddle.x + self.paddle.width/2
        self.y = self.paddle.y - self.radius
        self.xspeed = random.choice(self.xspeds)
        self.yspeed = -0.3

    def move(self):
        global lives, score
        if not self.still:
            self.x += self.xspeed
            self.y += self.yspeed
        
        # BORDER CHECKING
        if self.x >= width or self.x <= 0:
            self.xspeed *= -1
        
        if self.y <= 0:
            self.yspeed *= -1
        
        if self.y >= height:
            self.reset()
            lives -= 1

            if lives <= 0:
                self.out_of_lives = True

        # PADDLE AND BALL COLISIONS
        if self.paddle.x <= self.x <= self.paddle.x + self.paddle.width and self.paddle.y <= self.y <= self.paddle.y + self.paddle.height:
            self.y = self.paddle.y
            self.yspeed *= -1

        # PADDLE AND BRICK COLISIONS
        for i, brick in enumerate(bricks):
            if brick.x <= self.x <= brick.x + brick.width and brick.y <= self.y <= brick.y + brick.height:
                self.y = brick.y + brick.height
                bricks.pop(i)
                score += 1
                self.yspeed *= -1
            
        # CHECK WINNING
        if len(bricks) == 0:
            self.win = True
    

def draw_window(ball, paddle):
    # OBJECTS
    ball.draw()
    paddle.draw()

    for brick in bricks:
        brick.draw()

    # TEXT
    font1 = pygame.font.SysFont('comicsans', 30)
    lives_text = font1.render('Lives: {}'.format(lives), 1, (0, 219, 0))
    score_text = font1.render('Score: {}'.format(score), 1, (0, 219, 0))
    win.blit(score_text, (200,460))
    win.blit(lives_text, (400,460))
    pygame.display.update()

def reset_game():
    global score, lives
    score = 0
    lives = 5

def main():
    global bricks
    run = True
    paddle = Paddle(width/2 - 50, 430)
    ball = Ball(paddle)
    bricks = [
        Brick((255, 0, 102), 10,25),
        Brick((255, 0, 102), 120,25),
        Brick((255, 0, 102), 230,25),
        Brick((255, 0, 102), 340,25),
        Brick((255, 0, 102), 450,25),
        Brick((255, 0, 102), 560,25),
        Brick((255, 0, 102), 670,25),
        Brick((102, 255, 51), 10,60),
        Brick((102, 255, 51), 120,60),
        Brick((102, 255, 51), 230,60),
        Brick((102, 255, 51), 340,60),
        Brick((102, 255, 51), 450,60),
        Brick((102, 255, 51), 560,60),
        Brick((102, 255, 51), 670,60),
        Brick((255, 102, 0), 10,95),
        Brick((255, 102, 0), 120,95),
        Brick((255, 102, 0), 230,95),
        Brick((255, 102, 0), 340,95),
        Brick((255, 102, 0), 450,95),
        Brick((255, 102, 0), 560,95),
        Brick((255, 102, 0), 670,95),
        Brick((252,235,2), 10,130),
        Brick((252,235,2), 120,130),
        Brick((252,235,2), 230,130),
        Brick((252,235,2), 340,130),
        Brick((252,235,2), 450,130),
        Brick((252,235,2), 560,130),
        Brick((252,235,2), 670,130),
    ]
    seconds = 0
    clock = pygame.time.Clock()
    time = 0
    needed_time = 1000 # 1 second

    while run:
        clock.tick()
        time += clock.get_rawtime()
        win.fill((0,0,0))
        ball.move()
        draw_window(ball, paddle)

        if time >= needed_time and not ball.still:
            time = 0
            seconds += 1

            if seconds >= 5:
                seconds = 0
                if ball.xspeed < 0:
                    ball.xspeed -= 0.1
                else:
                    ball.xspeed += 0.1
                
                if ball.yspeed < 0:
                    ball.yspeed -= 0.1
                else:
                    ball.yspeed += 0.1

        if ball.out_of_lives:
            text = font.render('You Lost!', 1, (255, 26, 26))
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            run = False
            pygame.time.wait(2000)
        
        if ball.win:
            text = font.render('You Won!', 1, (255,215,0))
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            run = False
            pygame.time.wait(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            pygame.key.set_repeat(100)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    paddle.x += 30
                
                if event.key == pygame.K_LEFT:
                    paddle.x -= 30
                
                if event.key == pygame.K_UP:
                    ball.still = False

def menu_screen():
    run = True

    while run:
        win.fill((0,0,0))
        text = font.render('Press Any key to Play', 1, (255,255,255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                reset_game()
                main()
        

menu_screen()