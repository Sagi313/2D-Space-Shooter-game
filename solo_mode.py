import pygame
import random


class HeroCharacter(pygame.sprite.Sprite):  # Creating the hero character class

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.life = 2
        self.image = pygame.image.load("images/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.y = win_height - 150
        self.rect.x = win_length / 2

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


class LaserBean(HeroCharacter, pygame.sprite.Sprite):       # Creating a laser bean sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/space_missiles.png")
        self.rect = self.image.get_rect()
        self.rect.y = win_height
        self.rect.x = ship.current_place()
        self.keep_moving = False

    def shooting(self):     # Movement function with a key argument
        press = pygame.key.get_pressed()
        if press[pygame.K_SPACE] and not self.keep_moving:
            self.rect.x = ship.current_place() + ship.image.get_width() / 2 - self.image.get_width() / 2
            self.rect.y = win_height - ship.image.get_height()
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
pygame.display.set_caption("Space Battle", "Spine Runtime")  # Set window caption
close = False
gameover_img = pygame.image.load("images/gameover.jpg")
button = pygame.image.load("images/button.png")
background_img = pygame.image.load("images/background.jpg")
score_life_img = pygame.image.load("images/score_life.png")

ship = HeroCharacter()
life = Hearts()
laser = LaserBean()
all_sprites = pygame.sprite.Group()  # Creating a sprites groups
all_sprites.add(ship, laser, life)
rocks_group = pygame.sprite.Group()
for i in range(0, 10):  # Loop that fills the group with sprites
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
    while ship.life_left() >= 0 and not close:  # Actual game loop
        event = pygame.event.poll()
        if event.type == pygame.QUIT:  # Exit question
            close = True
        screen.blit(background_img, (0, image_y))  # Placing the background image
        image_y += 1.8
        if image_y > 0:
            image_y = -(background_img.get_height()) + win_height
        ship.movement()     # Moving all the sprites
        life.movement()
        laser.shooting()
        score += 0.05
        level_up += 0.5
        for EnemyCharacter in rocks_group.sprites():  # Use "movement" function on each sprite
            EnemyCharacter.movement()
            if pygame.sprite.collide_mask(ship, EnemyCharacter):  # Check for collusion (a hit)
                ship.hit()
                EnemyCharacter.hit()
            if pygame.sprite.collide_mask(laser, EnemyCharacter):       # Check for collusion (laser hit rock)
                EnemyCharacter.hit()
            if level_up % 1000 == 0:
                EnemyCharacter.speed_upgrade()
        if pygame.sprite.collide_mask(ship, life):  # Check for earning a life
            ship.add_life()
            life.caught()
        screen.blit(score_life_img, (10, 10))
        font = pygame.font.Font(None, 48)  # Printing the life and score text on the screen
        text_life = font.render(str(ship.life_left()), 1, (255, 255, 255))
        text_score = font.render(str(int(score)), 1, (255, 255, 255))
        screen.blit(text_life, (80, 21))
        screen.blit(text_score, (80, 82))

        rocks_group.draw(screen)  # Drawing the sprites on the surface
        all_sprites.draw(screen)
        pygame.display.update()  # Refreshing display
        clock.tick(60)  # 60 FPS timer
    screen.blit(gameover_img, (0, 0))
    font = pygame.font.Font(None, 70)
    final_score_text = font.render("= " + str(int(score)), 1, (255, 255, 255))
    best_record_text = font.render("Current Record- " + str(records_data(score)), 1, (255, 255, 255))
    screen.blit(final_score_text, (520, 270))
    screen.blit(best_record_text, (340, 340))
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
            ship.__init__()
            life.__init__()
            for EnemyCharacter in rocks_group.sprites():
                EnemyCharacter.__init__()
        if exit_button.collidepoint(pygame.mouse.get_pos()):
            close = True
    pygame.display.update()
