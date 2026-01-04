import pygame
import sys
import threading
from configuration import *
from simulation import simulation
from analytics import *

def progress_callback(current_second, total_runtime, standard_data, adaptive_data, simulation_state, graph_data, screen_data):
    # callback function that updates the simulation state
    simulation_state.update({
        'current_second': current_second,
        'total_runtime': total_runtime,
        'standard_results': standard_data,
        'adaptive_results': adaptive_data
    })
    
    add_data_point(graph_data, current_second, standard_data, adaptive_data)
    screen_data['graph_menu']['graph_surfaces'] = display_graph(graph_data, simulation_state['total_runtime'])
    
def run_simulation_thread(runtime, avg_molecule_length, target_fraction, screen_data, simulation_state, graph_data):
    simulation_state['running'] = True
    
    # run simulation and capture results
    result = simulation(runtime, avg_molecule_length, target_fraction, progress_callback, simulation_state, graph_data, screen_data)
    
    # store final results
    screen_data['grid_menu']['simulation_results'] = {
        'standard': result[0],
        'adaptive': result[1]
    }
    
    # always reset running state
    simulation_state['running'] = False

def draw_pore_grid(screen, flow_cell, x_start, y_start, title):
    # draw a 10x10 grid representing pore states
    title_font = pygame.font.Font(None, FONT_SIZES['grid_title'])
    
    # draw title above grid
    title_surf = title_font.render(title, True, pygame.Color(COLOURS['title']))
    title_rect = title_surf.get_rect(center=(x_start + (GRID_SIZE * (SQUARE_SIZE + SQUARE_GAP)) // 2, y_start - 30))
    screen.blit(title_surf, title_rect)
    
    # draw 10x10 grid
    for i in range(100):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        pore = flow_cell[i]
        
        # determine color based on pore state
        # pore[0] = is_sequencing, pore[1] = idle_seconds_left
        if pore[1] == 0:
            # dead
            color = pygame.Color(COLOURS['dead'])
        elif pore[0]: 
            # sequencing
            color = pygame.Color(COLOURS['sequencing'])
        else:
            # idle
            color = pygame.Color(COLOURS['idle'])
        
        # calculate position
        x = x_start + col * (SQUARE_SIZE + SQUARE_GAP)
        y = y_start + row * (SQUARE_SIZE + SQUARE_GAP)
        
        # draw filled square
        pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        
        # draw border
        pygame.draw.rect(screen, pygame.Color('#333333'), (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)

def handleevents(active_btn, current_screen, screen_data, simulation_state, graph_data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            screen_info = screen_data[current_screen]
            
            # check navigation button
            if 'navbtn' in screen_info:
                # set nav button position based on current screen
                if current_screen == 'grid_menu':
                    navbtn_rect = pygame.Rect(SCREEN_WIDTH - NAV_BTN_SIZE[0] - 30, SCREEN_HEIGHT - NAV_BTN_SIZE[1] - 30, *NAV_BTN_SIZE)
                elif current_screen == 'graph_menu':
                    navbtn_rect = pygame.Rect(30, SCREEN_HEIGHT - NAV_BTN_SIZE[1] - 30, *NAV_BTN_SIZE)
                else:
                    navbtn_rect = pygame.Rect(50, 50, *NAV_BTN_SIZE)

                # check if the nav button was clicked
                if navbtn_rect.collidepoint(event.pos):
                    # if going to graph menu, only allow if simulation data exists
                    if screen_info['navbtn']['target'] == 'graph_menu':
                        if simulation_state['standard_results'] is not None and len(graph_data['time_points']) > 0:
                            current_screen = screen_info['navbtn']['target']
                            active_btn = None
                            continue  # skip the rest of the event loop
                    else:
                        current_screen = screen_info['navbtn']['target']
                        active_btn = None
                        continue  # skip the rest of the event loop
            
            # check screen buttons
            if 'buttons' in screen_info:
                for btn_key, btn_data in screen_info['buttons'].items():
                    # skip hidden buttons
                    if btn_data.get('hidden') and not screen_info.get('dropdown_open'):
                        continue
                    
                    btnrect = pygame.Rect(0, 0, *btn_data['size'])
                    btnrect.center = btn_data['pos']
                    
                    if btnrect.collidepoint(event.pos):
                        # handle dropdown toggle
                        if btn_data.get('dropdown'):
                            screen_info['dropdown_open'] = not screen_info.get('dropdown_open', False)
                            active_btn = None
                            break
                        
                        # handle navigation (including Start button)
                        if 'target' in btn_data:
                            # check if Start button and validate inputs
                            if btn_key == 'start' and current_screen == 'input_menu':
                                # check if all input fields have values
                                input_menu = screen_data['input_menu']
                                all_filled = True
                                
                                # check all input fields are filled
                                # underscore used here as the other piece of data in the pair is not used but required for the loop syntax
                                for _, data in input_menu['buttons'].items():
                                    if data.get('input') and not data['text']:
                                        all_filled = False
                                        break
                                
                                # only proceed if all inputs are filled
                                if not all_filled:
                                    break
                                
                                # save inputs to variables usable in the backend simulation
                                runtime = int(input_menu['buttons'][1]['text'])
                                avg_molecule_length = int(input_menu['buttons'][2]['text'])
                                target_fraction = int(input_menu['buttons'][3]['text'])
                                
                                # create display text
                                display_text = f"Runtime: {runtime} s\n"
                                display_text += f"Avg Molecule Length: {avg_molecule_length} Kb\n"
                                display_text += f"Target Fraction: {target_fraction}%\n\n"
                                display_text += "Simulation Running..."
                                
                                screen_data['grid_menu']['display_text'] = display_text
                                
                                # Start simulation in separate thread
                                sim_thread = threading.Thread(
                                    target=run_simulation_thread,
                                    args=(runtime, avg_molecule_length, target_fraction, screen_data, simulation_state, graph_data)
                                )
                                sim_thread.daemon = True
                                sim_thread.start()
                            
                            current_screen = btn_data['target']
                            active_btn = None
                            if 'dropdown_open' in screen_info:
                                screen_info['dropdown_open'] = False
                            break
                        
                        # handle default values button
                        if btn_key == 'default_values':
                            # runtime (2hrs)
                            screen_info['buttons'][1]['text'] = '7200'
                            # avg molecule length (10,000 bases)
                            screen_info['buttons'][2]['text'] = '10000'
                            # percentage of target bases (5%)
                            screen_info['buttons'][3]['text'] = '5'
                            active_btn = None
                            break
                        
                        if btn_key == 'toggle' and current_screen == 'graph_menu':
                            if not screen_info['show_graph_4']:
                                screen_info['show_graph_4'] = True
                                btn_data['text'] = 'Adaptive'
                            else:
                                screen_info['show_graph_4'] = False
                                btn_data['text'] = 'Standard'
                            break
                            
                        # handle input buttons
                        if btn_data.get('input'):
                            active_btn = btn_key
                            break
            
        elif event.type == pygame.KEYDOWN and active_btn:
            screen_info = screen_data[current_screen]
            if 'buttons' in screen_info and active_btn in screen_info['buttons']:
                btn_data = screen_info['buttons'][active_btn]
                if btn_data.get('input'):
                    current_text = btn_data['text']
                    max_length = btn_data.get('max_length', 6)
                    
                    if event.key == pygame.K_BACKSPACE:
                        btn_data['text'] = current_text[:-1]
                    elif event.unicode.isdigit() and len(current_text) < max_length:
                        btn_data['text'] = current_text + event.unicode

    return active_btn, current_screen

def renderscreen(screen, font, activebtn, current_screen, screen_data, simulation_state, graph_data):
    # clear screen
    screen.fill(COLOURS['background'])
    screen_info = screen_data[current_screen]
    
    # draw title
    title_surf = font.render(screen_data[current_screen]['title'], True, COLOURS['title'])
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)
    
    # draw navigation button
    if 'navbtn' in screen_info:
        nav_font = pygame.font.Font(None, FONT_SIZES['nav'])
        
        if current_screen == 'grid_menu':
            navbtn_rect = pygame.Rect(SCREEN_WIDTH - NAV_BTN_SIZE[0] - 30, SCREEN_HEIGHT - NAV_BTN_SIZE[1] - 30, *NAV_BTN_SIZE)
        elif current_screen == 'graph_menu':
            navbtn_rect = pygame.Rect(30, SCREEN_HEIGHT - NAV_BTN_SIZE[1] - 30, *NAV_BTN_SIZE)
        else:
            navbtn_rect = pygame.Rect(50, 50, *NAV_BTN_SIZE)
            
        pygame.draw.rect(screen, COLOURS['navbtn'], navbtn_rect)
        textsurf = nav_font.render(screen_info['navbtn']['text'], True, COLOURS['text'])
        textrect = textsurf.get_rect(center=navbtn_rect.center)
        screen.blit(textsurf, textrect)
        
    # draw help text
    if 'help_text' in screen_info:
        help_font = pygame.font.Font(None, FONT_SIZES['help'])
        words = screen_info['help_text'].split(' ')
        lines = []
        current_line = []
        max_width = SCREEN_WIDTH - 20
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = help_font.render(test_line, True, COLOURS['title'])
            if test_surf.get_width() <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        
        y_offset = 180  # Moved up from 250
        for line in lines:
            line_surf = help_font.render(line, True, COLOURS['title'])
            line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(line_surf, line_rect)
            y_offset += 40  # Reduced from 50 to 40

    # draw display text and simulation results on grid
    if current_screen == 'grid_menu':
        display_font = pygame.font.Font(None, FONT_SIZES['display'])
        y_offset = 200
        
        # show input parameters
        if 'display_text' in screen_info and screen_info['display_text']:
            text_lines = screen_info['display_text'].split('\n')
            
            for line in text_lines[:4]:  # First 4 lines are parameters + status
                line_surf = display_font.render(line, True, COLOURS['title'])
                line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(line_surf, line_rect)
                y_offset += 60
    
        # show real-time progress if simulation is running
        if simulation_state['running'] or simulation_state['standard_results'] is not None:
            y_offset += 20
            
            # Progress indicator
            if simulation_state['running']:
                progress_text = f"Progress: {simulation_state['current_second']}/{simulation_state['total_runtime']} seconds"
                progress_surf = display_font.render(progress_text, True, COLOURS['title'])
                progress_rect = progress_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(progress_surf, progress_rect)
                y_offset += 170
                
                # Progress bar
                bar_width = 600
                bar_height = 30
                bar_x = (SCREEN_WIDTH - bar_width) // 2
                bar_y = y_offset
                
                # Background bar
                pygame.draw.rect(screen, COLOURS['btnpassive'], (bar_x, bar_y, bar_width, bar_height))
                
                # Progress bar
                if simulation_state['total_runtime'] > 0:
                    progress = simulation_state['current_second'] / simulation_state['total_runtime']
                    fill_width = int(bar_width * progress)
                    pygame.draw.rect(screen, COLOURS['btnactive'], (bar_x, bar_y, fill_width, bar_height))
                
                y_offset += 60
            else:
                complete_text = "Simulation Complete!"
                complete_surf = display_font.render(complete_text, True, COLOURS['title'])
                complete_rect = complete_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(complete_surf, complete_rect)
                y_offset += 60
        
            # display current pore data as grids
            if simulation_state['standard_results'] is not None and simulation_state['adaptive_results'] is not None:
                y_offset += 20
                
                # Calculate grid positions (side by side)
                grid_total_width = GRID_SIZE * (SQUARE_SIZE + SQUARE_GAP)
                # space between grids
                spacing = 500
                
                # Margine from left
                std_x = (SCREEN_WIDTH // 2) - grid_total_width - (spacing // 2)
                # Margin from right
                adp_x = (SCREEN_WIDTH // 2) + (spacing // 2)
                
                y_pos = 150
                
                # draw both grids
                draw_pore_grid(screen, simulation_state['standard_results'], std_x, y_pos, "Standard Pores")
                draw_pore_grid(screen, simulation_state['adaptive_results'], adp_x, y_pos, "Adaptive Pores")
                
                # calculate summary statistics across ALL pores
                standard_flow_cell = simulation_state['standard_results']
                adaptive_flow_cell = simulation_state['adaptive_results']
                
                # initialize counters
                std_total_bases = 0
                std_target_bases = 0
                std_sequencing_count = 0
                std_idle_count = 0
                std_dead_count = 0
                
                adp_total_bases = 0
                adp_target_bases = 0
                adp_sequencing_count = 0
                adp_idle_count = 0
                adp_dead_count = 0
                
                # sum up statistics for standard pores
                for i in range(100):
                    pore = standard_flow_cell[i]
                    std_total_bases += pore[3]  # total bases sequenced
                    std_target_bases += pore[4]  # target bases sequenced
                    
                    # count pore states
                    if pore[1] == 0:  # dead
                        std_dead_count += 1
                    elif pore[0]:  # sequencing
                        std_sequencing_count += 1
                    else:  # idle
                        std_idle_count += 1
                
                # sum up statistics for adaptive pores
                for i in range(100):
                    pore = adaptive_flow_cell[i]
                    adp_total_bases += pore[3]  # total bases sequenced
                    adp_target_bases += pore[4]  # target bases sequenced
                    
                    # count pore states
                    if pore[1] == 0:  # dead
                        adp_dead_count += 1
                    elif pore[0]:  # sequencing
                        adp_sequencing_count += 1
                    else:  # idle
                        adp_idle_count += 1
                
                # display summary statistics
                summary_font = pygame.font.Font(None, FONT_SIZES['summary'])
                
                # helper function to draw centered text
                def draw_text(text, centre_x, y):
                    surf = summary_font.render(text, True, COLOURS['title'])
                    screen.blit(surf, surf.get_rect(center=(centre_x, y)))

                grid_height = GRID_SIZE * (SQUARE_SIZE + SQUARE_GAP)
                summary_start_y = y_pos + grid_height + 30

                std_center_x = std_x + grid_total_width // 2 + 115
                adp_center_x = adp_x + grid_total_width // 2 - 115

                std_y = summary_start_y
                adp_y = summary_start_y

                # standard pores summary
                draw_text(f"Standard - Total Bases: {std_total_bases:,} | Target Bases: {std_target_bases:,}", std_center_x, std_y)
                std_y += 35
                draw_text(f"Standard - Sequencing: {std_sequencing_count} | Idle: {std_idle_count} | Dead: {std_dead_count}", std_center_x, std_y)

                # Adaptive pores summary
                draw_text(f"Adaptive - Total Bases: {adp_total_bases:,} | Target Bases: {adp_target_bases:,}", adp_center_x, adp_y)
                adp_y += 35
                draw_text(f"Adaptive - Sequencing: {adp_sequencing_count} | Idle: {adp_idle_count} | Dead: {adp_dead_count}", adp_center_x, adp_y)

    # draw display text and simulation results on graphs
    if current_screen == 'graph_menu':
        
        #call the display_graph function to create images for the graphs
        analytics_graphs = screen_data['graph_menu']['graph_surfaces']
        
        # display all three graphs
        if analytics_graphs:
            screen.blit(analytics_graphs[0], (50, 150))
            screen.blit(analytics_graphs[1], (455, 150))
            screen.blit(analytics_graphs[2], (860, 150))
        
    # draw buttons
    if 'buttons' in screen_info:
        button_font = pygame.font.Font(None, FONT_SIZES['button_small'])
        for btn_key, btn_data in screen_info['buttons'].items():
            # Skip hidden buttons
            if btn_data.get('hidden') and not screen_info.get('dropdown_open'):
                continue
            
            isactive = (activebtn == btn_key)
            
            # determine button colour
            if btn_data.get('colour'):
                colour = COLOURS[btn_data['colour']]
            elif isactive:
                colour = COLOURS['btnactive']
            else:
                colour = COLOURS['btnpassive']
            
            # draw button
            rect = pygame.Rect(0, 0, *btn_data['size'])
            rect.center = btn_data['pos']
            pygame.draw.rect(screen, colour, rect)
            
            # Use custom font size if specified, otherwise use default
            if btn_data.get('font_size'):
                current_button_font = pygame.font.Font(None, FONT_SIZES[btn_data['font_size']])
            else:
                current_button_font = button_font
            
            # draw button text
            if btn_data.get('input'):
                if btn_data['text'] or isactive:
                    displaytext = btn_data['text']
                else:
                    displaytext = btn_data.get('label', str(btn_key))
            else:
                displaytext = btn_data['text']
            
            # Handle multi-line text
            if '\n' in displaytext:
                lines = displaytext.split('\n')
                line_spacing = 28
                total_height = len(lines) * line_spacing
                start_y = rect.centery - (total_height // 2) + (line_spacing // 2) - 2
                
                for i, line in enumerate(lines):
                    textsurf = current_button_font.render(line, True, COLOURS['text'])
                    textrect = textsurf.get_rect(center=(rect.centerx, start_y + i * line_spacing))
                    screen.blit(textsurf, textrect)
            else:
                textsurf = current_button_font.render(displaytext, True, COLOURS['text'])
                textrect = textsurf.get_rect(center=rect.center)
                screen.blit(textsurf, textrect)
            
            # Draw black outline for nav buttons (help dropdown buttons)
            if btn_data.get('colour') == 'navbtn':
                pygame.draw.rect(screen, COLOURS['outline'], rect, 3)
    
    pygame.display.update()
    
def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZES['title'])
    
    active_btn = None
    current_screen = 'main_menu'
    
    simulation_state = {
    'running': False,
    'current_second': 0,
    'total_runtime': 0,
    'standard_results': None,
    'adaptive_results': None
    }
    
    graph_data = {
        'time_points': [],
        'std_total_bases': [],
        'std_target_bases': [],
        'adp_total_bases': [],
        'adp_target_bases': [],
        'std_dead_pores': [],
        'adp_dead_pores': [],
        'std_sequencing_pores': [],
        'adp_sequencing_pores': [],
        'std_idle_pores': [],
        'adp_idle_pores': [],
    }
    
    # deep copy screen data
    screen_data = {}
    for screenid, screen_info in SCREENS.items():
        screen_data[screenid] = {'title': screen_info['title']}
        
        for key in ['navbtn', 'help_text', 'dropdown_open', 'display_text', 'simulation_results', 'simulation_running', 'current_second', 'total_runtime']:
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
    
    # main game loop
    while True:
        active_btn, current_screen = handleevents(active_btn, current_screen, screen_data, simulation_state, graph_data)
        renderscreen(screen, font, active_btn, current_screen, screen_data, simulation_state, graph_data)
        clock.tick(FPS)