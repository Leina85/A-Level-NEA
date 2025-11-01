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

INP_BTN_SIZE = (240, 64)
NAV_BTN_SIZE = (200, 60)

SCREENS = {
    0: {
        'title': 'Input Screen',
        'navbtn': {'text': 'InpScreen', 'target': 1},
        'buttons': {
            1: {'pos': (640, 260), 'text': ''},
            2: {'pos': (640, 360), 'text': ''},
            3: {'pos': (640, 460), 'text': ''}
        }
    },
    1: {
        'title': 'Main Screen',
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

def handleevents(activebtn, current_screen, screendata):
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
                current_screen = screendata[current_screen]['navbtn']['target']
                activebtn = None
                continue
            
            # Check which input button was clicked
            clickedbtn = None
            for inp_btn_key, inp_btn_data in screendata[current_screen]['buttons'].items():
                btnrect = pygame.Rect(0, 0, *INP_BTN_SIZE)
                btnrect.center = inp_btn_data['pos']
                if btnrect.collidepoint(event.pos):
                    clickedbtn = inp_btn_key
                    break
            activebtn = clickedbtn
            
        elif event.type == pygame.KEYDOWN and activebtn:
            # Handle text input for active button
            currenttext = screendata[current_screen]['buttons'][activebtn]['text']
            
            if event.key == pygame.K_BACKSPACE:
                # Remove last character
                screendata[current_screen]['buttons'][activebtn]['text'] = currenttext[:-1]
            elif event.key == pygame.K_RETURN and currenttext:
                # Print input when Enter is pressed
                screen_name = screendata[current_screen]['title']
                print(f"Input for button {activebtn} on {screen_name}: {currenttext}")
            elif event.unicode.isdigit() and len(currenttext) < 7:
                # Add digit to text (maximum 7 digits)
                screendata[current_screen]['buttons'][activebtn]['text'] = currenttext + event.unicode
    
    return activebtn, current_screen

def drawnavbtn(screen, font, rect, text):
    # Draw navigation button rectangle
    pygame.draw.rect(screen, COLOURS['navbtn'], rect)
    # Render and centre text on button
    textsurf = font.render(text, True, COLOURS['text'])
    textrect = textsurf.get_rect(center=rect.center)
    screen.blit(textsurf, textrect)

def renderscreen(screen, font, activebtn, current_screen, screendata):
    # Clear screen with background colour
    screen.fill(COLOURS['background'])
    
    # Draw navigation button
    navbtn_rect = pygame.Rect(50, 50, *NAV_BTN_SIZE)
    drawnavbtn(screen, font, navbtn_rect, screendata[current_screen]['navbtn']['text'])
    
    # Draw screen title
    titlesurf = font.render(screendata[current_screen]['title'], True, COLOURS['title'])
    titlerect = titlesurf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(titlesurf, titlerect)
    
    # Draw all input buttons for current screen
    for inp_btn_key, inp_btn_data in screendata[current_screen]['buttons'].items():
        isactive = (activebtn == inp_btn_key)
        
        # Draw button rectangle with appropriate colour
        rect = pygame.Rect(0, 0, *INP_BTN_SIZE)
        rect.center = inp_btn_data['pos']
        colour = COLOURS['btnactive'] if isactive else COLOURS['btnpassive']
        pygame.draw.rect(screen, colour, rect)
        
        # Draw button text (show button number if empty and inactive)
        displaytext = inp_btn_data['text'] if inp_btn_data['text'] or isactive else str(inp_btn_key)
        textsurf = font.render(displaytext, True, COLOURS['text'])
        textrect = textsurf.get_rect(midleft=(rect.x + 5, rect.centery))
        screen.blit(textsurf, textrect)
    
    # Update display
    pygame.display.update()

def main():
    # Initialise Pygame
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 70)
    
    # Initialise local state
    activebtn = None
    current_screen = 1
    
    # Copy screen data to preserve changes made by user
    screendata = {}
    for screenid, screeninfo in SCREENS.items():
        screendata[screenid] = {
            'title': screeninfo['title'],
            'navbtn': screeninfo['navbtn'].copy(),
            'buttons': {k: v.copy() for k, v in screeninfo['buttons'].items()}
        }
    
    # Main game loop
    while True:
        activebtn, current_screen = handleevents(activebtn, current_screen, screendata)
        renderscreen(screen, font, activebtn, current_screen, screendata)
        clock.tick(FPS)

# ============================================================================
# RUN APPLICATION
# ============================================================================

main()