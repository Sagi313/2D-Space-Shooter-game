import pygame
import random


class Player1(pygame.sprite.Sprite):  # Creating the hero character class

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.life = 2
        self.image = pygame.image.load("images/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.y = win_height - 150
        self.rect.x = win_length / 2 + 100

    def movement(self):  # Key arguments movement function
        press = pygame.key.get_pressed()
        if press[pygame.K_RIGHT] and self.rect.x < win_length - self.image.get_width():
            self.rect.x += 4
        if press[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 4

    def hit(self):
        self.life -= 1

    def add_life(self):
        self.life += 1

    def life_left(self):
        return self.life

    def current_place(self):
        return self.rect.x


class Player2(pygame.sprite.Sprite):  # Creating the hero character class

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.life = 2
        self.image = pygame.image.load("images/player_2.png")
        self.rect = self.image.get_rect()
        self.rect.y = win_height - 150
        self.rect.x = win_length / 2 - 100

    def movement(self):  # Key arguments movement function
        press = pygame.key.get_pressed()
        if press[pygame.K_d] and self.rect.x < win_length - self.image.get_width():
            self.rect.x += 4
        if press[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= 4

    def hit(self):
        self.life -= 1

    def add_life(self):
        self.life += 1

    def life_left(self):
        return self.life

    def current_place(self):
        return self.rect.x


class EnemyCharacter(pygame.sprite.Sprite):  # Creating the enemy character class

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.life = 1
        self.min_speed = 2
        self.max_speed = 7
        self.speed = self.min_speed
        image_number = random.randrange(0, 3)
        if image_number == 0:
            self.image = pygame.image.load("images/asteroid1.png")
        if image_number == 1:
            self.image = pygame.image.load("images/asteroid2.png")
        if image_number == 2:
            self.image = pygame.image.load("images/asteroid3.png")
        self.rect = self.image.get_rect()
        self.rect.y = win_height

    def movement(self):  # Automatic movement function
        if self.rect.y <= win_height:
            self.rect.y += self.speed
        else:
            self.rect.y = -(self.image.get_height())
            self.rect.x = random.randrange(0, win_length - self.image.get_width())
            self.speed = random.randrange(self.min_speed, self.max_speed)

    def hit(self):
        self.rect.y = -(self.image.get_height())
        self.rect.x = random.randrange(0, win_length - self.image.get_width())

    def speed_upgrade(self):
        self.min_speed += 1
        self.max_speed += 1


class Hearts(pygame.sprite.Sprite):  # Creating a heart sprite (+1 life)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/heart.png")
        self.rect = self.image.get_rect()
        self.rect.y = win_height
        self.rect.x = random.randrange(0, win_length - self.image.get_width())

    def movement(self):  # Moving the heart
        if self.rect.y < win_height:
            self.rect.y += 3
        else:
            if random.randrange(1, 1000) == 2:  # The odds of getting a heart
                self.rect.y = -(self.image.get_height())
                self.rect.x = random.randrange(0, win_length - self.image.get_width())

    def caught(self):
        self.rect.y = win_height
        self.rect.x = random.randrange(0, win_length - self.image.get_width())


class LaserBean1(Player1, pygame.sprite.Sprite):       # Creating a laser bean sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/space_missiles.png")
        self.rect = self.image.get_rect()
        self.rect.y = win_height
        self.rect.x = ship1.current_place()
        self.keep_moving = False

    def shooting(self):     # Movement function with a key argument
        press = pygame.key.get_pressed()
        if press[pygame.K_SPACE] and not self.keep_moving:
            self.rect.x = ship1.current_place() + ship1.image.get_width() / 2 - self.image.get_width() / 2
            self.rect.y = win_height - ship1.image.get_height()
            self.keep_moving = True
        if self.keep_moving is True:
            if self.rect.y > -(self.image.get_height()):
                self.rect.y -= 6
            else:
                self.rect.y = win_height
                self.keep_moving = False


class LaserBean2(Player2, pygame.sprite.Sprite):       # Creating a laser bean sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/space_missiles.png")
        self.rect = self.image.get_rect()
        self.rect.y = win_height
        self.rect.x = ship2.current_place()
        self.keep_moving = False

    def shooting(self):     # Movement function with a key argument
        press = pygame.key.get_pressed()
        if press[pygame.K_w] and not self.keep_moving:
            self.rect.x = ship2.current_place() + ship2.image.get_width() / 2 - self.image.get_width() / 2
            self.rect.y = win_height - ship2.image.get_height()
            self.keep_moving = True
        if self.keep_moving is True:
            if self.rect.y > -(self.image.get_height()):
                self.rect.y -= 6
            else:
                self.rect.y = win_height
                self.keep_moving = False


def records_data(record):       # Gets the record into the text database
    record_file = open('record', 'r')
    current_record = float(record_file.read())
    if current_record < record:
        record_file = open('record', 'w')
        record_file.write(str(record))
    record_file = open('record', 'r')
    return int(float(record_file.read()))


pygame.font.init()
win_height, win_length = 600, 1100  # Window size parameters
screen = pygame.display.set_mode((win_length, win_height))  # Creating a window
pygame.display.set_icon(pygame.image.load("images/game_icon.png"))  # Set window icon image
pygame.display.set_caption("SpaceGame", "Spine Runtime")  # Set window caption
close = False
gameover_img = pygame.image.load("images/game_over_dual.jpg")
button = pygame.image.load("images/button.png")
background_img = pygame.image.load("images/background.jpg")
dual_life_img = pygame.image.load("images/dual_life.png")

ship1 = Player1()
ship2 = Player2()
life = Hearts()
laser1 = LaserBean1()
laser2 = LaserBean2()
all_sprites = pygame.sprite.Group()  # Creating a sprites groups
all_sprites.add(laser1, laser2, ship1, ship2, life)
rocks_group = pygame.sprite.Group()
for i in range(0, 5):  # Loop that fills the group with sprites
    rock = EnemyCharacter()
    rocks_group.add(rock)
level_up = 0
score = 0

button_x = win_length / 2 - button.get_width() / 2      # Position of the buttons in the middle
button_y = 450
space_between = 60      # The space between the buttons

start_over_button = button.get_rect()        # Setting the Start Over button
start_over_button.move_ip(button_x, button_y)

exit_button = button.get_rect()     # Setting the Exit button
exit_button.move_ip(button_x, button_y + space_between)

while not close:  # Main infinite loop
    image_y = -(background_img.get_height()) + win_height
    event = pygame.event.poll()
    if event.type == pygame.QUIT:  # Exit question
        close = True
    clock = pygame.time.Clock()
    while ship1.life_left() >= 0 and ship2.life_left() >= 0 and not close:  # Actual game loop
        event = pygame.event.poll()
        if event.type == pygame.QUIT:  # Exit question
            close = True
        screen.blit(background_img, (0, image_y))  # Placing the background image
        image_y += 0.8
        if image_y > 0:
            image_y = -(background_img.get_height()) + win_height
        ship1.movement()     # Moving all the sprites
        ship2.movement()
        life.movement()
        laser1.shooting()
        laser2.shooting()
        score += 0.04
        level_up += 0.5
        for EnemyCharacter in rocks_group.sprites():  # Use "movement" function on each sprite
            EnemyCharacter.movement()
            if pygame.sprite.collide_mask(ship1, EnemyCharacter):  # Check for collusion (a hit)
                ship1.hit()
                EnemyCharacter.hit()
            if pygame.sprite.collide_mask(laser1, EnemyCharacter):
                EnemyCharacter.hit()
            if pygame.sprite.collide_mask(ship2, EnemyCharacter):  # Check for collusion (a hit)
                ship2.hit()
                EnemyCharacter.hit()
            if pygame.sprite.collide_mask(laser2, EnemyCharacter):
                EnemyCharacter.hit()
            if level_up % 1000 == 0:
                EnemyCharacter.speed_upgrade()
        if pygame.sprite.collide_mask(ship1, life):  # Check for earning a life
            ship1.add_life()
            life.caught()
        if pygame.sprite.collide_mask(ship2, life):  # Check for earning a life
            ship2.add_life()
            life.caught()
        screen.blit(dual_life_img, (10, 10))
        font = pygame.font.Font(None, 48)  # Printing the life and score text on the screen
        p1_life = font.render(str(ship1.life_left()), 1, (255, 255, 255))
        p2_life = font.render(str(ship2.life_left()), 1, (255, 255, 255))
        screen.blit(p1_life, (80, 21))
        screen.blit(p2_life, (80, 82))

        rocks_group.draw(screen)  # Drawing the sprites on the surface
        all_sprites.draw(screen)
        pygame.display.update()  # Refreshing display
        clock.tick(60)  # 60 FPS timer
    screen.blit(gameover_img, (0, 0))
    font = pygame.font.Font(None, 70)
    if ship1.life_left() > ship2.life_left():
        screen.blit(ship1.image, (230, 250))
    else:
        screen.blit(ship2.image, (230, 250))
    winner_text = font.render("= Has Won The Match!", 1, (255, 255, 255))
    screen.blit(winner_text, (360, 300))
    screen.blit(button, (button_x, button_y))
    screen.blit(button, (button_x, button_y + space_between))
    font = pygame.font.Font(None, 40)
    text_button = font.render("Start Over", 1, (0, 0, 0))
    screen.blit(text_button, (button_x + 45, button_y + 6))
    text_button = font.render("Exit", 1, (0, 0, 0))
    screen.blit(text_button, (button_x + 85, button_y + space_between + 6))
    if event.type == pygame.MOUSEBUTTONDOWN:        # Check if mouse was clicked
        if start_over_button.collidepoint(pygame.mouse.get_pos()):       # Check which button was clicked
            score = 0
            ship1.__init__()
            ship2.__init__()
            life.__init__()
            for EnemyCharacter in rocks_group.sprites():
                EnemyCharacter.__init__()
        if exit_button.collidepoint(pygame.mouse.get_pos()):
            close = True
    pygame.display.update()
