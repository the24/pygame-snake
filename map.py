import pygame

from game_colors import Color
from menu import Menu
from snake import Snake

class Tile:
    TILE_WIDTH: int = 36
    TILE_HEIGHT: int = 36

    def __init__(self, color) -> None:
        self.size = self.width, self.height = Tile.TILE_WIDTH, Tile.TILE_HEIGHT
        self.color = color


class Map(Menu):
    snake = Snake()

    def __init__(self, width: int, height: int, x: int = 0, y: int = 0) -> None:
        super().__init__(width, height, x, y)
        self._objects.append(self.snake)
    
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
