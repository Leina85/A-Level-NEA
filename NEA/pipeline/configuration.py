# screen constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# pore grid constants
GRID_SIZE = 10
SQUARE_SIZE = 35
SQUARE_GAP = 2

COLOURS = {
    'btnactive': '#4A7090',
    'btnpassive': '#86A6C1',
    'navbtn': '#2E5266',
    'background': '#F2F2F2',
    'text': '#F2F2F2',
    'title': '#333333',
    'sequencing': '#AFD9AE',
    'idle': '#FFC107',
    'dead': '#F88378',
    'outline': '#000000'
}

# font size constants
FONT_SIZES = {
    'title': 70,
    'nav': 70,
    'help': 28,
    'button_small': 36,
    'button_large': 50,
    'display': 36,
    'result': 35,
    'grid_title': 40,
    'summary': 28
}

DEFAULT_BTN_SIZE = (240, 64)
NAV_BTN_SIZE = (240, 70)
MAIN_BTN_SIZE = (300, 80)

SCREENS = {
    'main_menu': {
        'title': 'Main Menu',
        'buttons': {
            'start': {'pos': (640, 360), 'text': 'Start', 'target': 'input_menu', 'size': MAIN_BTN_SIZE, 'font_size': 'button_large'},
            'help': {'pos': (1130, 60), 'text': 'Help', 'size': NAV_BTN_SIZE, 'colour': 'navbtn', 'dropdown': True},
            'help1': {'pos': (1130, 135), 'text': 'What is Nanopore\nSequencing?', 'target': 'help_menu_1', 'size': NAV_BTN_SIZE, 'colour': 'navbtn', 'hidden': True},
            'help2': {'pos': (1130, 210), 'text': 'What Values\nShould I input?', 'target': 'help_menu_2', 'size': NAV_BTN_SIZE, 'colour': 'navbtn', 'hidden': True}
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
            1: {'pos': (640, 240), 'text': '', 'size': MAIN_BTN_SIZE, 'input': True, 'label': 'Runtime (s)'},
            2: {'pos': (640, 340), 'text': '', 'size': MAIN_BTN_SIZE, 'input': True, 'label': 'Average Molecule\nLength (Kb)'},
            3: {'pos': (640, 440), 'text': '', 'size': MAIN_BTN_SIZE, 'input': True, 'label': 'Fraction of Bases\nTarget (Percentage)', 'max_length': 2},
            'default_values': {'pos': (640, 540), 'text': 'Apply Default Values', 'size': MAIN_BTN_SIZE},
            'start': {'pos': (640, 640), 'text': 'Start', 'target': 'start_menu', 'size': MAIN_BTN_SIZE}
        }
    },
    'start_menu': {
        'title': 'Start Menu',
        'display_text': '',
        'simulation_results': None,
        'simulation_running': False,
        'current_second': 0,
        'total_runtime': 0
    }
}