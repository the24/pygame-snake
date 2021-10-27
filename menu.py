from typing import List
import pygame

from object import Object

class Menu:
    
    def __init__(self, width: int, height: int, x: int = 0, y: int = 0) -> None:
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self._childs: List[Menu] = []
        self._objects: List[Object] = []
    
    def append_child(self, child) -> None:
        self._childs.append(child)

    def center(self, screen: pygame.Surface) -> None:
        self.move((screen.get_width() - self.width) / 2, (screen.get_height() - self.height) / 2)
    
    def move(self, x: int, y: int) -> None:
        delta_x = x - self.x
        delta_y = y - self.y
        self.x = x
        self.y = y

        for child in self._childs:
            child.move(child.x + delta_x, child.y + delta_y)
        
        for obj in self._objects:
            obj.rect.x += delta_x
            obj.rect.y += delta_y
