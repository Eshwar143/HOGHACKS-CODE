import pygame

class Rehab:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Times New Roman', 36, bold=True)
        self.width, self.height = screen.get_size()

    def draw(self):
        # Draw rehab screen
        rehab_title = self.font.render("REHAB REQUIRED", True, (255, 0, 0))
        self.screen.blit(rehab_title, (self.width // 2 - rehab_title.get_width() // 2, 200))

        message = self.font.render("You've taken money too many times. Time to reflect and meditate.", True, (70, 130, 180))
        self.screen.blit(message, (self.width // 2 - message.get_width() // 2, 300))

        continue_text = "Press Enter to exit rehab"
        continue_surface = self.font.render(continue_text, True, (70, 130, 180))
        self.screen.blit(continue_surface, (self.width // 2 - continue_surface.get_width() // 2, 400))
