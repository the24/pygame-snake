import pygame

from food import Apple
from game_colors import Color
from map import Map
from menu import Menu
from snake import Snake


class Board(Menu):

    def __init__(self, x: int = 0, y: int = 0) -> None:
        border_size = 36
        self.map = Map(10, 9, x + border_size, y + border_size * 2)
        super().__init__(self.map.width + (2 * border_size), self.map.height + (3 * border_size), x, y)
        
        self.append_child(self.map)
        self.snake = Snake(self.map)
        self.apple = Apple(self.map)
        self.map._objects.append(self.snake)
        self.map._objects.append(self.apple)


    def update(self):
        if self.snake.rect.collidepoint(self.apple.rect.center):
            self.snake.eat()
            self.apple.gen_new_apple(self.snake)
        
        self.snake.update()

    def draw(self, screen: pygame.Surface):
        color = Color.DARK_GREEN
        
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, self.width, self.height))
        self.map.draw(screen)
