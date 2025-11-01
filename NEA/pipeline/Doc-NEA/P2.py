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

def handleevents(activebtn, current_screen, screendata):
    # Process all events in the queue
    for event in pygame.event.get():
        # Handle window close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check which button was clicked
            clickedbtn = None
            for btnid, btndata in screendata['buttons'].items():
                btnrect = pygame.Rect(0, 0, *BTN_SIZE)
                btnrect.center = btndata['pos']
                if btnrect.collidepoint(event.pos):
                    clickedbtn = btnid
                    break
            activebtn = clickedbtn
            
        elif event.type == pygame.KEYDOWN and activebtn:
            # Handle text input for active button
            currenttext = screendata['buttons'][activebtn]['text']
            
            if event.key == pygame.K_BACKSPACE:
                screendata['buttons'][activebtn]['text'] = currenttext[:-1]
            elif event.key == pygame.K_RETURN and currenttext:
                print(f"Input for button {activebtn}: {currenttext}")
            elif event.unicode.isdigit() and len(currenttext) < 7:
                screendata['buttons'][activebtn]['text'] = currenttext + event.unicode
    
    return activebtn

def renderscreen(screen, font, activebtn, screendata):
    # Clear screen
    screen.fill(COLOURS['background'])
    
    # Draw title
    titlesurf = font.render(screendata['title'], True, COLOURS['title'])
    titlerect = titlesurf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(titlesurf, titlerect)
    
    # Draw all buttons
    for btnid, btndata in screendata['buttons'].items():
        isactive = (activebtn == btnid)
        
        # Draw button rectangle
        rect = pygame.Rect(0, 0, *BTN_SIZE)
        rect.center = btndata['pos']
        colour = COLOURS['btnactive'] if isactive else COLOURS['btnpassive']
        pygame.draw.rect(screen, colour, rect)
        
        # Draw button text
        displaytext = btndata['text'] if btndata['text'] or isactive else str(btnid)
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
    activebtn = None
    current_screen = 0
    
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