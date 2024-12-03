#importing required library
import pygame
import random
import sys

pygame.init()

pomodoro_length = 1500 # 1500 secs / 25 mins
short_break_length = 300 # 30 secs / 5 mins
long_break_length = 900 # 900 secs / 15 mins
coin_wallet = 0
owned_kittens = []
current_seconds = pomodoro_length
timer_enabled = False
running = True

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

def handle_common_events(events):
    global current_seconds, running, timer_enabled, coin_wallet
    for event in events:
        match event.type:
            case pygame.USEREVENT:
                if not timer_enabled:
                    continue
                
                current_seconds -= 1 * 60
                
                if current_seconds <= 0:
                    timer_enabled = False
                    coin_wallet += 1
                    
                
            case pygame.QUIT:
                running = False
    
def get_timer_minutes_seconds():
    if current_seconds >= 0:
        display_seconds = current_seconds % 60
        display_minutes = int(current_seconds / 60) % 60
        return(display_minutes, display_seconds)
    return (0,0)

def store_kitten(kitten):
    global owned_kittens, coin_wallet
    coin_wallet -= 1
    scaled_kitten = pygame.transform.scale(kitten, (100, 149))
    owned_kittens.append(scaled_kitten)

def main():
    global running, coin_wallet
    
    # Initialize Pygame window  (width, height)
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Whisker Wishes")
    clock = pygame.time.Clock()
    
    # Creating buttons  (side to side loc.,top to bottom pos., width, height)
    menu_buttons = [
        Button(60, 700, 140, 50, "Wish", (114, 109, 181), (92, 86, 163)),
        Button(230, 700, 140, 50, "Timer", (204, 114, 128), (181, 87, 102)),
        Button(400, 700, 140, 50, "Quit", (204, 103, 82), (179, 81, 61))
    ]

    random_cat = {1:'Art\\1.png',
                  2:'Art\\2.png',
                  3:'Art\\3.png',
                  4:'Art\\4.png',
                  5:'Art\\5.png',
                  6:'Art\\6.png'}
    
    gamestate = "Menu"
    wish_select = None
    started = False
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    while running:
        events = pygame.event.get()
        handle_common_events(events)
        
        match gamestate:
            case "Menu":
                for event in events:
                # Handle button events
                    for button in menu_buttons:
                        if button.handle_event(event):
                            if button.text == "Wish" and coin_wallet > 0:
                                print("Wishing...")
                                gamestate = "Wishing"
                                wish_select = pygame.image.load(random_cat[random.randrange(1,7)]).convert_alpha()
                                store_kitten(wish_select)
                            elif button.text == "Wish" and coin_wallet == 0:
                                print("Not Enough Coins!")
                            elif button.text == "Timer":
                                gamestate = "Timer"
                                print("Timer...")
                            elif button.text == "Quit":
                                print("Exiting...")
                                running = False
                
                # Draw everything
                screen.fill((160, 160, 160))  # Background color
                menu_background = pygame.image.load('Art\\Menu.jpg')
                screen.blit(menu_background, (0, 0))
                x = 0 
                i = 0
                for kitten in owned_kittens:
                    screen.blit(kitten, ((x % 6) * 100, 800 - 120 - ((i // 6) * 140)))
                    i += 1
                    x += 1
                
                for button in menu_buttons:
                    button.draw(screen)
                    

            case "Wishing":

                # set the pygame window name
                pygame.display.set_caption('Whisker Wishes')
                
                # Creating buttons
                wish_buttons = [
                    Button(60, 700, 140, 50, "Wish Again", (114, 109, 181), (92, 86, 163)),
                    Button(400, 700, 140, 50, "Back", (204, 114, 128), (181, 87, 102))]

                for event in events:
                    # Handle button events
                    for button in wish_buttons:
                        if button.handle_event(event):
                            if button.text == "Wish Again" and coin_wallet > 0:
                                print("Wishing...")
                                wish_select = pygame.image.load(random_cat[random.randrange(1,7)]).convert_alpha()
                                store_kitten(wish_select)
                            elif button.text == "Wish Again" and coin_wallet == 0:
                                print("Not Enough Coins!")
                            elif button.text == "Back":
                                print("Going back...")
                                gamestate = "Menu"

                # Using blit to copy content from one surface to other
                screen.fill((160, 160, 160))  # Background color
                wish_background = pygame.image.load('Art\\Wish.jpg')
                screen.blit(wish_background, (0, 0))
                screen.blit(wish_select, (0, 0))
                for button in wish_buttons:
                    button.draw(screen)
                

            case "Timer":
                global timer_enabled, current_seconds
                # set the pygame window name
                pygame.display.set_caption('Whisker Wishes')
                timer_text = ""

                # Creating buttons
                time_buttons = [
                    Button(225, 500, 150, 50, "Start / Pause", (219, 136, 149), (191, 101, 115)),
                    Button(35, 65, 140, 50, "Pomodoro", (156, 95, 140), (128, 70, 113)),
                    Button(225, 65, 150, 50, "Short Break", (156, 95, 140), (128, 70, 113)),
                    Button(425, 65, 140, 50, "Long Break", (156, 95, 140), (128, 70, 113)),
                    Button(400, 700, 140, 50, "Back", (214, 75, 110), (173, 49, 80))]
                
                global current_seconds
                for event in events:
                    (display_minutes, display_seconds) = get_timer_minutes_seconds()
                    # Handle button events
                    for button in time_buttons:
                        if button.handle_event(event):
                            if button.text == "Start / Pause" and current_seconds > 0:
                                if timer_enabled:
                                    timer_enabled = False
                                    print("Pausing...")
                                else:
                                    timer_enabled = True
                                    print("Starting...")
                            if button.text == "Pomodoro":
                                current_seconds = pomodoro_length
                                timer_enabled = False
                                print("Pomodoro Selected...")
                            if button.text == "Short Break":
                                current_seconds = short_break_length
                                print("Short Break Selected...")
                            if button.text == "Long Break":
                                current_seconds = long_break_length
                                print("Long Break Selected...")
                                    
                            elif button.text == "Back":      
                                print("Going back...")
                                gamestate = "Menu"
                    timer_text = (f"{display_minutes:02}:{display_seconds:02}")
                    # Render text
                    font = pygame.font.Font(None, 80)
                    text_surface = font.render(timer_text, True, (200, 200, 200), (0, 0, 0))
                    text_rect = text_surface.get_rect(center = pygame.Rect(225, 255, 140, 50).center)

                    # Using blit to copy content from one surface to other
                    screen.fill((160, 160, 160))  # Background color
                    timer_background = pygame.image.load('Art\\Timer.jpg')
                    screen.blit(timer_background, (0, 0))
                    for button in time_buttons:
                        button.draw(screen)
                    screen.blit(text_surface, text_rect)


        coin_wallet_text = (f": {coin_wallet:01}")
        # Render text
        font = pygame.font.Font(None, 40)
        text_surface = font.render(coin_wallet_text, True, (200, 200, 200), (0, 0, 0))
        text_rect = text_surface.get_rect(center = pygame.Rect(500, 10, 140, 50).center)
        coin_icon = pygame.image.load('Art\\Coin.png')


        screen.blit(text_surface, text_rect)
        screen.blit(coin_icon, (510, 10))
        
        # paint screen one time
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

 