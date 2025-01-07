import pygame
from pygame.math import Vector2
import numpy as np
import random as r
from algos import find_best_empty_cell, dijkstra
from config import *

class Button(object):
    def __init__(self, btn_pos, text, font, text_pos):
        self.btn_pos = np.array(btn_pos)
        self.text = font.render(text, True, WHITE)
        self.text_pos = np.array(text_pos)

    def is_hover(self, mouse_pos):
        x0, y0, w, h = self.btn_pos
        return x0 <= (mouse_pos[0]/GRID_SIZE) <= (x0 + w) and y0 <= (mouse_pos[1]/GRID_SIZE) <= (y0 + h)
    
    def draw(self, screen, mouse_pos):
        if self.is_hover(mouse_pos):
            pygame.draw.rect(screen, BTN_LIGHT, GRID_SIZE * self.btn_pos)
        else:
            pygame.draw.rect(screen, BTN_DARK, GRID_SIZE * self.btn_pos)
        screen.blit(self.text, GRID_SIZE * self.text_pos)


class Fruit(object):
    def __init__(self):
        self.pos = Vector2(r.randint(0, GRID_WIDTH - 1), r.randint(0, GRID_HEIGHT - 1))

    def draw(self, screen):
        fruit_rect = pygame.Rect(self.pos.x * GRID_SIZE, self.pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, GREEN, fruit_rect)

    def random_position(self):
        self.pos.x = r.randint(0, GRID_WIDTH - 1)
        self.pos.y = r.randint(0, GRID_HEIGHT - 1)



class Snake(object):
    def __init__(self):
        self.head = Vector2(7, 10)
        self.body = [Vector2(6, 10), Vector2(5, 10)]
        self.direction = RIGHT
        self.remove_tail = True

    def draw(self, screen):
        block_rect = pygame.Rect(self.head.x * GRID_SIZE, self.head.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, block_rect)
        for block in self.body:
            block_rect = pygame.Rect(block.x * GRID_SIZE, block.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, PINK, block_rect)

    def move_snake(self):
        if self.remove_tail:
            self.body.pop(-1)
        self.body.insert(0, self.head)
        self.head = self.head + self.direction
        self.remove_tail = True

    def add_block(self):
        self.remove_tail = False

    def update_direction(self, key):
        if key == pygame.K_UP:
            if self.direction != DOWN:
                self.direction = UP
        if key == pygame.K_DOWN:
            if self.direction != UP:
                self.direction = DOWN
        if key == pygame.K_LEFT:
            if self.direction != RIGHT:
                self.direction = LEFT
        if key == pygame.K_RIGHT:
            if self.direction != LEFT:
                self.direction = RIGHT

    def get_parts(self):
        return [self.head] + self.body



class MainGame(object):
    def __init__(self):
        self.score = 0
        self.ticks_without_path = 0

        self.reset()

    def reset(self):
        self.score = 0
        self.snake = Snake()
        self.fruit = Fruit()
        self.random_fruit()

    def random_fruit(self):
        snake_parts = self.snake.get_parts()
        while self.fruit.pos in snake_parts:
            self.fruit.random_position()

    def update(self):
        self.snake.move_snake()

        if self.check_collision():
            self.score += 1
            self.snake.add_block()
            self.random_fruit()

    def draw_elements(self, screen):
        self.snake.draw(screen)
        self.fruit.draw(screen)

    def check_collision(self):
        return (self.fruit.pos == self.snake.head)
    
    def check_gameover(self):
        if not (0 <= self.snake.head.x < GRID_WIDTH and 0 <= self.snake.head.y < GRID_HEIGHT):
            return True
        if self.snake.head in self.snake.body:
            return True
        return False
    
    def self_play(self, key):
        if key is not None:
            self.snake.update_direction(key)

    def auto_play(self):
        path = dijkstra(self.snake.head, self.fruit.pos, self.snake.get_parts())
        if path != []:
            self.ticks_without_path = 0
            next_move = path[0] - self.snake.head
        else:
            # No path is found. Increment tick counter
            self.ticks_without_path += 1
            
            # Snake has had no path for too long. Find valid moves until a path opens up. 
            if self.ticks_without_path >= MAX_TICKS_WITHOUT_PATH:
                next_cell = find_best_empty_cell(self.snake.get_parts(), self.snake.direction)
                next_move = next_cell - self.snake.head
                
        self.snake.direction = next_move
