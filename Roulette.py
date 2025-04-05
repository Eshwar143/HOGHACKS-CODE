import pygame
import random

class Roulette:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.bg_color = (0, 100, 0)  # Dark green background
        self.grid_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.red_color = (255, 0, 0)
        self.black_color = (0, 0, 0)
        self.border_color = (255, 255, 255)
        
        # Fonts
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        
        # Game state
        self.spinning = False
        self.spin_time = 0
        self.result = None
        self.guess = None
        self.game_over = False
        
        # Input field
        self.input_rect = pygame.Rect(self.width//2 - 100, self.height//2 + 150, 200, 50)
        self.input_text = ""
        self.input_active = False
        
        # Calculate grid dimensions
        self.cell_size = 60
        self.grid_width = 4 * self.cell_size  # 4 columns for 20 numbers
        self.grid_height = 5 * self.cell_size  # 5 rows for 20 numbers
        self.grid_x = (self.width - self.grid_width) // 2
        self.grid_y = (self.height - self.grid_height) // 2
        
        # Create number grid (1-20)
        self.numbers = list(range(1, 21))  # Numbers 1-20
        self.grid = []
        for i in range(5):  # 5 rows
            row = []
            for j in range(4):  # 4 columns
                num = self.numbers[i * 4 + j]
                row.append(num)
            self.grid.append(row)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False
                
            if not self.spinning and not self.game_over:
                # Check if a number was clicked
                for i in range(5):  # 5 rows
                    for j in range(4):  # 4 columns
                        rect = pygame.Rect(
                            self.grid_x + j * self.cell_size,
                            self.grid_y + i * self.cell_size,
                            self.cell_size,
                            self.cell_size
                        )
                        if rect.collidepoint(event.pos):
                            self.guess = self.grid[i][j]
                            self.spin()
                            return True
        elif event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                try:
                    self.guess = int(self.input_text)
                    if 1 <= self.guess <= 20:  # Check if guess is between 1-20
                        self.spin()
                        return True
                except ValueError:
                    pass
                self.input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if event.unicode.isdigit():
                    self.input_text += event.unicode
        return False
    
    def spin(self):
        self.spinning = True
        self.spin_time = 0
        self.result = None
        self.game_over = False
    
    def update(self):
        if self.spinning:
            self.spin_time += 1
            if self.spin_time >= 60:  # 1 second at 60 FPS
                self.spinning = False
                self.result = random.randint(1, 20)  # Random number between 1-20
                self.game_over = True
                return True
        return False
    
    def get_result(self):
        if self.game_over and self.result is not None:
            return self.result == self.guess
        return None
    
    def draw(self):
        # Fill background
        self.screen.fill(self.bg_color)
        
        # Draw title
        title = self.title_font.render("Roulette", True, self.text_color)
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        # Draw instructions
        instructions = self.font.render("Click a number or enter your guess (1-20):", True, self.text_color)
        self.screen.blit(instructions, (self.width//2 - instructions.get_width()//2, 120))
        
        # Draw grid
        for i in range(5):  # 5 rows
            for j in range(4):  # 4 columns
                num = self.grid[i][j]
                rect = pygame.Rect(
                    self.grid_x + j * self.cell_size,
                    self.grid_y + i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                # Alternate colors
                color = self.red_color if num % 2 == 0 else self.black_color
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.border_color, rect, 2)
                
                # Draw number
                text = self.font.render(str(num), True, self.text_color)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
        
        # Draw input field
        pygame.draw.rect(self.screen, self.text_color, self.input_rect, 2)
        text_surface = self.font.render(self.input_text, True, self.text_color)
        self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 10))
        
        # Draw result if game is over
        if self.game_over:
            result_text = f"Result: {self.result}"
            if self.result == self.guess:
                result_text += " - You won!"
            else:
                result_text += " - You lost!"
            result_surface = self.font.render(result_text, True, self.text_color)
            self.screen.blit(result_surface, (self.width//2 - result_surface.get_width()//2, self.height - 100)) 