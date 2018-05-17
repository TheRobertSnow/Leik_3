import pygame
import random
import time


WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
score = 0
shoot_ef = pygame.mixer.Sound('sounds/shoot.wav')
kill_ef = pygame.mixer.Sound('sounds/invaderkilled.wav')
die_ef = pygame.mixer.Sound('sounds/shipexplosion.wav')
enemy_explode = pygame.image.load('images/explosiongreen.png')
font_name = pygame.font.match_font('fonts/space_invaders.ttf')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()
        #self.radius = 23
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 15
        self.speed = 5
        self.shoot_delay = 300
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.x <= -50:
                self.rect.x = 800

        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.x >= 800:
                self.rect.x = -50

        if key[pygame.K_UP]:
            self.rect.y -= self.speed
            if self.rect.y <= -48:
                self.rect.y = 648

        if key[pygame.K_DOWN]:
            self.rect.y += self.speed
            if self.rect.y >= 648:
                self.rect.y = -48

        if key[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            shoot_ef.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy3_2.png")
        self.image = pygame.transform.scale(self.image, (52, 38))
        self.rect = self.image.get_rect()
        #self.radius = 23
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(- 100, -40)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(- 100, -40)
            self.speedy = random.randrange(1, 4)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/laser.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Explotion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = enemy_explode
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()



all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
mob_amount = 8

for i in range(mob_amount):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # check for bullet mob collision
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hits in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        score += 10
        kill_ef.play()

    # check for player mob collision
    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        die_ef.play()
        time.sleep(0.5)
        running = False

    # Draw/Render
    screen.fill(BLACK)
    background = Background('images/background.jpg', [0, 0])
    screen.blit(background.image, background.rect)
    if score == 1000:
        text = "You Win!"
        draw_text(screen, str(text), 70, (WIDTH / 2), (HEIGHT / 2))
        time.sleep(3)
        running = False
    all_sprites.draw(screen)
    draw_text(screen, str(score), 50, (WIDTH / 2), 18)

    pygame.display.flip()

pygame.quit()