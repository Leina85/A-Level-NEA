import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

# Screen setup
screen = pygame.display.set_mode([1280, 720])
base_font = pygame.font.Font(None, 70)

# Standard Button dimensions
standard_btn_width = 240
standard_btn_height = 64

# Track which button is active
active_btn = None

# Track current screen (0 = main menu, 1 = second menu)
current_screen = 0

# Colours
btn_colour_active = '#4A7090'
btn_colour_passive = '#86A6C1'
menu_btn_color = '#2E5266'  # Different color for menu navigation button
background_colour = '#F2F2F2'
text_colour = '#F2F2F2'

# Main screen buttons (your original buttons)
screen_0_btns = {
    1: {'pos': (screen.get_width() // 2, screen.get_height() // 2), 'text': ''},
    2: {'pos': (screen.get_width() // 2, screen.get_height() // 2 + 100), 'text': ''},
    3: {'pos': (screen.get_width() // 2, screen.get_height() // 2 - 100), 'text': ''}
}

# Second screen buttons
screen_1_btns = {
    1: {'pos': (screen.get_width() // 2, screen.get_height() // 2 - 50), 'text': ''},
    2: {'pos': (screen.get_width() // 2, screen.get_height() // 2 + 50), 'text': ''},
}

# Menu navigation button (appears on main screen)
menu_btn_rect = pygame.Rect(50, 50, 200, 60)

# Back button (appears on second screen)
back_btn_rect = pygame.Rect(50, 50, 150, 60)

# Standard button function
def standard_btn(width, height, center, active, user_text, standard_button_key, btn_color_active, btn_color_passive, screen, base_font, text_color):
    # Create the button
    button_rect = pygame.Rect(0, 0, width, height)
    button_rect.center = center

    # Determine button color
    btn_color = btn_color_active if active else btn_color_passive
    pygame.draw.rect(screen, btn_color, button_rect)

    # Display placeholder or user input
    if user_text == '' and not active:
        text_surf = base_font.render(str(standard_button_key), True, text_color)
    else:
        text_surf = base_font.render(user_text, True, text_color)

    # Center the text vertically
    text_rect = text_surf.get_rect(midleft=(button_rect.x + 5, button_rect.centery))
    screen.blit(text_surf, text_rect)

    return button_rect

# Navigation button function
def nav_btn(rect, text, color, screen, font, text_color):
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return rect

# Main loop
while True:
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == 0:  # Main screen
                # Check menu button click
                if menu_btn_rect.collidepoint(event.pos):
                    current_screen = 1
                    active_btn = None  # Reset active button when switching screens
                    continue
                
                # Check main screen buttons
                for standard_btn_key, standard_btn_data in screen_0_btns.items():
                    btn_rect = standard_btn(standard_btn_width, standard_btn_height, standard_btn_data['pos'], active_btn == standard_btn_key, standard_btn_data['text'], standard_btn_key, btn_colour_active, btn_colour_passive, screen, base_font, text_colour)
                    if btn_rect.collidepoint(event.pos):
                        active_btn = standard_btn_key
                        break
                else:
                    active_btn = None  # Deselect if clicked outside
                    
            elif current_screen == 1:  # Second screen
                # Check back button click
                if back_btn_rect.collidepoint(event.pos):
                    current_screen = 0
                    active_btn = None  # Reset active button when switching screens
                    continue
                
                # Check second screen buttons
                for standard_btn_key, standard_btn_data in screen_1_btns.items():
                    btn_rect = standard_btn(standard_btn_width, standard_btn_height, standard_btn_data['pos'], active_btn == standard_btn_key, standard_btn_data['text'], standard_btn_key, btn_colour_active, btn_colour_passive, screen, base_font, text_colour)
                    if btn_rect.collidepoint(event.pos):
                        active_btn = standard_btn_key
                        break
                else:
                    active_btn = None  # Deselect if clicked outside

        # Input handling
        if event.type == pygame.KEYDOWN and active_btn:
            current_btns = screen_0_btns if current_screen == 0 else screen_1_btns
            
            if event.key == pygame.K_BACKSPACE:
                current_btns[active_btn]['text'] = current_btns[active_btn]['text'][:-1]
            elif event.unicode.isdigit() and len(current_btns[active_btn]['text']) < 7:  # Only allow digits
                current_btns[active_btn]['text'] += event.unicode
            elif event.key == pygame.K_RETURN and len(current_btns[active_btn]['text']) > 0:
                screen_name = "main screen" if current_screen == 0 else "second screen"
                print(f"User input for button {active_btn} on {screen_name}:", current_btns[active_btn]['text'])

    # Set background colour
    screen.fill(background_colour)
    
    # Draw current screen
    if current_screen == 0:  # Main screen
        # Draw menu navigation button
        nav_btn(menu_btn_rect, "Open Menu", menu_btn_color, screen, base_font, text_colour)
        
        # Draw main screen buttons
        for standard_btn_key, standard_btn_data in screen_0_btns.items():
            standard_btn(standard_btn_width, standard_btn_height, standard_btn_data['pos'], active_btn == standard_btn_key, standard_btn_data['text'], standard_btn_key, btn_colour_active, btn_colour_passive, screen, base_font, text_colour)
            
        # Draw screen title
        title_surf = base_font.render("Main Screen", True, '#333333')
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surf, title_rect)
        
    elif current_screen == 1:  # Second screen
        # Draw back button
        nav_btn(back_btn_rect, "Back", menu_btn_color, screen, base_font, text_colour)
        
        # Draw second screen buttons
        for standard_btn_key, standard_btn_data in screen_1_btns.items():
            standard_btn(standard_btn_width, standard_btn_height, standard_btn_data['pos'], active_btn == standard_btn_key, standard_btn_data['text'], standard_btn_key, btn_colour_active, btn_colour_passive, screen, base_font, text_colour)
            
        # Draw screen title
        title_surf = base_font.render("Second Screen", True, '#333333')
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surf, title_rect)

    pygame.display.update()
    clock.tick(60)