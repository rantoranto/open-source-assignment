import pygame, sys, math, random, time
from pygame.locals import *

pygame.init()
pygame.display.set_caption("20256562 김권택")
s = pygame.display.set_mode((1000, 600))
c = pygame.time.Clock()
b = pygame.image.load("C:/Users/ball.png").convert_alpha()
b = pygame.transform.scale(b, (45, 45))

rs = 0
ls = 0
f1 = pygame.font.Font(None, 40)
f2 = pygame.font.SysFont("corbel", 70)
f3 = pygame.font.Font(None, 60)
t0 = time.time()

class P:
    def __init__(self, k, x, d):
        self.k = k
        self.x = x
        self.y = 260
        self.d = d
        self.t = 0

    def u(self):
        if k[self.k[0]] and self.y > 0:
            self.y -= 10
        if k[self.k[1]] and self.y < 520:
            self.y += 10

    def r(self):
        o = -self.d * (time.time() < self.t + 0.5) * 10
        pygame.draw.line(s, (255, 255, 255), (self.x, self.y), (self.x + o, self.y + 80), 6)

    def sm(self):
        if time.time() > self.t + 0.3:
            self.t = time.time()

class GB:
    def __init__(self):
        self.a = (math.pi / 3) * random.random() + (math.pi / 3) + math.pi * random.randint(0, 1)
        self.v = 12
        self.vx = math.sin(self.a) * self.v
        self.vy = math.cos(self.a) * self.v
        self.x = 475
        self.y = 275

    def u(self):
        self.x += self.vx
        self.y += self.vy

    def r(self):
        s.blit(b, (int(self.x), int(self.y)))

    def col(self):
        if (self.y <= 0 and self.vy < 0) or (self.y >= 550 and self.vy > 0):
            self.vy *= -1
            self.a = math.atan2(self.vx, self.vy)

        for p in ps:
            if pygame.Rect(p.x, p.y, 6, 80).colliderect(self.x, self.y, 50, 50) and abs(self.vx) / self.vx == p.d:
                self.a += random.random() * math.pi / 4 - math.pi / 8
                if (0 < self.a < math.pi / 6) or (math.pi * 5 / 6 < self.a < math.pi):
                    self.a = (math.pi / 3) * random.random() + (math.pi / 3)
                elif (math.pi < self.a < math.pi * 7 / 6) or (math.pi * 11 / 6 < self.a < math.pi * 2):
                    self.a = (math.pi / 3) * random.random() + (math.pi / 3) + math.pi

                self.a *= -1
                self.a %= math.pi * 2

                if time.time() < p.t + 0.05 and self.v < 20:
                    self.v *= 1.5

                self.vx = math.sin(self.a) * self.v
                self.vy = math.cos(self.a) * self.v

g = GB()
ps = [P([K_a, K_z], 10, -1), P([K_UP, K_DOWN], 984, 1)]

while True:
    c.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_q:
                ps[0].sm()
            if e.key == K_RSHIFT:
                ps[1].sm()

    k = pygame.key.get_pressed()
    s.fill((0, 0, 0))

    pygame.draw.line(s, (255, 255, 255), (s.get_width() / 2, 0), (s.get_width() / 2, s.get_height()), 3)
    pygame.draw.circle(s, (255, 255, 255), (int(s.get_width() / 2), int(s.get_height() / 2)), 50, 3)

    t = f1.render(str(int(60 - (time.time() - t0))), True, (255, 255, 255))
    s.blit(t, (s.get_width() / 2 - t.get_width() / 2, 20))

    for p in ps:
        p.u()
        p.r()

    if g.x < -50:
        g = GB()
        rs += 1

    if g.x > 1000:
        g = GB()
        ls += 1

    g.u()
    g.r()
    g.col()

    st1 = f1.render(str(ls), True, (255, 255, 255))
    s.blit(st1, (20, 20))
    st2 = f1.render(str(rs), True, (255, 255, 255))
    s.blit(st2, (980 - st2.get_width(), 20))

    if rs > 9 or ls > 9 or time.time() - t0 > 60:
        ttl = f2.render("score", True, (255, 0, 255))
        s.blit(ttl, (s.get_width() / 4 - ttl.get_width() / 2, s.get_height() / 4))
        s.blit(ttl, (s.get_width() * 3 / 4 - ttl.get_width() / 2, s.get_height() / 4))

        fsl = f3.render(str(ls), True, (255, 255, 255))
        s.blit(fsl, (s.get_width() / 4 - fsl.get_width() / 2, s.get_height() / 2))

        fsr = f3.render(str(rs), True, (255, 255, 255))
        s.blit(fsr, (s.get_width() * 3 / 4 - fsr.get_width() / 2, s.get_height() / 2))

        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
            pygame.display.update()

    pygame.display.update()
