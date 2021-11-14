from dataclasses import dataclass
from math import ceil, floor
from typing import List, Tuple, Union

import pygame

from object import Object

_ColorValue = Union[
    str, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
]

# The font used in the Label.
# Must be initialized before being used (`init_font`).
_GameFont: pygame.font.Font = None

class Color():
    BLUE = (41, 128, 185)
    LIGHT_GREEN = (196, 229, 56)
    GREEN = (163, 203, 56)
    DARK_GREEN = (0, 148, 50)
    EYES = (255, 255, 255)


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
    
    def append_childs(self, *childs) -> None:
        for child in childs:
            self.append_child(child)
    
    def append_object(self, object: Object) -> None:
        self._objects.append(object)
    
    def append_objects(self, *objects: Object) -> None:
        for object in objects:
            self.append_object(object)

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


class Label:

    def __init__(self, text: str, color: _ColorValue, rect: pygame.Rect) -> None:
        self.text = text
        self.color = color
        self.rect = rect
    
    def set_text(self, text: str):
        self.text = text

    def draw(self, screen: pygame.Surface):
        text = _GameFont.render(self.text, True, self.color)
        x = self.rect.x
        y = self.rect.centery - text.get_size()[1]/2
        screen.blit(text, (x, y))

@dataclass
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
    color: _ColorValue
    size: int


class Board(Menu):

    def __init__(self, x: int = 0, y: int = 0) -> None:
        border_size = 36

        self.map = Map(10, 9, x + border_size, y + border_size * 2)
        label_rect = pygame.Rect(x + border_size, y, x + border_size + 50, y + border_size * 2)
        self.label = Label("0", (255, 255, 255), label_rect)

        super().__init__(self.map.width + (2 * border_size), self.map.height + (3 * border_size), x, y)

        self.append_child(self.map)
        self.append_object(self.label)

    def draw(self, screen: pygame.Surface, score: int):
        color = Color.DARK_GREEN
        
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, self.width, self.height))
        self.label.set_text(str(score))
        self.label.draw(screen)
        self.map.draw(screen)


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


def init_font(font: str, size: int):
    global _GameFont
    _GameFont = pygame.font.SysFont(font, size)

def get_head_surface(size: int, main_color: _ColorValue, angle: int) -> pygame.Surface:
    draw_surface = pygame.Surface((size, size)).convert_alpha()
    draw_surface.fill((0, 0, 0, 0))
        
    snake_width = ceil(0.8*size)
    margin = floor(0.1*size)
    one_third = round(1/3*size)

    # Nose
    pygame.draw.ellipse(draw_surface, main_color, (one_third, margin, 2*one_third, snake_width))

    # Body
    pygame.draw.rect(draw_surface, main_color, (0, margin, 2*one_third, snake_width))

    # Eye
    r = round(1/4*size)
    pygame.draw.circle(draw_surface, main_color, (one_third, r), r)
    pygame.draw.circle(draw_surface, main_color, (one_third, size - r), r)

    r = round(1/7*size)
    pygame.draw.circle(draw_surface, Color.EYES, (one_third, r), r)
    pygame.draw.circle(draw_surface, Color.EYES, (one_third, size - r), r)
        
    pygame.draw.circle(draw_surface, main_color, (7/18*size, r), 2/3*r)
    pygame.draw.circle(draw_surface, main_color, (7/18*size, size - r), 2/3*r)

    draw_surface = pygame.transform.rotate(draw_surface, angle)
    
    # Because it's not totally symmetrical
    if angle == 180:
        draw_surface = pygame.transform.flip(draw_surface, False, True)
    elif angle == 270:
        draw_surface = pygame.transform.flip(draw_surface, True, False)

    return draw_surface

def get_neck_surface(size, x: int, y: int, head_rect: pygame.Rect, main_color: _ColorValue, angle: int) -> pygame.Surface:
    # TODO: Handle when the neck is a corner

    draw_surface = pygame.Surface((size, size)).convert_alpha()
    draw_surface.fill((0, 0, 0, 0))

    lenght_x = abs(x - head_rect.x)
    lenght_y = abs(y - head_rect.y)

    snake_width = ceil(0.8*size)
    margin = floor(0.1*size)

    if angle == 0:
        pygame.draw.rect(draw_surface, main_color, (0, margin, lenght_x, snake_width))
    elif angle == 90:
        pygame.draw.rect(draw_surface, main_color, (margin, head_rect.height - lenght_y, snake_width, lenght_y))
    elif angle == 180:
        pygame.draw.rect(draw_surface, main_color, (head_rect.width - lenght_x, margin, lenght_x, snake_width))
    elif angle == 270:
        pygame.draw.rect(draw_surface, main_color, (margin, 0, snake_width, lenght_y))
    else:
        pygame.draw.rect(draw_surface, main_color, (0, margin, size, snake_width))
    
    return draw_surface


def get_corner_surface(size, main_color: _ColorValue, corner_pos: Tuple[int, int]) -> pygame.Surface:
    draw_surface = pygame.Surface((size, size)).convert_alpha()
    transparent = (0, 0, 0, 0)
    draw_surface.fill(transparent)

    pos_x, pos_y = corner_pos[0], corner_pos[1]
    snake_width = ceil(0.8*size)
    margin = floor(0.1*size)

    pygame.draw.circle(draw_surface, main_color, (size*pos_x, size*pos_y), snake_width + margin)
    pygame.draw.circle(draw_surface, transparent, (size*pos_x, size*pos_y), margin)

    return draw_surface        

def get_end_tail_surface(size, main_color: _ColorValue, angle: int, delta: int, speed: int) -> pygame.Surface:
    lenght = (3/2)*size if speed > 0 else size
    draw_surface = pygame.Surface((lenght, size)).convert_alpha()
    draw_surface.fill((0, 0, 0, 0))

    snake_width = ceil(0.8*size)
    margin = floor(0.1*size)
    r = round(snake_width/2)
    center = round(size/2)
    
    pygame.draw.circle(draw_surface, main_color, (center + delta, center), r)
    pygame.draw.rect(draw_surface, main_color, (center + delta, margin, lenght, snake_width))
    
    draw_surface = pygame.transform.rotate(draw_surface, angle)

    # Because it's not totally symmetrical on small screens
    if angle == 180:
        draw_surface = pygame.transform.flip(draw_surface, False, True)
    elif angle == 270:
        draw_surface = pygame.transform.flip(draw_surface, True, False)
    
    return draw_surface
