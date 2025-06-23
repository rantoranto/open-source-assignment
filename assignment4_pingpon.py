import pygame, sys, math, random, time
from pygame.locals import *

pygame.init()
pygame.display.set_caption("20256562 김권택")
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
ball_sprite = pygame.image.load("C:/Users/ball.png").convert_alpha()
ball_sprite = pygame.transform.scale(ball_sprite, (45, 45))

right_score = 0
left_score = 0
main_font = pygame.font.Font(None, 40)
title_font = pygame.font.SysFont("corbel", 70)
score_font = pygame.font.Font(None, 60)
start_time = time.time()

class Paddle:
    def __init__(self, keys, x_pos, direction):
        self.keys = keys
        self.x = x_pos
        self.y = 260
        self.direction = direction
        self.last_smash = 0

    def update(self):
        if pressed_keys[self.keys[0]] and self.y > 0:
            self.y -= 10
        if pressed_keys[self.keys[1]] and self.y < 520:
            self.y += 10

    def render(self):
        offset = -self.direction * (time.time() < self.last_smash + 0.5) * 10
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (self.x + offset, self.y + 80), 6)

    def smash(self):
        if time.time() > self.last_smash + 0.3:
            self.last_smash = time.time()

class GameBall:
    def __init__(self):
        self.angle = (math.pi / 3) * random.random() + (math.pi / 3) + math.pi * random.randint(0, 1)
        self.speed = 12
        self.vx = math.sin(self.angle) * self.speed
        self.vy = math.cos(self.angle) * self.speed
        self.x = 475
        self.y = 275

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def render(self):
        screen.blit(ball_sprite, (int(self.x), int(self.y)))

    def check_collision(self):
        if (self.y <= 0 and self.vy < 0) or (self.y >= 550 and self.vy > 0):
            self.vy *= -1
            self.angle = math.atan2(self.vx, self.vy)

        for paddle in paddles:
            if pygame.Rect(paddle.x, paddle.y, 6, 80).colliderect(self.x, self.y, 50, 50) and abs(self.vx) / self.vx == paddle.direction:
                self.angle += random.random() * math.pi / 4 - math.pi / 8

                if (0 < self.angle < math.pi / 6) or (math.pi * 5 / 6 < self.angle < math.pi):
                    self.angle = ((math.pi / 3) * random.random() + (math.pi / 3))
                elif (math.pi < self.angle < math.pi * 7 / 6) or (math.pi * 11 / 6 < self.angle < math.pi * 2):
                    self.angle = ((math.pi / 3) * random.random() + (math.pi / 3)) + math.pi

                self.angle *= -1
                self.angle %= math.pi * 2

                if time.time() < paddle.last_smash + 0.05 and self.speed < 20:
                    self.speed *= 1.5

                self.vx = math.sin(self.angle) * self.speed
                self.vy = math.cos(self.angle) * self.speed

game_ball = GameBall()
paddles = [Paddle([K_a, K_z], 10, -1), Paddle([K_UP, K_DOWN], 984, 1)]

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_q:
                paddles[0].smash()
            if event.key == K_RSHIFT:
                paddles[1].smash()

    pressed_keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    pygame.draw.line(screen, (255, 255, 255), (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()), 3)
    pygame.draw.circle(screen, (255, 255, 255), (int(screen.get_width() / 2), int(screen.get_height() / 2)), 50, 3)

    timer_text = main_font.render(str(int(60 - (time.time() - start_time))), True, (255, 255, 255))
    screen.blit(timer_text, (screen.get_width() / 2 - timer_text.get_width() / 2, 20))

    for paddle in paddles:
        paddle.update()
        paddle.render()

    if game_ball.x < -50:
        game_ball = GameBall()
        right_score += 1

    if game_ball.x > 1000:
        game_ball = GameBall()
        left_score += 1

    game_ball.update()
    game_ball.render()
    game_ball.check_collision()

    score_text_left = main_font.render(str(left_score), True, (255, 255, 255))
    screen.blit(score_text_left, (20, 20))
    score_text_right = main_font.render(str(right_score), True, (255, 255, 255))
    screen.blit(score_text_right, (980 - score_text_right.get_width(), 20))

    if right_score > 9 or left_score > 9 or time.time() - start_time > 60:
        title = title_font.render("score", True, (255, 0, 255))
        screen.blit(title, (screen.get_width() / 4 - title.get_width() / 2, screen.get_height() / 4))
        screen.blit(title, (screen.get_width() * 3 / 4 - title.get_width() / 2, screen.get_height() / 4))

        final_score_left = score_font.render(str(left_score), True, (255, 255, 255))
        screen.blit(final_score_left, (screen.get_width() / 4 - final_score_left.get_width() / 2, screen.get_height() / 2))

        final_score_right = score_font.render(str(right_score), True, (255, 255, 255))
        screen.blit(final_score_right, (screen.get_width() * 3 / 4 - final_score_right.get_width() / 2, screen.get_height() / 2))

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            pygame.display.update()

    pygame.display.update()
