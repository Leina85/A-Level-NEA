import pygame
import sys

# =============
# CONFIGURATION
# =============

# Screen setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colours
colours = {
    'btn_active' : '#4A7090',
    'btn_passive' : '#86A6C1',
    'background_colour' : '#F2F2F2',
    'text_colour' : '#F2F2F2'
}

# Button dimensions
BTN_SIZE = (240, 64)

# Track which button is active
active_btn = None

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

# ==================================
# Drawing Everything onto the Screen
# ==================================

def draw_btn(screen, font, btn_id):
    

# ==============
# Event Handling (check handle_mouse_click() for efficiency and if active = ... is in the right place
# ==============

def handle_mouse_click(pos):
    # takes pos, the coordinates of the mouse click as a parameter
    # resets the clicked_btn
    clicked_btn = None
    for btn_id, btn_data in SCREEN['buttons'].items():
        btn_rect = pygame.Rect(0, 0, *BTN_SIZE)
        btn_rect.center = btn_data['pos']
        # If the click is on the button, that button becomes active
        if btn_rect.collidepoint(pos):
            clicked_btn = btn_id
            break
    
    # The clicked button becomes active
    set_active_btn(clicked_btn)

def handle_key_input():
    # Key inputs only used for button inputs so reliant on a button being active
    active = get_active_btn()
    
    # Exits function if no active button
    if not active:
        return
    
    # Function continues so a button must be active, its assigned the variable 'button'
    button = SCREEN['buttons'][active]
    if event.key == pygame.K_BACKSPACE:
        # Backspace deletes the last character of the input
        button['text'] = button['text'][:-1]
    elif event.key == pygame.K_RETURN and button['text']:
        # Enter outputs the text to the command line
        print(f"Input for button {active}: {button['text']}")
    elif event.unicode.isdigit() and len(button['text']) < 7:
        # User can input only numbers and has a character limit of 7 (later this will need to be specific per button as different inputs will need different limits)
        button['text'] += event.unicode

# =================
# Screen Management
# =================

def render_screen(screen, font):
    active = get_active_btn()
    
    # Clear the screen and draw the background and title of the screen
    clear_screen(screen)
    draw_title(screen, font, SCREEN['title'])
    
    # Draw the appropriate buttons
    for btn_id, btn_data in SCREEN['buttons']:
        draw_btn(screen, font, btn_id)

def update_screen():
    # Update the display
    pygame.display.update()

# ============
# Main Program
# ============

def start_pygame():
    # Initilise pygame
    # Create the window using constants defined at the start of the program
    # Create clock and font
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 70)
    return screen, clock, font

def events():
    # Call the appropriate function for each event
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            handle_key_input()

def main():
    screen, clock, font = start_pygame()
    
    # Check events, render the screen and update it
    while True:
        events()
        render_screen(screen, font)
        update_screen()
        clock.tick(FPS)

# Run Program
main()