import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

# Screen setup
screen = pygame.display.set_mode([1280, 720])
font = pygame.font.Font(None, 70)

# Button dimensions
btn_size = (240, 64)

# Track which button is active
active_btn = None

# Colours
colours = {
    'btn_active' : '#4A7090',
    'btn_passive' : '#86A6C1',
    'background_colour' : '#F2F2F2',
    'text_colour' : '#F2F2F2'
}

# Standard Button position and text to be used in standard_button subroutine
standard_btns = {
    1: {'pos': (640, 260), 'text': ''},
    2: {'pos': (640, 360), 'text': ''},
    3: {'pos': (640, 460), 'text': ''}
}

# Standard button function
def draw_button(pos, text, btn_id, is_active=False):
    #Draw a standard input button
    rect = pygame.Rect(0, 0, *btn_size)
    rect.center = pos
    
    color = colours['btn_active'] if is_active else colours['btn_passive']
    pygame.draw.rect(screen, color, rect)
    
    # Show placeholder number if empty and not active
    display_text = text if text or is_active else str(btn_id)
    text_surf = font.render(display_text, True, colours['text'])
    text_rect = text_surf.get_rect(midleft=(rect.x + 5, rect.centery))
    screen.blit(text_surf, text_rect)
    
    return rect

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
                btn_rect = standard_btn(standard_btn_width, standard_btn_height, standard_btn_data['pos'], active_btn == standard_btn_key, standard_btn_data['text'], standard_btn_key, btn_colour_active, btn_passive, screen, base_font, text_colour)
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
        standard_btn(standard_btn_width, standard_btn_height, standard_btn_data['pos'], active_btn == standard_btn_key, standard_btn_data['text'], standard_btn_key, btn_colour_active, btn_passive, screen, base_font, text_colour)

    pygame.display.update()
    clock.tick(60)