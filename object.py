from typing import Tuple
import pygame

class Object:
    
    def __init__(self, x: int, y: int, width:int, height:int, color: Tuple[int] = (0, 0, 0)) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def change_color(self, color: Tuple[int]) -> None:
        self.color = color

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect)


class Mouvable(Object):

    def __init__(self, x: int, y: int, width: int, height: int, color: Tuple[int] = (0, 0, 0)) -> None:
        super().__init__(x, y, width, height, color=color)
    
    def move(self, x, y) -> None:
        self.rect.x += x
        self.rect.y += y