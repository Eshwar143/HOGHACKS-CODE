import pygame
import sys
from Roulette import Roulette
from SlotMachine import SlotMachine
class Rehab:

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

    
    def draw(self):
        title_font = pygame.font.SysFont('Times New Roman', 48, bold=True)
        message_font = pygame.font.SysFont('Times New Roman', 36, bold=True)

        title = title_font.render("REHAB REQUIRED", True, (255, 0, 0))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 200))
        
        message = message_font.render("You've taken money too many times. Time to reflect and meditate.", True, (70, 130, 180))
        self.screen.blit(message, (self.width//2 - message.get_width()//2, 300))
        
        continue_text = "Think about what you have done. You were wasting money instead of giving."
        continue_surface = message_font.render(continue_text, True, (70, 130, 180))
        self.screen.blit(continue_surface, (self.width//2 - continue_surface.get_width()//2, 400))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            return True  # Exit rehab mode
        return False


# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Charity and Chance")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Main color scheme
SKY_BLUE = (135, 206, 235)     # Main background
LIGHT_BLUE = (173, 216, 230)   # Secondary background
DEEP_BLUE = (0, 191, 255)      # Accent color
PALE_BLUE = (176, 224, 230)    # Input field
STEEL_BLUE = (70, 130, 180)    # Text color
GOLD = (255, 215, 0)           # Button color
DARK_GOLD = (184, 134, 11)     # Button hover

# Fonts
title_font = pygame.font.SysFont('Times New Roman', 48, bold=True)
button_font = pygame.font.SysFont('Times New Roman', 32, bold=True)
input_font = pygame.font.SysFont('Times New Roman', 24)
message_font = pygame.font.SysFont('Times New Roman', 36, bold=True)

# Button dimensions
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 60
BUTTON_SPACING = 30
BUTTON_RADIUS = 10  # For rounded corners

# Create button rectangles
take_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH - BUTTON_SPACING//2, HEIGHT - 120, BUTTON_WIDTH, BUTTON_HEIGHT)
donate_button = pygame.Rect(WIDTH//2 + BUTTON_SPACING//2, HEIGHT - 120, BUTTON_WIDTH, BUTTON_HEIGHT)
roulette_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH - BUTTON_SPACING//2, HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT)
slot_button = pygame.Rect(WIDTH//2 + BUTTON_SPACING//2, HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT)

# Input field
input_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50)
input_text = ""
input_active = False
donation_mode = False
take_mode = False
show_message = False
message = ""
message_timer = 0
game_selection_mode = False
current_game = None
amount_to_take = 0
take_count = 0  # Initialize take count
in_rehab = False

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if in_rehab:
                rehab = Rehab(screen, WIDTH, HEIGHT)
                rehab.draw()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if rehab.handle_event(event):
                        in_rehab = False  # Exit rehab mode
                        break  # Break the event loop to avoid multiple key presse
                
            if game_selection_mode:
                if roulette_button.collidepoint(event.pos):
                    current_game = Roulette(screen)
                    game_selection_mode = False
                elif slot_button.collidepoint(event.pos):
                    current_game = SlotMachine(screen)
                    game_selection_mode = False
            else:
                if take_button.collidepoint(event.pos):
                    take_mode = True
                    input_active = True
                    donation_mode = False
                    show_message = False
                    take_count += 1  # Increment take count
                elif donate_button.collidepoint(event.pos):
                    donation_mode = True
                    input_active = True
                    take_mode = False
                    show_message = False
                elif input_rect.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                if current_game:
                    if current_game.handle_event(event):
                        result = current_game.get_result()
                        if result is not None:
                            if result:
                                message = f"Congratulations! You won ${amount_to_take:.2f}!"
                                show_message = True
                                message_timer = 180
                                game_selection_mode = False
                                current_game = None
                            else:
                                donation_total = amount_to_take * 2
                                message = f"Sorry, you lost! You must donate ${donation_total:.2f}."
                                show_message = True
                                message_timer = 180
                                game_selection_mode = False
                                current_game = None
                                donation_mode = True
                                take_mode = False
                                input_active = True
                                input_text = str(donation_total)
        elif event.type == pygame.KEYDOWN:
            if in_rehab and event.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()
            elif donation_mode or take_mode:
                if event.key == pygame.K_RETURN:
                    try:
                        amount = float(input_text)
                        if take_mode:
                            if amount > 500:
                                message = "Maximum amount to take is $500!"
                                show_message = True
                                message_timer = 180
                            else:
                                amount_to_take = amount
                                game_selection_mode = True
                                message = f"Choose a game to win ${amount:.2f}!"
                                show_message = True
                                message_timer = 180
                                if take_count >= 5:
                                    in_rehab = True  # Trigger rehab after 5 tries
                        else:
                            message = f"Thank you for donating ${amount:.2f}!"
                            show_message = True
                            message_timer = 180
                        donation_mode = False
                        take_mode = False
                        input_text = ""
                    except ValueError:
                        message = "Please enter a valid number"
                        show_message = True
                        message_timer = 180
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode == '.':
                        input_text += event.unicode
            elif current_game:
                if current_game.handle_event(event):
                    result = current_game.get_result()
                    if result is not None:
                        if result:
                            message = f"Congratulations! You won ${amount_to_take:.2f}!"
                        else:
                            donation_total = amount_to_take * 2
                            message = f"Sorry, you lost! You must donate ${donation_total:.2f}."
                            show_message = True
                            message_timer = 180
                            game_selection_mode = False
                            current_game = None

    # Update message timer
    if show_message and message_timer > 0:
        message_timer -= 1
        if message_timer == 0:
            show_message = False

    # Fill the screen with sky blue
    screen.fill(SKY_BLUE)

    if in_rehab:
        # Draw rehab message
        title = title_font.render("REHAB REQUIRED", True, (255, 0, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        
        message = message_font.render("You've taken money too many times. Time to reflect and meditate.", True, STEEL_BLUE)
        screen.blit(message, (WIDTH//2 - message.get_width()//2, 300))
        
        continue_text = "Do you really want to waste your life on gambling?"
        continue_surface = message_font.render(continue_text, True, STEEL_BLUE)
        screen.blit(continue_surface, (WIDTH//2 - continue_surface.get_width()//2, 400))
    elif current_game:
        if current_game.update():
            result = current_game.get_result()
            if result is not None:
                if result:
                    message = f"Congratulations! You won ${amount_to_take:.2f}!"
                else:
                    donation_total = amount_to_take * 2
                    message = f"Sorry, you lost! You must donate ${donation_total:.2f}."
                    show_message = True
                    message_timer = 180
                    game_selection_mode = False
                    current_game = None
        else:
            current_game.draw()
    else:
        # Draw title with subtle glow effect
        title = title_font.render("Charity and Chance", True, STEEL_BLUE)
        title_glow = title_font.render("Charity and Chance", True, DEEP_BLUE)
        screen.blit(title_glow, (WIDTH//2 - title.get_width()//2 + 2, 52))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        # Draw buttons with rounded corners
        # Take button
        draw_rounded_rect(screen, GOLD, take_button, BUTTON_RADIUS)
        take_text = button_font.render("Take", True, STEEL_BLUE)
        screen.blit(take_text, (take_button.centerx - take_text.get_width()//2, 
                               take_button.centery - take_text.get_height()//2))

        # Donate button
        draw_rounded_rect(screen, GOLD, donate_button, BUTTON_RADIUS)
        donate_text = button_font.render("Donate", True, STEEL_BLUE)
        screen.blit(donate_text, (donate_button.centerx - donate_text.get_width()//2, 
                                 donate_button.centery - donate_text.get_height()//2))

        # Draw input field if in donation or take mode
        if donation_mode or take_mode:
            # Draw prompt
            prompt_text = "Enter donation amount ($):" if donation_mode else "Enter amount to take ($) [Max: $500]:"
            prompt = input_font.render(prompt_text, True, STEEL_BLUE)
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 80))
            
            # Draw input box with rounded corners
            draw_rounded_rect(screen, PALE_BLUE, input_rect, 5)
            pygame.draw.rect(screen, DEEP_BLUE, input_rect, 2, border_radius=5)
            
            # Draw input text
            text_surface = input_font.render(input_text, True, STEEL_BLUE)
            screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))
        
        # Draw game selection buttons if in game selection mode
        if game_selection_mode:
            # Draw prompt
            prompt = message_font.render("Choose a game to play:", True, STEEL_BLUE)
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 100))
            
            # Roulette button
            draw_rounded_rect(screen, GOLD, roulette_button, BUTTON_RADIUS)
            roulette_text = button_font.render("Roulette", True, STEEL_BLUE)
            screen.blit(roulette_text, (roulette_button.centerx - roulette_text.get_width()//2, 
                                       roulette_button.centery - roulette_text.get_height()//2))
            
            # Slot Machine button
            draw_rounded_rect(screen, GOLD, slot_button, BUTTON_RADIUS)
            slot_text = button_font.render("Slots", True, STEEL_BLUE)
            screen.blit(slot_text, (slot_button.centerx - slot_text.get_width()//2, 
                                   slot_button.centery - slot_text.get_height()//2))

    # Draw take attempts counter
    attempt_text = f"Take Attempts: {take_count}"
    attempt_surface = message_font.render(attempt_text, True, STEEL_BLUE)
    screen.blit(attempt_surface, (10, 10))

    # Draw message if active
    if show_message:
        message_surface = message_font.render(str(message),True, (70, 130, 180))
        message_rect = message_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        # Draw semi-transparent background for message
        s = pygame.Surface((message_rect.width + 40, message_rect.height + 20))
        s.set_alpha(200)
        s.fill(LIGHT_BLUE)
        screen.blit(s, (message_rect.x - 20, message_rect.y - 10))
        screen.blit(message_surface, message_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()