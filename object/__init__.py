
from typing import List, Tuple, Union

import pygame

_ColorValue = Union[
    str, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
]
_IntVec2D = Tuple[int, int]


class Object:
    """
    An object in the game.
    Attributes
    ----------
    pos: `_IntVec2D`
        position of the object
    _surface (private): `pygame.Surface`
        surface of the object
    Methods
    -------
    set_surface(surface: `pygame.Surface`) -> `None`:
        change the surface of the object
    set_pos(x: `int`, y: `int`) -> None:
        change position of the object
    """

    def __init__(self, pos: _IntVec2D, surface: pygame.Surface) -> None:
        self.pos = pos
        self._surface = surface

    def set_surface(self, surface: pygame.Surface) -> None:
        """
        Change the surface of the object
        """
        self._surface = surface
    
    def set_pos(self, x: int, y: int) -> None:
        """
        Change position of the object
        """
        self.pos = (x, y)
