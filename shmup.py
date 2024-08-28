import pygame
import random

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 450
FPS = 60

# Color palette
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initializing game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shmup')
clock = pygame.time.Clock()

# Sprite Groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Classes and functions
font_name = pygame.font.match_font('Arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    print("New mob created")  # Debugging print

def draw_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (50, 38))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 0
        self.shield = 100

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        if keys[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = random.choice(meteor_images)
        self.image = self.orig_image.copy()
        self.rect = self.orig_image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 8)
        self.speedx = random.randint(-3, 3)
        self.rot = 0
        self.rot_speed = random.randint(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot_speed + self.rot) % 360
            new_image = pygame.transform.rotate(self.orig_image, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.y > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 8)
            self.speedx = random.randint(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_image, (30, 18))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Load images
player_image = pygame.image.load('playerShip1_blue.png').convert_alpha()
enemy_image = pygame.image.load('enemyGreen1.png').convert_alpha()
meteor_image = pygame.image.load('meteorBrown_big2.png')
laser_image = pygame.image.load('laserGreen12.png').convert_alpha()

meteor_images = []
meteor_list = ['meteorBrown_big2.png', 'meteorBrown_big3.png', 'meteorBrown_big4.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
               'meteorBrown_tiny2.png', 'meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_big3.png',
               'meteorGrey_big4.png', 'meteorGrey_med1.png', 'meteorGrey_med2.png', 'meteorGrey_small1.png',
               'meteorGrey_big1.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(img))

# Load sound
shoot = pygame.mixer.Sound('burst fire.mp3')
pygame.mixer.music.load('space (1).mp3')
pygame.mixer.music.set_volume(0.5)
sounds = []
for sound in ['explosion01.wav', 'explosion02.wav', 'explosion04.wav']:
    sounds.append(pygame.mixer.Sound(sound))

score = 0
pygame.mixer.music.play(loops=-1)

# Create sprites
ship = Spaceship()
all_sprites.add(ship)

for i in range(8):
    newmob()

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.spritecollide(ship, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        ship.shield -= 30
        if ship.shield <= 0:
            running = False

    hits = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for hit in hits:
        score += 1
        random.choice(sounds).play()
        newmob()

    # Draw/render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, SCREEN_WIDTH / 2, 10)
    draw_bar(screen, 5, 5, ship.shield)

    pygame.display.flip()

pygame.quit()
