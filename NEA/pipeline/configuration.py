import pygame

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
COLORS = {
    'btn_active': '#4A7090',
    'btn_passive': '#86A6C1',
    'text': '#F2F2F2'
}

# Button dimensions
BTN_SIZE = (240, 64)

# Standard Button position and text to be used in standard_button subroutine
standard_btns = {
    1: {'pos': (640, 260), 'text': ''},
    2: {'pos':  (640, 360), 'text': ''},
    3: {'pos': (640, 460), 'text': ''}
}