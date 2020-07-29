import pygame


pygame.font.init()
win_height, win_length = 600, 1100  # Window size parameters
screen = pygame.display.set_mode((win_length, win_height))  # Creating a window
pygame.display.set_icon(pygame.image.load("images/game_icon.png"))  # Set window icon image
pygame.display.set_caption("Space Battle", "Spine Runtime")  # Set window caption
close = False
start_img = pygame.image.load("images/startimg.jpg")
how_to_img = pygame.image.load("images/how_to.jpg")

button = pygame.image.load("images/button.png")
button_x = win_length / 2 - button.get_width() / 2      # Position of the buttons in the middle
button_y = 350
space_between = 60      # The space between the buttons

start_button = button.get_rect()        # Setting the start button
start_button.move_ip(button_x, button_y)

dual_button = button.get_rect()     # Setting the One vs One button
dual_button.move_ip(button_x, button_y + space_between)

how_to_button = button.get_rect()     # Setting the How- To button
how_to_button.move_ip(button_x, button_y + space_between * 2)

exit_button = button.get_rect()     # Setting the Exit button
exit_button.move_ip(button_x, button_y + space_between * 3)

back_button = pygame.Rect((20, win_height - 70), (60, 50))     # Setting the How- To button

clock = pygame.time.Clock()

while not close:  # Opening screen loop
    clicked = False
    screen.blit(start_img, (0, 0))
    font = pygame.font.Font(None, 40)  # Version text
    text_version = font.render("SpaceBattle v.1.8 Beta", 1, (255, 255, 255))
    screen.blit(text_version, (0, win_height - 30))
    event = pygame.event.poll()
    if event.type == pygame.QUIT:  # Exit question
        close = True
    if event.type == pygame.MOUSEBUTTONDOWN:        # Check if mouse was clicked
        if start_button.collidepoint(pygame.mouse.get_pos()):       # Check which button was clicked
            import solo_mode        # Importing the solo mode game
            close = True
        if dual_button.collidepoint(pygame.mouse.get_pos()):
            import oneonone     # Importing the One Vs One mode game
            close = True
        if how_to_button.collidepoint(pygame.mouse.get_pos()):
            while not clicked and not close:        # How to play screen
                clock.tick(60)
                screen.blit(how_to_img, (0, 0))
                event = pygame.event.poll()
                if event.type == pygame.QUIT:  # Exit question
                    clicked = True
                    close = True
                if event.type == pygame.MOUSEBUTTONDOWN:  # Check if Back button was clicked
                    if back_button.collidepoint(pygame.mouse.get_pos()):
                        clicked = True
                pygame.display.update()  # Updating the display
        if exit_button.collidepoint(pygame.mouse.get_pos()):
            close = True
    screen.blit(button, (button_x, button_y))       # Drawing the buttons on the screen
    screen.blit(button, (button_x, button_y + space_between))
    screen.blit(button, (button_x, button_y + space_between * 2))
    screen.blit(button, (button_x, button_y + space_between * 3))
    text_button = font.render("Start", 1, (0, 0, 0))
    screen.blit(text_button, (button_x + 75, button_y + 6))
    text_button = font.render("One Vs One", 1, (0, 0, 0))
    screen.blit(text_button, (button_x + 30, button_y + space_between + 6))
    text_button = font.render("How To Play", 1, (0, 0, 0))
    screen.blit(text_button, (button_x + 25, button_y + space_between * 2 + 6))
    text_button = font.render("Exit", 1, (0, 0, 0))
    screen.blit(text_button, (button_x + 80, button_y + space_between * 3 + 6))
    pygame.display.update()  # Updating the display

