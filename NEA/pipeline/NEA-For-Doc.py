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

# Colours
btn_colour_active = '#4A7090'
btn_colour_passive = '#86A6C1'
background_colour = '#F2F2F2'
text_colour = '#F2F2F2'

# Standard Button position and text to be used in standard_button subroutine
standard_btns = {
    1: {'pos': (screen.get_width() // 2, screen.get_height() // 2), 'text': ''},
    2: {'pos': (screen.get_width() // 2, screen.get_height() // 2 + 100), 'text': ''},
    3: {'pos': (screen.get_width() // 2, screen.get_height() // 2 - 100), 'text': ''}
}

# Standard button function
def standard_btn(width, height, center, active, user_text, standard_button_key, btn_color_active, btn_color_passive, screen, base_font, text_color):
    # Create the button
    standard_btn = pygame.Rect(0, 0, width, height)
    standard_btn.center = center

    # Determine button color
    btn_color = btn_color_active if active else btn_color_passive
    pygame.draw.rect(screen, btn_color, standard_btn)

    # Display placeholder or user input
    if user_text == '' and not active:
        text_surf = base_font.render(str(standard_button_key), True, text_color)
    else:
        text_surf = base_font.render(user_text, True, text_color)

    # Center the text vertically
    text_rect = text_surf.get_rect(midleft=(standard_btn.x + 5, standard_btn.centery))
    screen.blit(text_surf, text_rect)

    return standard_btn

# Main loop
while True:
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click to activate a button
        if event.type == pygame.MOUSEBUTTONDOWN:
            for standard_btn_key, standard_btn_data in standard_btns.items():
                btn_rect = standard_btn(standard_btn_width, standard_btn_height, standard_btn_data['pos'], active_btn == standard_btn_key, standard_btn_data['text'], standard_btn_key, btn_colour_active, btn_colour_passive, screen, base_font, text_colour)
                if btn_rect.collidepoint(event.pos):
                    active_btn = standard_btn_key
                    break
            else:
                active_btn = None  # Deselect if clicked outside

        # Input handling
        if event.type == pygame.KEYDOWN and active_btn:
            if event.key == pygame.K_BACKSPACE:
                standard_btns[active_btn]['text'] = standard_btns[active_btn]['text'][:-1]
            elif event.unicode.isdigit() and len(standard_btns[active_btn]['text']) < 7:  # Only allow digits
                standard_btns[active_btn]['text'] += event.unicode
            elif event.key == pygame.K_RETURN and len(standard_btns[active_btn]['text']) > 0:
                print(f"User input for button {active_btn}:", standard_btns[active_btn]['text'])

    
    # Set background colour
    screen.fill(background_colour)
    
    # Draw each button and update its state
    for standard_btn_key, standard_btn_data in standard_btns.items():
        standard_btn(standard_btn_width, standard_btn_height, standard_btn_data['pos'], active_btn == standard_btn_key, standard_btn_data['text'], standard_btn_key, btn_colour_active, btn_colour_passive, screen, base_font, text_colour)

    pygame.display.update()
    clock.tick(60)