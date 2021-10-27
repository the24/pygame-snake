from typing import Tuple
import pygame

from game_colors import Color
from menu import Menu

class Tile:
    TILE_WIDTH: int = 36
    TILE_HEIGHT: int = 36

    def __init__(self, color) -> None:
        self.size = self.width, self.height = Tile.TILE_WIDTH, Tile.TILE_HEIGHT
        self.color = color


class Map(Menu):

    def __init__(self, width: int, height: int, x: int = 0, y: int = 0) -> None:
        super().__init__(width, height, x, y)
    
    def get_pos(self, x: int, y: int) -> Tuple[int, int]:
        return self.x + x * Tile.TILE_WIDTH, self.y + y * Tile.TILE_HEIGHT

    def get_case(self, x: int, y: int) -> Tuple[int, int] | int:
        x = (x - self.x) // Tile.TILE_WIDTH
        y = (y - self.y) // Tile.TILE_HEIGHT
        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y
        else:
            return -1

    def draw(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                if (i + j) % 2 == 1:
                    tile = Tile(Color.LIGHT_GREEN)
                else:
                    tile = Tile(Color.GREEN)
                
                x = i * tile.width + self.x
                y = j * tile.height + self.y
                
                pygame.draw.rect(screen, tile.color, pygame.Rect(x, y, tile.width, tile.height))
        
        for obj in self._objects:
            obj.draw(screen)
