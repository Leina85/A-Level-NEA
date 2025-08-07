import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode([1280, 720])
base_font = pygame.font.Font(None, 70)
user_text = ''

# Colours
screen_colour = pygame.Color('#F2F2F2')
btn_colour_active = pygame.Color('#4A7090')
btn_colour_passive = pygame.Color('#86A6C1')
btn_colour = btn_colour_passive

rect_width = 210
rect_height = 64

input_rect = pygame.Rect(0, 0, rect_width, rect_height)
input_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

active = False

while True:
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                    
        if event.type == pygame.KEYDOWN and active == True:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]

            elif event.unicode.isdigit() and len(user_text) < 7:
                user_text += event.unicode

            elif event.key == pygame.K_RETURN and len(user_text) > 0:
                print("User input:", user_text)
    
    # Set background color
    screen.fill(screen_colour)

    # Change color if the input box is active
    if active:
        btn_colour = btn_colour_active
    else:
        btn_colour = btn_colour_passive
        
    if user_text == '' and not active:
        text_surface = base_font.render('Input', True, ('#F2F2F2'))  # Show "Input" when inactive
    else:
        text_surface = base_font.render(user_text, True, ('#F2F2F2'))  # Show user text when active

    # Show button and update screen
    pygame.draw.rect(screen, btn_colour, input_rect)
    
    # Center the text within the input box
    text_rect = text_surface.get_rect(center=input_rect.center)
    screen.blit(text_surface, text_rect)

    pygame.display.update()

    clock.tick(60)


