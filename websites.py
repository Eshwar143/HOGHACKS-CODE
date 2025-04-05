import pygame
import sys
import time
from Roulette import Roulette
from SlotMachine import SlotMachine

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starving Kids in Los Angeles")
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A 404NotFound HogHacks Parody Charity")

# Colors
SKY_BLUE = (135, 206, 235)  # Sky blue background
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (52, 152, 219)  # Nice blue for buttons
BUTTON_HOVER = (41, 128, 185)  # Darker blue for hover
BUTTON_DISABLED = (189, 195, 199)  # Gray for disabled buttons
TEXT_COLOR = (44, 62, 80)  # Dark blue-gray for text
INPUT_BG = (236, 240, 241)  # Light gray for input field

# Fonts
title_font = pygame.font.SysFont('Times New Roman', 48, bold=True)
button_font = pygame.font.SysFont('Times New Roman', 32)
input_font = pygame.font.SysFont('Times New Roman', 24)

# Button dimensions
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 60
BUTTON_SPACING = 30
BUTTON_RADIUS = 10  # For rounded corners

# Create button rectangles
take_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH - BUTTON_SPACING//2, HEIGHT - 120, BUTTON_WIDTH, BUTTON_HEIGHT)
donate_button = pygame.Rect(WIDTH//2 + BUTTON_SPACING//2, HEIGHT - 120, BUTTON_WIDTH, BUTTON_HEIGHT)
roulette_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
slot_machine_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 160, 200, 50)

# Input field
input_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50)
input_text = ""
input_active = False
donation_mode = False
take_mode = False
thank_you = False
game_message = False
roulette_mode = False
slot_machine_mode = False
original_amount = 0
current_amount = 0
game_result = None
lose_message = False
has_played = False
lose_timer = None

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def reset_game():
    global input_text, input_active, donation_mode, take_mode, thank_you, game_message
    global roulette_mode, slot_machine_mode, original_amount, current_amount, game_result, lose_message, has_played, lose_timer
    input_text = ""
    input_active = False
    donation_mode = False
    take_mode = False
    thank_you = False
    game_message = False
    roulette_mode = False
    slot_machine_mode = False
    original_amount = 0
    current_amount = 0
    game_result = None
    lose_message = False
    has_played = False
    lose_timer = None

# Create games
roulette = Roulette(screen)
slot_machine = SlotMachine(screen)
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    dt = clock.tick(60)

    # Check if we need to reset after losing
    if lose_timer is not None and time.time() - lose_timer >= 5:
        reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if take_button.collidepoint(event.pos) and not has_played:
                take_mode = True
                donation_mode = False
                thank_you = False
                game_message = False
                roulette_mode = False
                slot_machine_mode = False
                game_result = None
                lose_message = False
            elif donate_button.collidepoint(event.pos):
                donation_mode = True
                take_mode = False
                thank_you = False
                game_message = False
                roulette_mode = False
                slot_machine_mode = False
                game_result = None
                lose_message = False
            elif roulette_button.collidepoint(event.pos) and game_message and not has_played:
                roulette_mode = True
            elif slot_machine_button.collidepoint(event.pos) and game_message and not has_played:
                slot_machine_mode = True
            elif input_rect.collidepoint(event.pos):
                pass
            else:
                donation_mode = False
                take_mode = False
        elif event.type == pygame.KEYDOWN and (donation_mode or take_mode):
            if event.key == pygame.K_RETURN:
                try:
                    amount = float(input_text)
                    if take_mode and amount > 500:
                        input_text = "Please choose an amount equal to or below $500"
                    else:
                        if take_mode:
                            original_amount = amount
                            current_amount = amount
                            game_message = True
                            donation_mode = False
                            take_mode = False
                        else:
                            thank_you = True
                            donation_mode = False
                        input_text = ""
                except ValueError:
                    pass
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.unicode.isdigit() or event.unicode == '.':
                input_text += event.unicode
        elif roulette_mode:
            roulette.handle_event(event)
            result = roulette.get_result()
            if result is not None and game_result is None:
                game_result = result
                has_played = True
                if "You won!" in roulette.message:
                    thank_you = True
                    game_message = False
                    roulette_mode = False
                else:
                    current_amount = original_amount * 2
                    donation_mode = True
                    game_message = False
                    roulette_mode = False
                    lose_message = True
                    lose_timer = time.time()
        elif slot_machine_mode:
            slot_machine.handle_event(event)
            result = slot_machine.get_result()
            if result is not None and game_result is None:
                game_result = result
                has_played = True
                if "JACKPOT!" in slot_machine.message:
                    thank_you = True
                    game_message = False
                    slot_machine_mode = False
                else:
                    current_amount = original_amount * 2
                    donation_mode = True
                    game_message = False
                    slot_machine_mode = False
                    lose_message = True
                    lose_timer = time.time()

    # Fill the screen with sky blue
    screen.fill(SKY_BLUE)

    if not (roulette_mode or slot_machine_mode):
        # Draw title at the top with shadow
        title = title_font.render("Starving Kids in Los Angeles", True, TEXT_COLOR)
        title_shadow = title_font.render("Starving Kids in Los Angeles", True, (0, 0, 0, 128))
        screen.blit(title_shadow, (WIDTH//2 - title.get_width()//2 + 2, 52))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        # Draw buttons with rounded corners
        # Take button
        button_color = BUTTON_DISABLED if has_played else BUTTON_COLOR
        draw_rounded_rect(screen, button_color, take_button, BUTTON_RADIUS)
        take_text = button_font.render("Take", True, WHITE)
        screen.blit(take_text, (take_button.centerx - take_text.get_width()//2, 
                               take_button.centery - take_text.get_height()//2))

        # Donate button
        draw_rounded_rect(screen, BUTTON_COLOR, donate_button, BUTTON_RADIUS)
        donate_text = button_font.render("Donate", True, WHITE)
        screen.blit(donate_text, (donate_button.centerx - donate_text.get_width()//2, 
                                 donate_button.centery - donate_text.get_height()//2))

        # Draw input field if in donation mode
        if donation_mode:
            # Draw prompt
            if lose_message:
                prompt = input_font.render(f"You lost! You must donate ${current_amount} now:", True, TEXT_COLOR)
            else:
                prompt = input_font.render("Enter donation amount ($):", True, TEXT_COLOR)
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 80))
            
            # Draw input box with rounded corners
            draw_rounded_rect(screen, INPUT_BG, input_rect, 5)
            text_surface = input_font.render(str(current_amount), True, TEXT_COLOR)
            screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        # Take input
        if take_mode:
            prompt = input_font.render("Enter amount to take (Max $500):", True, TEXT_COLOR)
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 80))
            draw_rounded_rect(screen, INPUT_BG, input_rect, 5)
            text_surface = input_font.render(input_text, True, TEXT_COLOR)
            screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        # Thank you message
        if thank_you:
            if game_result is not None and ("You won!" in roulette.message or "JACKPOT!" in slot_machine.message):
                thanks = title_font.render(f"Congratulations! You won ${original_amount}!", True, TEXT_COLOR)
            else:
                thanks = title_font.render("Thank you for your donation!", True, TEXT_COLOR)
            screen.blit(thanks, (WIDTH//2 - thanks.get_width()//2, HEIGHT//2))

        # Game message
        if game_message and not has_played:
            game_text = title_font.render("You must win a game of chance!", True, TEXT_COLOR)
            screen.blit(game_text, (WIDTH//2 - game_text.get_width()//2, HEIGHT//2 - 50))
            
            # Roulette button
            draw_rounded_rect(screen, BUTTON_COLOR, roulette_button, BUTTON_RADIUS)
            roulette_text = button_font.render("Play Roulette", True, WHITE)
            screen.blit(roulette_text, (roulette_button.centerx - roulette_text.get_width()//2, 
                                      roulette_button.centery - roulette_text.get_height()//2))

            # Slot Machine button
            draw_rounded_rect(screen, BUTTON_COLOR, slot_machine_button, BUTTON_RADIUS)
            slot_text = button_font.render("Play Slots", True, WHITE)
            screen.blit(slot_text, (slot_machine_button.centerx - slot_text.get_width()//2, 
                                  slot_machine_button.centery - slot_text.get_height()//2))
    else:
        if roulette_mode:
            roulette.update(dt)
            roulette.draw()
        elif slot_machine_mode:
            slot_machine.update(dt)
            slot_machine.draw()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
