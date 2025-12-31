import pygame
import sys
import threading
from configuration import *
from simulation import simulation

def progress_callback(current_second, total_runtime, standard_data, adaptive_data):
    # callback function that updates the simulation state
    simulation_state.update({
        'current_second': current_second,
        'total_runtime': total_runtime,
        'standard_results': standard_data,
        'adaptive_results': adaptive_data
    })
    
def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZES['title'])
    
    active_btn = None
    current_screen = 'main_menu'
    
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
        active_btn, current_screen = handleevents(active_btn, current_screen, screen_data)
        renderscreen(screen, font, active_btn, current_screen, screen_data)
        clock.tick(FPS)