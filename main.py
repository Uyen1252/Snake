import pygame
import sys
import numpy as np
from config import *
from game_objects import MainGame, Button
    
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    main = MainGame()
    
    stop_text = pygame.font.SysFont('Corbel', GRID_SIZE).render('STOP', True, WHITE)
    continue_text = pygame.font.SysFont('Corbel', GRID_SIZE).render('CONTINUE', True, WHITE)

    start_btn = Button([22, 6, 6, 2], 'START', pygame.font.SysFont('Corbel', GRID_SIZE), [23.8, 6.5])
    quit_btn = Button([22, 9, 6, 2], 'QUIT', pygame.font.SysFont('Corbel', GRID_SIZE), [23.8, 9.5])
    stop_btn = Button([22, 6, 6, 2], 'STOP', pygame.font.SysFont('Corbel', GRID_SIZE), [23.8, 6.5])
    continue_btn = Button([22, 6, 6, 2], 'CONTINUE', pygame.font.SysFont('Corbel', GRID_SIZE), [22.8, 6.5])
    back_btn = Button([22, 9, 6, 2], 'BACK', pygame.font.SysFont('Corbel', GRID_SIZE), [23.8, 9.5])
    self_play_btn = Button([24, 3, 5, 1.5], 'Self-play', pygame.font.SysFont('Corbel', 16), [25.1, 3.4])
    auto_play_btn = Button([24, 3, 5, 1.5], 'Auto-play', pygame.font.SysFont('Corbel', 16), [24.9, 3.4])

    case = 0
    key = None
    play_mode = 'self'

    while True:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BROWN, GRID_SIZE * np.array([20, 0, 10, 20]))
        
        # Display score --------------------------
        score_text = pygame.font.Font(None, 36).render(f"Score: {main.score}", True, GREEN)
        screen.blit(score_text, GRID_SIZE * np.array([22, 1]))
        
        # get mouse's position ------------------
        mouse_pos = pygame.mouse.get_pos()

        # draw button ---------------------------
        if case == 0:
            start_btn.draw(screen, mouse_pos)
            quit_btn.draw(screen, mouse_pos)
        if case == 1:
            stop_btn.draw(screen, mouse_pos)
        if case == 2:
            continue_btn.draw(screen, mouse_pos)

        if case in [1, 2]:
            back_btn.draw(screen, mouse_pos)
            
            mode_text = pygame.font.Font(None, 20).render("Mode", True, WHITE)
            screen.blit(mode_text, GRID_SIZE * np.array([22, 3.4]))
            if play_mode == 'self':
                self_play_btn.draw(screen, mouse_pos)
            else:
                auto_play_btn.draw(screen, mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                case = 1
                key = event.key
                if event.key in [ord('s'), ord('S')]:
                    play_mode = 'self'
                if event.key in [ord('a'), ord('A')]:
                    play_mode = 'auto'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if case == 0:
                    if start_btn.is_hover(mouse_pos):
                        case = 1
                    if quit_btn.is_hover(mouse_pos):
                        pygame.quit()
                        sys.exit()
                elif case == 1:
                    if stop_btn.is_hover(mouse_pos):
                        case = 2
                    if back_btn.is_hover(mouse_pos):
                        case = 0
                        play_mode = 'self'
                        main.reset()
                elif case == 2:
                    if continue_btn.is_hover(mouse_pos):
                        case = 1
                
                if case in [1, 2]:
                    if self_play_btn.is_hover(mouse_pos):
                        play_mode = 'self' if play_mode != 'self' else 'auto'
                    elif auto_play_btn.is_hover(mouse_pos):
                        play_mode = 'auto' if play_mode != 'auto' else 'self'
                    
                    if back_btn.is_hover(mouse_pos):
                        case = 0
                        play_mode = 'self'
                        main.reset()
        
        if case == 1:
            if play_mode == 'auto':
                main.auto_play()
            else:
                main.self_play(key)
                key = None
            main.update()

            if main.check_gameover():
                case = 0
                play_mode = 'self'
                main.reset()
        
        main.draw_elements(screen)

        # update display
        pygame.display.update()
        clock.tick(FPS)
