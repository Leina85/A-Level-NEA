import pygame
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
COLORS = {
    'btn_active': '#4A7090',
    'btn_passive': '#86A6C1',
    'nav_btn': '#2E5266',
    'background': '#F2F2F2',
    'text': '#F2F2F2',
    'title': '#333333'
}

# Button dimensions
BTN_SIZE = (240, 64)

# Screen configurations
SCREENS = {
    0: {
        'title': 'Main Screen',
        'buttons': {
            1: {'pos': (640, 260), 'text': ''},
            2: {'pos': (640, 360), 'text': ''},
            3: {'pos': (640, 460), 'text': ''}
        },
        'nav_button': {'rect': pygame.Rect(50, 50, 200, 60), 'text': 'Open Menu', 'action': 'next'}
    },
    1: {
        'title': 'Second Screen',
        'buttons': {
            1: {'pos': (640, 310), 'text': ''},
            2: {'pos': (640, 410), 'text': ''}
        },
        'nav_button': {'rect': pygame.Rect(50, 50, 150, 60), 'text': 'Back', 'action': 'prev'}
    }
}

# ============================================================================
# GLOBAL STATE
# ============================================================================

current_screen = 0
active_btn = None

def get_current_screen():
    return current_screen

def set_current_screen(screen_id):
    global current_screen
    current_screen = screen_id

def get_active_btn():
    return active_btn

def set_active_btn(btn_id):
    global active_btn
    active_btn = btn_id

def reset_active_btn():
    global active_btn
    active_btn = None

# ============================================================================
# RENDERING FUNCTIONS
# ============================================================================

def draw_button(screen, font, pos, size, text, btn_id, is_active=False):
    """Draw a standard input button"""
    rect = pygame.Rect(0, 0, *size)
    rect.center = pos
    
    color = COLORS['btn_active'] if is_active else COLORS['btn_passive']
    pygame.draw.rect(screen, color, rect)
    
    # Show placeholder number if empty and not active
    display_text = text if text or is_active else str(btn_id)
    text_surf = font.render(display_text, True, COLORS['text'])
    text_rect = text_surf.get_rect(midleft=(rect.x + 5, rect.centery))
    screen.blit(text_surf, text_rect)
    
    return rect

def draw_nav_button(screen, font, rect, text):
    """Draw a navigation button"""
    pygame.draw.rect(screen, COLORS['nav_btn'], rect)
    text_surf = font.render(text, True, COLORS['text'])
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_title(screen, font, title, y_pos=100):
    """Draw screen title"""
    title_surf = font.render(title, True, COLORS['title'])
    title_rect = title_surf.get_rect(center=(screen.get_width() // 2, y_pos))
    screen.blit(title_surf, title_rect)

def clear_screen(screen):
    """Clear screen with background color"""
    screen.fill(COLORS['background'])

# ============================================================================
# INPUT HANDLING FUNCTIONS
# ============================================================================

def handle_nav_click(action):
    """Handle navigation button clicks"""
    current = get_current_screen()
    
    if action == 'next':
        set_current_screen(min(current + 1, len(SCREENS) - 1))
    elif action == 'prev':
        set_current_screen(max(current - 1, 0))
    reset_active_btn()

def handle_text_input(event):
    """Handle keyboard input for active button"""
    active = get_active_btn()
    if not active:
        return
        
    current_buttons = SCREENS[get_current_screen()]['buttons']
    
    if event.key == pygame.K_BACKSPACE:
        current_buttons[active]['text'] = current_buttons[active]['text'][:-1]
    elif event.key == pygame.K_RETURN and current_buttons[active]['text']:
        screen_name = SCREENS[get_current_screen()]['title']
        print(f"Input for button {active} on {screen_name}: {current_buttons[active]['text']}")
    elif event.unicode.isdigit() and len(current_buttons[active]['text']) < 7:
        current_buttons[active]['text'] += event.unicode

def handle_mouse_click(pos):
    """Handle mouse clicks"""
    current = get_current_screen()
    screen_config = SCREENS[current]
    
    # Check navigation button
    nav_btn = screen_config['nav_button']
    if nav_btn['rect'].collidepoint(pos):
        handle_nav_click(nav_btn['action'])
        return
    
    # Check input buttons
    clicked_btn = None
    for btn_id, btn_data in screen_config['buttons'].items():
        btn_rect = pygame.Rect(0, 0, *BTN_SIZE)
        btn_rect.center = btn_data['pos']
        if btn_rect.collidepoint(pos):
            clicked_btn = btn_id
            break
    
    set_active_btn(clicked_btn)

# ============================================================================
# SCREEN MANAGEMENT FUNCTIONS
# ============================================================================

def render_current_screen(screen, font):
    """Render the current screen"""
    current = get_current_screen()
    screen_config = SCREENS[current]
    active = get_active_btn()
    
    # Clear and draw background
    clear_screen(screen)
    
    # Draw title
    draw_title(screen, font, screen_config['title'])
    
    # Draw navigation button
    nav_btn = screen_config['nav_button']
    draw_nav_button(screen, font, nav_btn['rect'], nav_btn['text'])
    
    # Draw input buttons
    for btn_id, btn_data in screen_config['buttons'].items():
        draw_button(
            screen, font,
            btn_data['pos'], 
            BTN_SIZE,
            btn_data['text'], 
            btn_id, 
            active == btn_id
        )

def update_display(screen):
    """Update the display"""
    pygame.display.update()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def initialise_pygame():
    """Initialize pygame and return screen, clock, font"""
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 70)
    return screen, clock, font

def handle_events():
    """Handle all pygame events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            handle_text_input(event)

def main():
    # Main game loop
    screen, clock, font = initialise_pygame()
    
    while True:
        handle_events()
        render_current_screen(screen, font)
        update_display(screen)
        clock.tick(FPS)

# Run the main game loop
main()



"""
import pygame
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colours
COLOURS = {
    'btn_active': '#4A7090',
    'btn_passive': '#86A6C1',
    'nav_btn': '#2E5266',
    'background': '#F2F2F2',
    'text': '#F2F2F2',
    'title': '#333333'
}

# Button dimensions
BTN_SIZE = (240, 64)

# Screen configurations
SCREEN = {
    'title': 'Main Screen',
    'buttons': {
        1: {'pos': (640, 260), 'text': ''},
        2: {'pos': (640, 360), 'text': ''},
        3: {'pos': (640, 460), 'text': ''}
    }
}

# ============================================================================
# GLOBAL STATE
# ============================================================================

active_btn = None

def get_active_btn():
    return active_btn

def set_active_btn(btn_id):
    global active_btn
    active_btn = btn_id

def reset_active_btn():
    global active_btn
    active_btn = None

# ============================================================================
# RENDERING FUNCTIONS
# ============================================================================

def draw_btn(screen, font, btn_id):
    # Look up button info inside the function
    btn_data = SCREEN['buttons'][btn_id]
    pos = btn_data['pos']
    text = btn_data['text'] 
    is_active = (get_active_btn() == btn_id)
    
    # Draw the button with the looked-up info
    rect = pygame.Rect(0, 0, *BTN_SIZE)
    rect.center = pos
    
    colour = COLOURS['btn_active'] if is_active else COLOURS['btn_passive']
    pygame.draw.rect(screen, colour, rect)
    
    # Show placeholder number if empty and not active
    display_text = text if text or is_active else str(btn_id)
    text_surf = font.render(display_text, True, COLOURS['text'])
    text_rect = text_surf.get_rect(midleft=(rect.x + 5, rect.centery))
    screen.blit(text_surf, text_rect)
    
    return rect

def draw_title(screen, font, title, y_pos=100):
    # Draw screen title
    title_surf = font.render(title, True, COLOURS['title'])
    title_rect = title_surf.get_rect(center=(screen.get_width() // 2, y_pos))
    screen.blit(title_surf, title_rect)

def clear_screen(screen):
    # Clear screen with background colour
    screen.fill(COLOURS['background'])

# ============================================================================
# INPUT HANDLING FUNCTIONS
# ============================================================================

def handle_text_input(event):
    # Handle keyboard input for active button
    active = get_active_btn()
    if not active:
        return
        
    current_buttons = SCREEN['buttons']
    
    if event.key == pygame.K_BACKSPACE:
        current_buttons[active]['text'] = current_buttons[active]['text'][:-1]
    elif event.key == pygame.K_RETURN and current_buttons[active]['text']:
        print(f"Input for button {active}: {current_buttons[active]['text']}")
    elif event.unicode.isdigit() and len(current_buttons[active]['text']) < 7:
        current_buttons[active]['text'] += event.unicode

def handle_mouse_click(pos):
    # Handle mouse clicks
    # Check input buttons
    clicked_btn = None
    for btn_id, btn_data in SCREEN['buttons'].items():
        btn_rect = pygame.Rect(0, 0, *BTN_SIZE)
        btn_rect.center = btn_data['pos']
        if btn_rect.collidepoint(pos):
            clicked_btn = btn_id
            break
    
    set_active_btn(clicked_btn)

# ============================================================================
# SCREEN MANAGEMENT FUNCTIONS
# ============================================================================

def render_current_screen(screen, font):
    active = get_active_btn()
    
    # Clear the screen and draw the background and title of the screen
    clear_screen(screen)
    draw_title(screen, font, SCREEN['title'])
    
    # Draw the appropriate buttons
    for btn_id, btn_data in SCREEN['buttons']:
        draw_btn(screen, font, btn_id)

def update_display(screen):
    # Update the display
    pygame.display.update()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def initialise_pygame():
    # Initialise pygame and return screen, clock, font
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 70)
    return screen, clock, font

def handle_events():
    # Handle all pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            handle_text_input(event)

def main():
    # Main game loop
    screen, clock, font = initialise_pygame()
    
    while True:
        handle_events()
        render_current_screen(screen, font)
        update_display(screen)
        clock.tick(FPS)

# Run the main game loop
main()
"""