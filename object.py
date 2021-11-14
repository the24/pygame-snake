from typing import List, Tuple, Union

import pygame

_ColorValue = Union[
    str, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
]


class Object:
    """
    An object in the game.

    Attributes
    ----------
    rect: `pygame.Rect`
        size of the object
    color: `_ColorValue`
        color of the object

    Methods
    -------
    set_color(color: `_ColorValue`) -> `None`:
        change the color of the object
    draw(screen: `pygame.Surface`) -> `None`:
        draw the object (rect) on the screen
    """

    def __init__(self, x: int, y: int, width:int, height:int, color: _ColorValue = (0, 0, 0)) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self._color = color

    def set_color(self, color: _ColorValue) -> None:
        """
        Change the color of the object
        """
        self._color = color

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the object (rect) on the screen
        """
        pygame.draw.rect(screen, self._color, self.rect)


class Movable(Object):
    """
    An object that can move

    Attributes
    ----------
    rect: `pygame.Rect`
        size of the object
    color: `_ColorValue`
        color of the object

    Methods
    -------
    set_color(color: `_ColorValue`) -> `None`:
        change the color of the object
    draw(screen: `pygame.Surface`) -> `None`:
        draw the object (rect) on the screen
    move(x: `int`, y: `int`) -> `None`:
        add (x; y) to the coordinates of the object
    """

    def __init__(self, x: int, y: int, width: int, height: int, color: _ColorValue = (0, 0, 0)) -> None:
        super().__init__(x, y, width, height, color=color)
    
    def move(self, x, y) -> None:
        """
        Add (x, y) to the coordinates of the object
        """
        self.rect.x += x
        self.rect.y += y
