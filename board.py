import pygame
from game_colors import Color
from map import Map, Tile
from menu import Menu
from snake import Snake

class Board(Menu):

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.map = Map(10, 9, x + Tile.TILE_WIDTH, y + (Tile.TILE_HEIGHT * 2))
        super().__init__((self.map.width + 2) * Tile.TILE_WIDTH, (self.map.height + 3) * Tile.TILE_HEIGHT, x, y)
        
        self.append_child(self.map)
        self.snake = Snake(self.map)
        self.map._objects.append(self.snake)


    def draw(self, screen: pygame.Surface):
        color = Color.DARK_GREEN
        
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, self.width, self.height))
        self.map.draw(screen)
