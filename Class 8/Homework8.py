import pygame
import random


def text_object(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def message_display(text, w = 0.5, h = 0.5):
    global show_message
    if not show_message:
        return
    largeText = pygame.font.SysFont('times', 100)
    text_surf, text_rect = text_object(text, largeText)
    text_rect.center = (display_width * w, display_height * h)

    screen.blit(text_surf, text_rect)
    show_message = False


def check_collision(player, obstacle):
    if not isinstance(player, Sprite):
        raise ValueError("Cannot use check collision with non sprites for player")
    if not isinstance(obstacle, Sprite):
        raise ValueError("Cannot use check collision with non sprites for obstacle")

    squared_summed_radii = (player.radius + obstacle.radius) ** 2
    distance = (player.x - obstacle.x) ** 2 + (player.y - obstacle.y) ** 2

    if squared_summed_radii >= distance:
        return True
    else:
        return False


class Sprite:
    """ A sprite object """
    x = 0
    y = 0
    radius = 1
    img = ""

    def __init__(self, x, y, radius, img):
        self.x = x
        self.y = y
        self.radius = radius
        self.img = pygame.image.load(img)

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))


enemies = 0


class Enemy(Sprite):
    def __init__(self, x, y, radius, img):
        global enemies
        self.x = x
        self.y = y
        self.radius = radius
        self.img = pygame.image.load(img)
        enemies += 1

    show = True
    dead = 0

    def update(self):
        global enemies
        if self.show:
            self.render(screen)
        if self.dead == 0 and self.show is False:
            enemies -= 1
            self.dead = 1


class Player(Sprite):
    direction = 'down'
    bullet_direction = 'down'

    def shoot(self):
        blast = pygame.mixer.Sound('blast.wav')
        blast.play()
        self.bullet_direction = self.direction
        bullet_sprite.x = player_sprite.x
        bullet_sprite.y = player_sprite.y

    def update(self):
        if self.direction == 'down':
            self.img = pygame.image.load("interceptor_down.png")
        elif self.direction == 'up':
            self.img = pygame.image.load("interceptor_up.png")
        elif self.direction == 'right':
            self.img = pygame.image.load("interceptor_right.png")
        elif self.direction == 'left':
            self.img = pygame.image.load("interceptor_left.png")


# the game
pygame.init()

display_width = 800
display_height = 600

screen = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("My Simple Pygame")

blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
space = pygame.image.load("space.jpg")

y = display_height * 0.5
x = display_width * 0.5

otherx = 50
othery = 100

player_sprite = Player(x, y, 16, 'interceptor_down.png')
bullet_sprite = Sprite(-50, -50, 16, 'bullet.png')


enemy1 = Enemy(random.randint(1, display_width), random.randint(1, display_height), 16, 'qmark.png')
enemy2 = Enemy(random.randint(1, display_width), random.randint(1, display_height), 16, 'qmark.png')
enemy3 = Enemy(random.randint(1, display_width), random.randint(1, display_height), 16, 'qmark.png')
enemy4 = Enemy(random.randint(1, display_width), random.randint(1, display_height), 16, 'qmark.png')
enemy5 = Enemy(random.randint(1, display_width), random.randint(1, display_height), 16, 'qmark.png')

enemies_group = enemy1, enemy2, enemy3, enemy4, enemy5

is_running = True

clock = pygame.time.Clock()

show_message = True
pygame.mixer.music.load('spark_man.wav')
pygame.mixer.music.play(-1)
# the game is running
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # input
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        is_running = False

    if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
        player_sprite.y += 5
        player_sprite.direction = 'down'
    elif pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
        player_sprite.y -= 5
        player_sprite.direction = 'up'

    if pressed_keys[pygame.K_RIGHT]:
        player_sprite.x += 5
        player_sprite.direction = 'right'
    elif pressed_keys[pygame.K_LEFT]:
        player_sprite.x -= 5
        player_sprite.direction = 'left'

    if player_sprite.bullet_direction == 'down':
        bullet_sprite.y += 10
    elif player_sprite.bullet_direction == 'up':
        bullet_sprite.y -= 10
    elif player_sprite.bullet_direction == 'right':
        bullet_sprite.x += 10
    elif player_sprite.bullet_direction == 'left':
        bullet_sprite.x -= 10

    player_sprite.update()

    if pressed_keys[pygame.K_SPACE]:
        player_sprite.shoot()

    # bounds
    player_sprite.x = max(player_sprite.x, 0)
    player_sprite.x = min(player_sprite.x, display_width - (player_sprite.radius * 2))
    player_sprite.y = max(player_sprite.y, 0)
    player_sprite.y = min(player_sprite.y, display_height - (player_sprite.radius * 2))

    for k in range(5):
        if check_collision(bullet_sprite, enemies_group[k]):
            enemies_group[k].show = False

    screen.fill(black)
    screen.blit(space, (0, 0))
    bullet_sprite.render(screen)
    player_sprite.render(screen)
    enemy1.update()
    enemy2.update()
    enemy3.update()
    enemy4.update()
    enemy5.update()
    print(enemies)
    if enemies == 0:
        message_display("Winner!")
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
