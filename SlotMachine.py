import pygame
import random

class SlotMachine:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.bg_color = (0, 100, 0)  # Dark green background
        self.text_color = (255, 255, 255)
        self.frame_color = (139, 69, 19)  # Brown frame
        
        # Fonts
        self.font = pygame.font.SysFont('Times New Roman', 24)
        self.title_font = pygame.font.SysFont('Times New Roman', 36, bold=True)
        
        # Game state
        self.spinning = False
        self.spin_time = 0
        self.wait_time = 0
        self.symbols = [0, 0, 0]  # Current symbols
        self.result = None
        self.show_result = False
        self.waiting_for_enter = False
        
        # Load and scale symbols
        self.symbol_size = 100
        try:
            # Load the actual images
            cherry = pygame.image.load('cherry-removebg-preview.png').convert_alpha()
            lemon = pygame.image.load('lemon-removebg-preview.png').convert_alpha()
            seven = pygame.image.load('seven-removebg-preview.png').convert_alpha()
            
            # Scale the images
            self.symbol_images = [
                pygame.transform.scale(cherry, (self.symbol_size, self.symbol_size)),
                pygame.transform.scale(lemon, (self.symbol_size, self.symbol_size)),
                pygame.transform.scale(seven, (self.symbol_size, self.symbol_size))
            ]
        except pygame.error:
            # Fallback to colored squares if images can't be loaded
            self.symbol_images = [
                pygame.Surface((self.symbol_size, self.symbol_size)),
                pygame.Surface((self.symbol_size, self.symbol_size)),
                pygame.Surface((self.symbol_size, self.symbol_size))
            ]
            self.symbol_images[0].fill((255, 0, 0))  # Red for cherry
            self.symbol_images[1].fill((255, 255, 0))  # Yellow for lemon
            self.symbol_images[2].fill((0, 0, 255))  # Blue for seven
        
        # Button properties
        self.button_width = 100
        self.button_height = 50
        self.button_x = self.width//2 - self.button_width//2
        self.button_y = self.height - 100
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.spinning and not self.waiting_for_enter:
                # Check if spin button was clicked
                button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
                if button_rect.collidepoint(event.pos):
                    self.spin()
                    return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.waiting_for_enter:
                return True  # Signal to return to home
        return False
    
    def spin(self):
        self.spinning = True
        self.spin_time = 0
        self.wait_time = 0
        self.symbols = [0, 0, 0]
        self.result = None
        self.show_result = False
        self.waiting_for_enter = False
    
    def update(self):
        if self.spinning:
            self.spin_time += 1
            if self.spin_time >= 60:  # 1 second at 60 FPS
                self.spinning = False
                self.symbols = [random.randint(0, 2) for _ in range(3)]
                self.result = all(s == self.symbols[0] for s in self.symbols)
                self.wait_time = 0
        elif self.result is not None and not self.show_result:
            self.wait_time += 1
            if self.wait_time >= 30:  # 0.5 second wait after spinning
                self.show_result = True
                self.waiting_for_enter = True
                return True
        return False
    
    def get_result(self):
        return self.result
    
    def draw(self):
        # Fill background
        self.screen.fill(self.bg_color)
        
        # Draw title
        title = self.title_font.render("Slot Machine", True, self.text_color)
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        # Draw frame
        frame_rect = pygame.Rect(self.width//2 - 150, self.height//2 - 100, 300, 200)
        pygame.draw.rect(self.screen, self.frame_color, frame_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), frame_rect, 5)
        
        # Draw symbols
        for i in range(3):
            x = self.width//2 - 90 + i * 60
            y = self.height//2 - 30
            if self.spinning:
                # Show spinning animation
                symbol = self.symbol_images[random.randint(0, 2)]
            else:
                symbol = self.symbol_images[self.symbols[i]]
            self.screen.blit(symbol, (x, y))
        
        # Draw spin button
        button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        button_color = (139, 69, 19) if self.spinning else (255, 215, 0)  # Brown when spinning, Gold otherwise
        pygame.draw.rect(self.screen, button_color, button_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
        
        button_text = "Spinning..." if self.spinning else "Spin"
        text_surface = self.font.render(button_text, True, (255, 0, 0))
        self.screen.blit(text_surface, (button_rect.centerx - text_surface.get_width()//2,
                                      button_rect.centery - text_surface.get_height()//2))
        
        # Draw result
        if self.show_result:
            result_text = "You won!" if self.result else "You lost!"
            result_surface = self.font.render(result_text, True, self.text_color)
            self.screen.blit(result_surface, (self.width//2 - result_surface.get_width()//2,
                                            self.height//2 + 120))
            
            # Draw "Press Enter to continue" message
            continue_text = "Press Enter to continue"
            continue_surface = self.font.render(continue_text, True, self.text_color)
            self.screen.blit(continue_surface, (self.width//2 - continue_surface.get_width()//2,
                                              self.height//2 + 160))