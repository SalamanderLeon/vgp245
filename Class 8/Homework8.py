import pygame
import random


def text_object(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


class Message:

    def __init__(self, show=False):
        self.show_message = show

    def message_display(self, text, w=0.5, h=0.5):
        #if not self.show_message:
        #    return
        largeText = pygame.font.SysFont('times', 100)
        text_surf, text_rect = text_object(text, largeText)
        text_rect.center = (display_width * w, display_height * h)

        screen.blit(text_surf, text_rect)
        #self.show_message = False


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
        self.alive = True
        enemies += 1

    def update(self, screen):
        if self.alive:
            self.render(screen)

    def killed(self):
        global enemies
        enemies -= 1
        self.alive = False
        print('enemy killed')

class Player(Sprite):
    direction = 'down'
    bullet_direction = 'down'

    def __init__(self, x, y, radius):
        self.left_img = pygame.image.load("interceptor_left.png")
        self.right_img = pygame.image.load("interceptor_right.png")
        self.up_img = pygame.image.load("interceptor_up.png")
        self.down_img = pygame.image.load("interceptor_down.png")
        super().__init__(x, y, radius, "interceptor_down.png")

    def shoot(self):
        blast = pygame.mixer.Sound('blast.wav')
        blast.play()
        self.bullet_direction = self.direction
        bullet_sprite.x = player_sprite.x
        bullet_sprite.y = player_sprite.y

    def update(self):
        if self.direction == 'down':
            self.img = self.down_img
        elif self.direction == 'up':
            self.img = self.up_img
        elif self.direction == 'right':
            self.img = self.right_img
        elif self.direction == 'left':
            self.img = self.left_img

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

player_sprite = Player(x, y, 16)
bullet_sprite = Sprite(-50, -50, 16, 'bullet.png')

enemy_count = 1000

enemies_group = []
for i in range(enemy_count):
    enemies_group.append(Enemy(random.randint(1, display_width - 16), random.randint(1, display_height - 16), 16, 'qmark.png'))

#win = Message(False)
#win.message_display("WINNER!\nPRESS ESC TO EXIT")
counter = Message(True)

is_running = True

clock = pygame.time.Clock()

#show_message = True
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

    screen.fill(black)
    screen.blit(space, (0, 0))

    for enemy in enemies_group:
        enemy.update(screen)
        if enemy.alive and check_collision(bullet_sprite, enemy):
            print('got hit')
            enemy.killed()

    bullet_sprite.render(screen)
    player_sprite.render(screen)

    counter.message_display(str(enemies), 0.9, 0.1)

    if enemies == 0:
        win = Message(False)
        win.message_display("WINNER!", 0.5, 0.3)
        win.message_display("PRESS ESC", 0.5, 0.6)
        win.message_display("TO EXIT", 0.5, 0.75)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
