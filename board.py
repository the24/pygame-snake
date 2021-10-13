import pygame
from game_colors import Color
from map import Map, Tile
from snake import Snake


class Board:
    snake = Snake()

    def __init__(self, x = 0, y = 0) -> None:
        self.map = Map(10, 9, x + Tile.TILE_WIDTH, y + (Tile.TILE_HEIGHT * 2))
        self.x = x
        self.y = y
        self.width = (self.map.width + 2) * Tile.TILE_WIDTH
        self.height = (self.map.height + 3) * Tile.TILE_HEIGHT


    def draw(self, screen: pygame.Surface):
        color = Color.DARK_GREEN
        
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, self.width, self.height))
        self.map.draw(screen)

        self.snake.draw(screen)
    
    def center(self, screen: pygame.Surface):
        self.x = (screen.get_width() - self.width) / 2
        self.y = (screen.get_height() - self.height) / 2
        self.map.map_posx = self.x + Tile.TILE_WIDTH
        self.map.map_posy = self.y + (Tile.TILE_HEIGHT * 2)
