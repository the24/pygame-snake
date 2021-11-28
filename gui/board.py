
from typing import Tuple

import pygame
from pygame import Rect, Surface

from gui import Menu, colors

_IntVec2D = Tuple[int, int]

class Board(Menu):

    def __init__(self, pos: _IntVec2D = (0, 0), tile_size = 36) -> None:
        self.border_size = self.tile_size = tile_size
        self.map_size = (10, 9)

        width  = (self.map_size[0] * self.tile_size) + (2 * self.border_size)
        height = (self.map_size[1] * self.tile_size) + (3 * self.border_size)
        super().__init__(pos, (width, height))
    
    @property
    def map_pos(self) -> _IntVec2D:
        return (self.rect.x + self.border_size, 
                self.rect.y + (self.border_size * 2))

    def draw(self, screen: Surface, score: int = 0):
        rect = self.rect
        
        pygame.draw.rect(screen,
                        colors.DARK_GREEN,
                        Rect(rect.x, rect.y, rect.width, rect.height))

        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                x = i * self.tile_size + rect.x + self.border_size
                y = j * self.tile_size + rect.y + (self.border_size * 2)

                if (i + j) % 2 == 1:
                    pygame.draw.rect(screen,
                                    colors.LIGHT_GREEN,
                                    Rect(x, y, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(screen,
                                    colors.GREEN,
                                    Rect(x, y, self.tile_size, self.tile_size))
