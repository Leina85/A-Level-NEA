# ============================================================================
# CONFIGURATION
# ============================================================================

import pygame
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

COLOURS = {
    'btnactive': '#4A7090',
    'btnpassive': '#86A6C1',
    'navbtn': '#2E5266',
    'background': '#F2F2F2',
    'text': '#F2F2F2',
    'title': '#333333'
}

DEFAULT_BTN_SIZE = (240, 64)
NAV_BTN_SIZE = (200, 60)
MAIN_BTN_SIZE = (300, 80)

SCREENS = {
    0: {
        'title': 'Main Screen',
        'navbtn': {'text': 'InpScreen', 'target': 1},
        'buttons': {
            1: {'pos': (640, 260), 'text': ''},
            2: {'pos': (640, 360), 'text': ''},
            3: {'pos': (640, 460), 'text': ''}
        }
    },
    1: {
        'title': 'Input Screen',
        'navbtn': {'text': 'Back', 'target': 0},
        'buttons': {
            1: {'pos': (640, 310), 'text': ''},
            2: {'pos': (640, 410), 'text': ''}
        }
    }
}

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def handleevents(active_btn, current_screen, screen_data):
    # Process all events in the queue
    for event in pygame.event.get():
        # Handle window close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check navigation button
            navbtn_rect = pygame.Rect(50, 50, *NAV_BTN_SIZE)
            if navbtn_rect.collidepoint(event.pos):
                current_screen = screen_data[current_screen]['navbtn']['target']
                active_btn = None
                continue
            
            # Check which input button was clicked
            clicked_btn = None
            for inp_btn_key, inp_btn_data in screen_data[current_screen]['buttons'].items():
                btnrect = pygame.Rect(0, 0, *DEFAULT_BTN_SIZE)
                btnrect.center = inp_btn_data['pos']
                if btnrect.collidepoint(event.pos):
                    clicked_btn = inp_btn_key
                    break
            active_btn = clicked_btn
            
        elif event.type == pygame.KEYDOWN and active_btn:
            # Handle text input for active button
            current_text = screen_data[current_screen]['buttons'][active_btn]['text']
            
            if event.key == pygame.K_BACKSPACE:
                # Remove last character
                screen_data[current_screen]['buttons'][active_btn]['text'] = current_text[:-1]
            elif event.key == pygame.K_RETURN and current_text:
                # Print input when Enter is pressed
                screen_name = screen_data[current_screen]['title']
                print(f"Input for button {active_btn} on {screen_name}: {current_text}")
            elif event.unicode.isdigit() and len(current_text) < 7:
                # Add digit to text (maximum 7 digits)
                screen_data[current_screen]['buttons'][active_btn]['text'] = current_text + event.unicode

    return active_btn, current_screen

def renderscreen(screen, font, activebtn, current_screen, screen_data):
    # Clear screen
    screen.fill(COLOURS['background'])
    
    # Draw title
    title_surf = font.render(screen_data[current_screen]['title'], True, COLOURS['title'])
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)
    
    # Draw navigation button
    navbtn_rect = pygame.Rect(50, 50, *NAV_BTN_SIZE)
    pygame.draw.rect(screen, COLOURS['navbtn'], navbtn_rect)
    textsurf = font.render(screen_data[current_screen]['navbtn']['text'], True, COLOURS['text'])
    textrect = textsurf.get_rect(center=navbtn_rect.center)
    screen.blit(textsurf, textrect)
    
    # Draw all input buttons for current screen
    for inp_btn_key, inp_btn_data in screen_data[current_screen]['buttons'].items():
        isactive = (activebtn == inp_btn_key)
        
        # Draw button rectangle with appropriate colour
        rect = pygame.Rect(0, 0, *DEFAULT_BTN_SIZE)
        rect.center = inp_btn_data['pos']
        colour = COLOURS['btnactive'] if isactive else COLOURS['btnpassive']
        pygame.draw.rect(screen, colour, rect)
        
        # Draw button text (show button number if empty and inactive)
        displaytext = inp_btn_data['text'] if inp_btn_data['text'] or isactive else str(inp_btn_key)
        textsurf = font.render(displaytext, True, COLOURS['text'])
        textrect = textsurf.get_rect(midleft=(rect.x + 5, rect.centery))
        screen.blit(textsurf, textrect)
    
    pygame.display.update()

def main():
    # Initialise Pygame
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 70)
    
    # Initialise local state
    active_btn = None
    current_screen = 0
    
    # Copy screen data to preserve changes made by user
    screen_data = {}
    for screenid, screen_info in SCREENS.items():
        screen_data[screenid] = {
            'title': screen_info['title'],
            'navbtn': screen_info['navbtn'].copy(),
            'buttons': {k: v.copy() for k, v in screen_info['buttons'].items()}
        }
    
    # Main game loop
    while True:
        active_btn, current_screen = handleevents(active_btn, current_screen, screen_data)
        renderscreen(screen, font, active_btn, current_screen, screen_data)
        clock.tick(FPS)

# ============================================================================
# RUN SIMULATION
# ============================================================================

main()