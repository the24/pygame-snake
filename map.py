from typing import List, Tuple, Union

import pygame

from game_colors import Color
from menu import Menu

_ColorValue = Union[
    str, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
]

class Tile:
    """
    A class to represent a cell on the map

    Attributes
    ----------
    size: `int`
        size of one side
    color: `_ColorValue`
        color of the tile
    """

    def __init__(self, color: _ColorValue, size: int) -> None:
        """
        Parameters
        ----------
        size: `int`
            size of one side
        color: `pygame.color._ColorValue`
            color of the tile
        """
        self.size = size
        self.color = color


class Map(Menu):
    """
    The map where the snake moves

    Attributes
    ----------
    width: `int`
        map width in number of tiles
    height: `int`
        map height in number of tiles
    x: `int`
        horizontal position (x axis) of the top-left corner in the window
    y: `int`
        vertical position (y axis) of the top-left corner in the window
    
    Methods
    -------
    get_pos(x: `int`, y: `int`) -> `pygame.Rect`:
        return the rectangle corresponding to the tile with coordinates (x; y)
    get_case(x: `int`, y: `int`) -> `Union[Tuple[int, int], int]`:
        return the coordinates of a tile at position (x; y) on the screen
    draw(screen: `pygame.Surface`):
        draw the map on the screen
    """

    def __init__(self, width: int, height: int, x: int = 0, y: int = 0) -> None:
        self.tile_size = 36
        super().__init__(width * self.tile_size, height * self.tile_size, x, y)
    
    def get_pos(self, x: int, y: int) -> pygame.Rect:
        """
        Return the rectangle corresponding to the tile with coordinates (x; y)
        """
        x = self.x + x * self.tile_size
        y = self.y + y * self.tile_size
        return pygame.Rect(x, y, self.tile_size, self.tile_size)

    def get_case(self, x: int, y: int) -> Union[Tuple[int, int], int]:
        """
        Return the coordinates of a tile at position (x; y) on the screen
        """
        x = (x - self.x) // self.tile_size
        y = (y - self.y) // self.tile_size
        width = self.width // self.tile_size
        height = self.height // self.tile_size

        if 0 <= x < width and 0 <= y < height:
            return int(x), int(y)
        else:
            return -1

    def draw(self, screen: pygame.Surface):
        """
        Draw the map on the screen

        Parameters
        ----------
        screen: `pygame.Surface`
            Surface where the map is drawn
        """
        width, height = self.width // self.tile_size, self.height // self.tile_size
        
        for i in range(width):
            for j in range(height):
                if (i + j) % 2 == 1:
                    tile = Tile(Color.LIGHT_GREEN, self.tile_size)
                else:
                    tile = Tile(Color.GREEN, self.tile_size)
                
                x = i * tile.size + self.x
                y = j * tile.size + self.y
                
                pygame.draw.rect(screen, tile.color, pygame.Rect(x, y, tile.size, tile.size))
        
        for obj in self._objects:
            obj.draw(screen)
