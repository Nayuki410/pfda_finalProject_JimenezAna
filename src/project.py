#importing required library
import pygame
import random

pygame.init()

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=(255, 255, 255), font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        
    def draw(self, screen):
        # Draw button rectangle
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        
        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Check if mouse is hovering over button
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if button was clicked
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

def main():
    # Initialize Pygame window  (width, height)
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Whisker Wishes")
    clock = pygame.time.Clock()
    
    # Creating buttons  (side to side loc.,top to bottom pos., width, height)
    menu_buttons = [
        Button(60, 700, 140, 50, "Wish", (0, 100, 0), (0, 150, 0)),
        Button(230, 700, 140, 50, "Timer", (100, 100, 0), (150, 150, 0)),
        Button(400, 700, 140, 50, "Quit", (100, 0, 0), (150, 0, 0))
    ]

    random_cat = {1:'Art\\1.png',
                  2:'Art\\2.png',
                  3:'Art\\3.png',
                  4:'Art\\4.png',
                  5:'Art\\5.png',
                  6:'Art\\6.png'}
    
    gamestate = "Menu"
    wish_select = None
    running = True
    while running:
                
        match gamestate:
            case "Menu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                # Handle button events
                    for button in menu_buttons:
                        if button.handle_event(event):
                            if button.text == "Wish":
                                print("Wishing...")
                                gamestate = "Wishing"
                                wish_select = pygame.image.load(random_cat[random.randrange(1,7)]).convert()
                            elif button.text == "Timer":
                                print("Timing...")
                            elif button.text == "Quit":
                                running = False
                # Draw everything
                screen.fill((160, 160, 160))  # Background color
                for button in menu_buttons:
                    button.draw(screen)
                pygame.display.flip()
                clock.tick(60)
                continue

            case "Wishing":
                X = 600
                Y = 800
                
                # create the display surface object
                # of specific dimension..e(X, Y).
                scrn = pygame.display.set_mode((X, Y))
                
                # set the pygame window name
                pygame.display.set_caption('Whisker Wishes')
                
                # Creating buttons
                wish_buttons = [
                    Button(300, 200, 200, 50, "Wish Again", (0, 100, 0), (0, 150, 0)),
                    Button(300, 200, 200, 50, "Back", (0, 100, 0), (0, 150, 0))]

                # Handle button events
                for button in wish_buttons:
                    if button.handle_event(event):
                        if button.text == "Wish":
                            print("Wishing...")
                            gamestate = "Wishing"
                            wish_select = pygame.image.load(random_cat[random.randrange(1,7)]).convert()
                            
                        elif button.text == "Back":
                            print("Going back...")
                            gamestate = "Menu"

                # Using blit to copy content from one surface to other
                scrn.blit(wish_select, (0, 0))
                
                # paint screen one time
                pygame.display.flip()
                status = True
                while (status):
                
                # iterate over the list of Event objects
                # that was returned by pygame.event.get() method.
                    for i in pygame.event.get():
                
                        # if event object type is QUIT
                        # then quitting the pygame
                        # and program both.
                        if i.type == pygame.QUIT:
                            status = False


            case "Timer":
                continue

    pygame.quit()

if __name__ == "__main__":
    main()

 