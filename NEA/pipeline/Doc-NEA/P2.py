# ============================================================================
# CONFIGURATION
# ============================================================================

import pygame
import sys
from P1 import simulation

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
            'help1': {'pos': (1130, 120), 'text': 'What is Nanopore Sequencing?', 'target': 'help_menu_1', 'size': NAV_BTN_SIZE, 'colour': 'navbtn', 'hidden': True},
            'help2': {'pos': (1130, 180), 'text': 'What Values Should I input?', 'target': 'help_menu_2', 'size': NAV_BTN_SIZE, 'colour': 'navbtn', 'hidden': True}
        },
        'dropdown_open': False
    },
    'help_menu_1': {
        'title': 'Help Menu - Page 1',
        'navbtn': {'text': 'Back', 'target': 'main_menu'},
        'help_text': 'Nanopore sequencing is the process of finding the base sequence of DNA; DNA is made of repeating units called nucleotides which have bases A, T, G and C. This is useful, as knowing the base sequence can help identify a sample, find mutations and study genomes. Nanopore sequencing uses an artificial membrane containing channels called nanopores. An electric current flows through each nanopore. A single strand of DNA is passed through a nanopore, and the base sequence disrupts the current. This is recorded in real time and the disruption is measured to find the base sequence (each base disrupts the current differently). This DNA sequencing method is the only one that produces data in real time. There are two types of nanopore DNA sequencing, adaptive and standard. Standard has each pore process a complete molecule of DNA before moving onto the next, meaning pores are rarely idle and there is a large amount of data at the end of the run. Adaptive sequencing has each pore process a molecule of DNA for a set period to identify if it is on target or not (in some sequencing runs there are specific genes that the scientist is looking for data on). If the DNA is identified as on target, then the molecule is fully sequenced; however, if the DNA is identified as non-target, then the molecule is ejected to make way for another. Adaptive sequencing can result in more data on target, but less total data in comparison to standard sequencing. Numerous factors affect which method is better for a particular experiment. My simulation will take these factors into account to give an exact estimation of the data outputs from both methods, allowing a scientist to select the most appropriate sequencing method for their sample.'
    },
    'help_menu_2': {
        'title': 'Help Menu - Page 2',
        'navbtn': {'text': 'Back', 'target': 'main_menu'},
        'help_text': 'In this Simulation, there are three variables: Average Molecule Length; Sequencing Rate; and Runtime. Average Molecule Length refers to the mean length of the DNA molecules that pass through pores. It is measured in Kilobases (Kb), One Kilobase is one thousand bases. Sequencing rate is the number of bases a pore can sequence each second. It is measured in bases per second (Bps) and the standard rate of sequencing for nanopore sequencing is 450 Bps. Runtime is how many virtual seconds the simulation will run for (this is not how long the simulation will take to run). Too small values will generate very little data, but after too much time, the pores will die. If you are not sure, press the apply default values button to use predetermined values and see what happens!'
    },
    'input_menu': {
        'title': 'Input Menu',
        'navbtn': {'text': 'Back', 'target': 'main_menu'},
        'buttons': {
            1: {'pos': (640, 260), 'text': '', 'size': MAIN_BTN_SIZE, 'input': True, 'label': 'Runtime (s)'},
            2: {'pos': (640, 360), 'text': '', 'size': MAIN_BTN_SIZE, 'input': True, 'label': 'Average Molecule Length (Kb)'},
            3: {'pos': (640, 460), 'text': '', 'size': MAIN_BTN_SIZE, 'input': True, 'label': 'Fraction of Bases Target (Decimal)', 'max_length': 2},
            'default_values': {'pos': (640, 560), 'text': 'Apply Default Values', 'size': MAIN_BTN_SIZE},
            'start': {'pos': (640, 650), 'text': 'Start', 'target': 'start_menu', 'size': MAIN_BTN_SIZE}
        }
    },
    'start_menu': {
        'title': 'Start Menu',
        'display_text': '',
        'simulation_results': None
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
                        
                        # Handle navigation (including Start button)
                        if 'target' in btn_data:
                            # Check if Start button and validate inputs
                            if btn_key == 'start':
                                # Check if all input fields have values
                                all_filled = True
                                for key, data in screen_info['buttons'].items():
                                    if data.get('input') and not data['text']:
                                        all_filled = False
                                        break
                                
                                # Only proceed if all inputs are filled
                                if not all_filled:
                                    break
                                
                                # Print all inputs
                                print("\n=== Input Menu Values ===")
                                string_1 = ""
                                for key, data in screen_info['buttons'].items():
                                    if data.get('input'):
                                        label = data.get('label', str(key))
                                        print(f"{label}: {data['text']}")
                                        string_1 += f"{label}: {data['text']}\n"
                                print("=========================\n")
                                
                                # Store string_1 in start_menu for display
                                screen_data['start_menu']['display_text'] = string_1
                            
                            current_screen = btn_data['target']
                            active_btn = None
                            if 'dropdown_open' in screen_info:
                                screen_info['dropdown_open'] = False
                            break
                        
                        # Handle default values button
                        if btn_key == 'default_values':
                            # runtime (2hrs)
                            screen_info['buttons'][1]['text'] = '7200'
                            # avg molecule length (10,000 bases)
                            screen_info['buttons'][2]['text'] = '10000'
                            # percentage of target bases (5%)
                            screen_info['buttons'][3]['text'] = '5'
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
                    max_length = btn_data.get('max_length', 7)
                    
                    if event.key == pygame.K_BACKSPACE:
                        btn_data['text'] = current_text[:-1]
                    elif event.unicode.isdigit() and len(current_text) < max_length:
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
    
    # Draw display text (for start menu)
    if 'display_text' in screen_info and screen_info['display_text']:
        display_font = pygame.font.Font(None, 50)
        text_lines = screen_info['display_text'].strip().split('\n')
        y_offset = 250
        
        for line in text_lines:
            line_surf = display_font.render(line, True, COLOURS['title'])
            line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(line_surf, line_rect)
            y_offset += 60

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
                    displaytext = btn_data.get('label', str(btn_key))
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
        
        for key in ['navbtn', 'help_text', 'dropdown_open', 'display_text']:
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