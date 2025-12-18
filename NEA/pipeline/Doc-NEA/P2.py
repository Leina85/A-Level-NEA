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
    'main_menu': {
        'title': 'Main Menu',
        'buttons': {
            'start': {'pos': (640, 360), 'text': 'Start', 'target': 'input_menu', 'size': MAIN_BTN_SIZE},
            'help': {'pos': (1130, 60), 'text': 'Help', 'size': NAV_BTN_SIZE, 'colour': 'navbtn', 'dropdown': True},
            'help1': {'pos': (1130, 120), 'text': 'Help 1', 'target': 'help_menu_1', 'size': NAV_BTN_SIZE, 'colour': 'navbtn', 'hidden': True},
            'help2': {'pos': (1130, 180), 'text': 'Help 2', 'target': 'help_menu_2', 'size': NAV_BTN_SIZE, 'colour': 'navbtn', 'hidden': True}
        },
        'dropdown_open': False
    },
    'help_menu_1': {
        'title': 'Help Menu - Page 1',
        'navbtn': {'text': 'Back', 'target': 'main_menu'},
        'help_text': ''
    },
    'help_menu_2': {
        'title': 'Help Menu - Page 2',
        'navbtn': {'text': 'Back', 'target': 'main_menu'},
        'help_text': ''
    },
    'input_menu': {
        'title': 'Input Menu',
        'navbtn': {'text': 'Back', 'target': 'main_menu'},
        'buttons': {
            1: {'pos': (640, 260), 'text': '', 'size': MAIN_BTN_SIZE, 'input': True},
            2: {'pos': (640, 360), 'text': '', 'size': MAIN_BTN_SIZE, 'input': True},
            3: {'pos': (640, 460), 'text': '', 'size': MAIN_BTN_SIZE, 'input': True},
            'clear': {'pos': (640, 560), 'text': 'Clear All', 'size': MAIN_BTN_SIZE},
            'start': {'pos': (640, 650), 'text': 'Start', 'target': 'start_menu', 'size': MAIN_BTN_SIZE}
        }
    },
    'start_menu': {
        'title': 'Start Menu'
    }
}

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def handleevents(active_btn, current_screen, screen_data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            screen_info = screen_data[current_screen]
            
            # Check navigation button
            if 'navbtn' in screen_info:
                navbtn_rect = pygame.Rect(50, 50, *NAV_BTN_SIZE)
                if navbtn_rect.collidepoint(event.pos):
                    current_screen = screen_info['navbtn']['target']
                    active_btn = None
                    continue
            
            # Check screen buttons
            if 'buttons' in screen_info:
                for btn_key, btn_data in screen_info['buttons'].items():
                    # Skip hidden buttons
                    if btn_data.get('hidden') and not screen_info.get('dropdown_open'):
                        continue
                    
                    btnrect = pygame.Rect(0, 0, *btn_data['size'])
                    btnrect.center = btn_data['pos']
                    
                    if btnrect.collidepoint(event.pos):
                        # Handle dropdown toggle
                        if btn_data.get('dropdown'):
                            screen_info['dropdown_open'] = not screen_info.get('dropdown_open', False)
                            active_btn = None
                            break
                        
                        # Handle navigation
                        if 'target' in btn_data:
                            current_screen = btn_data['target']
                            active_btn = None
                            if 'dropdown_open' in screen_info:
                                screen_info['dropdown_open'] = False
                            break
                        
                        # Handle clear button
                        if btn_key == 'clear':
                            for key, data in screen_info['buttons'].items():
                                if data.get('input'):
                                    data['text'] = ''
                            active_btn = None
                            break
                        
                        # Handle input buttons
                        if btn_data.get('input'):
                            active_btn = btn_key
                            break
            
        elif event.type == pygame.KEYDOWN and active_btn:
            screen_info = screen_data[current_screen]
            if 'buttons' in screen_info and active_btn in screen_info['buttons']:
                btn_data = screen_info['buttons'][active_btn]
                if btn_data.get('input'):
                    current_text = btn_data['text']
                    
                    if event.key == pygame.K_BACKSPACE:
                        btn_data['text'] = current_text[:-1]
                    elif event.key == pygame.K_RETURN and current_text:
                        print(f"Input for button {active_btn} on {screen_info['title']}: {current_text}")
                    elif event.unicode.isdigit() and len(current_text) < 7:
                        btn_data['text'] = current_text + event.unicode

    return active_btn, current_screen

def renderscreen(screen, font, activebtn, current_screen, screen_data):
    # Clear screen
    screen.fill(COLOURS['background'])
    screen_info = screen_data[current_screen]
    
    # Draw title
    title_surf = font.render(screen_data[current_screen]['title'], True, COLOURS['title'])
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)
    
    # Draw navigation button
    if 'navbtn' in screen_info:
        navbtn_rect = pygame.Rect(50, 50, *NAV_BTN_SIZE)
        pygame.draw.rect(screen, COLOURS['navbtn'], navbtn_rect)
        textsurf = font.render(screen_info['navbtn']['text'], True, COLOURS['text'])
        textrect = textsurf.get_rect(center=navbtn_rect.center)
        screen.blit(textsurf, textrect)
        
    # Draw help text
    if 'help_text' in screen_info:
        help_font = pygame.font.Font(None, 40)
        words = screen_info['help_text'].split(' ')
        lines = []
        current_line = []
        max_width = SCREEN_WIDTH - 200
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = help_font.render(test_line, True, COLOURS['title'])
            if test_surf.get_width() <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        
        y_offset = 250
        for line in lines:
            line_surf = help_font.render(line, True, COLOURS['title'])
            line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(line_surf, line_rect)
            y_offset += 50

    # Draw buttons
    if 'buttons' in screen_info:
        for btn_key, btn_data in screen_info['buttons'].items():
            # Skip hidden buttons
            if btn_data.get('hidden') and not screen_info.get('dropdown_open'):
                continue
            
            isactive = (activebtn == btn_key)
            
            # Determine button colour
            if btn_data.get('colour'):
                colour = COLOURS[btn_data['colour']]
            elif isactive:
                colour = COLOURS['btnactive']
            else:
                colour = COLOURS['btnpassive']
            
            # Draw button
            rect = pygame.Rect(0, 0, *btn_data['size'])
            rect.center = btn_data['pos']
            pygame.draw.rect(screen, colour, rect)
            
            # Draw button text
            if btn_data.get('input'):
                if btn_data['text'] or isactive:
                    displaytext = btn_data['text']
                else:
                    displaytext = str(btn_key)
            else:
                displaytext = btn_data['text']
            
            textsurf = font.render(displaytext, True, COLOURS['text'])
            textrect = textsurf.get_rect(center=rect.center)
            screen.blit(textsurf, textrect)
    
    pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 70)
    
    active_btn = None
    current_screen = 'main_menu'
    
    # Deep copy screen data
    screen_data = {}
    for screenid, screen_info in SCREENS.items():
        screen_data[screenid] = {'title': screen_info['title']}
        
        for key in ['navbtn', 'help_text', 'dropdown_open']:
            if key in screen_info:
                screen_data[screenid][key] = screen_info[key] if key != 'navbtn' else screen_info[key].copy()
        
        # check if buttons present on screen
        if 'buttons' in screen_info:
            # empty dict for button copies
            buttons_copy = {}
            # loop through each button
            for k, v in screen_info['buttons'].items():
                # copy and store button data
                button_data_copy = v.copy()
                buttons_copy[k] = button_data_copy
            screen_data[screenid]['buttons'] = buttons_copy  
    
    # Main game loop
    while True:
        active_btn, current_screen = handleevents(active_btn, current_screen, screen_data)
        renderscreen(screen, font, active_btn, current_screen, screen_data)
        clock.tick(FPS)

# ============================================================================
# RUN SIMULATION
# ============================================================================

main()
