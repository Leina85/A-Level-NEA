import pygame

# Standard button function
def standard_btn(width, height, center, active, user_text, standard_button_key, btn_color_active, btn_color_passive, screen, base_font, text_color):
    # Create the button
    button_rect = pygame.Rect(0, 0, width, height)
    button_rect.center = center

    # Determine button color
    btn_color = btn_color_active if active else btn_color_passive
    pygame.draw.rect(screen, btn_color, button_rect)

    # Display placeholder or user input
    if user_text == '' and not active:
        text_surf = base_font.render(str(standard_button_key), True, text_color)
    else:
        text_surf = base_font.render(user_text, True, text_color)

    # Center the text vertically
    text_rect = text_surf.get_rect(midleft=(button_rect.x + 5, button_rect.centery))
    screen.blit(text_surf, text_rect)

    return button_rect