from math import ceil, floor
from random import randint
from typing import List, Tuple, Union

import pygame

import gui
from gui import Map
from object import Movable, Object

_ColorValue = Union[
    str, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
]
_Coords = Tuple[int, int]

class Snake(Movable):
    """
    The snake played by the player

    Attributes
    ----------
    dir: `(int, int)`
        direction vector of the snake
    speed: `int`
        speed of the snake
    map: `Map`
        the map on which the snake moves
    tail: `List[_Coords]`
        list of the positions of each part of the snake's tail
    tail_lenght: `int`
        lenght of the tail
    
    Methods
    -------
    update():
        method called at each frame
    eat():
        method called when the snake eats
    get_corner_orientation(p0: `_Coords`, p1: `_Coords`, p3: `_Coords`) -> `_Coords`:
        returns the orientation of the corner
    get_head_angle() -> int:
        returns the angle between the head and the vertical axis
    get_angle(p1: `_Coords`, p2: `_Coords`) -> int:
        returns the angle between two points with and the vertical axis
    get_head_advancement():
        offset between the beginning of the tile and the head position
    draw():
        draw the snake on the screen
    down():
        change direction of the snake
    up():
        change direction of the snake
    right():
        change direction of the snake
    left():
        change direction of the snake
    """

    def __init__(self, map: Map, x: int = 3, y: int = 4, color: _ColorValue = (30, 50, 170)) -> None:
        self.dir: _Coords = (0, 0)
        self.speed: int = 5
        self.map: Map = map
        self.tail: List[_Coords] = []

        super().__init__(*map.get_pos(x, y).topleft, 36, 36, color=color)

        self.prev_x, self.prev_y = self.x, self.y = self.rect.center

        # Adds the first parts of the tail
        for i in range(3, 0, -1):
            self.tail.append((x - i, y))
        self.tail_lenght: int = len(self.tail)
    
    def update(self) -> None:
        if self.dir == (0, 0):
            return
        
        if self.rect.center == (self.x, self.y):
            # Coords update
            self.prev_x, self.prev_y = self.x, self.y

            self.x += self.dir[0] * self.map.tile_size
            self.y += self.dir[1] * self.map.tile_size

            # Tail update
            for i in range(len(self.tail) - 1):
                self.tail[i] = self.tail[i + 1]
            
            self.tail[self.tail_lenght - 1] = self.map.get_case(self.rect.x, self.rect.y)
        else:
            # Translate rect
            delta_x = self.x - self.prev_x
            delta_y = self.y - self.prev_y
            
            mx = round(delta_x / 60 * self.speed)
            my = round(delta_y / 60 * self.speed)
            self.rect.x += mx
            self.rect.y += my
    
    def eat(self) -> None:
        """
        Method called when the snake eats.
        """
        self.tail.insert(0, self.tail[0])
        self.tail_lenght += 1
    
    def get_corner_orientation(self, p0: _Coords, p1: _Coords, p2: _Coords) -> _Coords:
        """
        Returns the orientation of the corner.
        Where :
            * `(-1, -1)` is top-left
            * `(-1, 1)` is down-left
            * `(1, -1)` is top-right
            * `(1, 1)` is down-right
        """
        top_left = (-1, -1)
        down_left = (-1, 1)
        top_right = (1, -1)
        down_right = (1, 1)
        x, y = p1

        if  (p0 == (x-1, y) and p2 == (x, y+1)) or \
            (p2 == (x-1, y) and p0 == (x, y+1)):
            return down_left
        elif (p0 == (x-1, y) and p2 == (x, y-1)) or \
             (p2 == (x-1, y) and p0 == (x, y-1)):
            return top_left
        elif (p0 == (x+1, y) and p2 == (x, y-1)) or \
             (p2 == (x+1, y) and p0 == (x, y-1)):
            return top_right
        elif (p0 == (x+1, y) and p2 == (x, y+1)) or \
             (p2 == (x+1, y) and p0 == (x, y+1)):
            return down_right
        else:
            raise Exception("The three points do not form a corner")
    
    def get_head_angle(self) -> int:
        """
        Returns the angle between the head and the vertical axis.
        """
        if self.dir == (1, 0) or self.dir == (0, 0):
            return 0
        elif self.dir == (0, -1):
            return 90
        elif self.dir == (-1, 0):
            return 180
        elif self.dir == (0, 1):
            return 270
    
    def get_angle(self, p1: _Coords, p2: _Coords) -> int:
        """
        Returns the angle between two juxtaposed points with respect to the vertical axis.
        """
        if p1[0] == p2[0] - 1 and p1[1] == p2[1]:
            return 0
        elif p1[0] == p2[0] and p1[1] == p2[1] + 1:
            return 90
        elif p1[0] == p2[0] + 1 and p1[1] == p2[1]:
            return 180
        elif p1[0] == p2[0] and p1[1] == p2[1] - 1:
            return 270
        else:
            return 0
    
    def get_head_advancement(self) -> None:
        """
        Returns the offset between the beginning of the tile and the current head position.
        """
        prev = self.tail[self.tail_lenght - 1]
        prev = self.map.get_pos(*prev).topleft
        return max(abs(prev[0] - self.rect.x), abs(prev[1] - self.rect.y))

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw snake on the screen.
        """
        head_x, head_y = self.rect.x, self.rect.y
        head_angle = self.get_head_angle()
        size = self.rect.width
        
        head = gui.get_head_surface(size, self._color, head_angle)
        pygame.Surface.blit(screen, head, (head_x, head_y))

        for i in range(self.tail_lenght):
            t = self.tail[i]
            x, y = self.map.get_pos(t[0], t[1]).topleft
            if i == 0:
                # End of tail
                prev = self.tail[1]
                delta = self.get_head_advancement()
                angle = self.get_angle(t, prev)
                end_tail = gui.get_end_tail_surface(size, self._color, angle, delta, self.speed)
                
                if angle == 90 or angle == 180:
                    pygame.Surface.blit(screen, end_tail, (x, y))
                elif angle == 0:
                    offset = end_tail.get_size()[0] - size
                    pygame.Surface.blit(screen, end_tail, (x - offset, y))
                elif angle == 270:
                    offset = end_tail.get_size()[1] - size
                    pygame.Surface.blit(screen, end_tail, (x, y - offset))
                
            elif i == self.tail_lenght - 1:
                # Neck
                neck = gui.get_neck_surface(size, x, y, self.rect, self._color, head_angle)
                pygame.Surface.blit(screen, neck, (x, y))
            else:
                t_before = self.tail[i-1]
                t_after = self.tail[i+1]
                
                snake_width = ceil(0.8*size)
                margin = floor(0.1*size)

                if t_before[0] == t[0] == t_after[0]:
                    # Horizontal line
                    pygame.draw.rect(screen, self._color, (x + margin, y, snake_width, size))
                elif t_before[1] == t[1] == t_after[1]:
                    # Vertical line
                    pygame.draw.rect(screen, self._color, (x, y + margin, size, snake_width))
                else:
                    # Corner
                    orientation = self.get_corner_orientation(t_before, self.map.get_case(x, y), t_after)
                    # Transforms -1 into 0 and 1 into 1
                    corner_pos = tuple(map(lambda x: (x+1)//2, orientation))
                    corner = gui.get_corner_surface(size, self._color, corner_pos)
                    pygame.Surface.blit(screen, corner, (x, y))

    def down(self) -> None:
        """
        Change the direction downwards
        """
        self.dir = (0, 1)
    
    def up(self) -> None:
        """
        Change the direction upwards
        """
        self.dir = (0, -1)
    
    def right(self) -> None:
        """
        Change the direction to the right
        """
        self.dir = (1, 0)
    
    def left(self) -> None:
        """
        Change the direction to the left
        """
        self.dir = (-1, 0)


class Apple(Object):

    def __init__(self, map: Map) -> None:
        self.pos = (7, 4)
        self.map = map
        self.size = map.tile_size
        x, y = map.get_pos(self.pos[0], self.pos[1]).topleft
        super().__init__(x, y, self.size, self.size, color=(255, 0, 0))
    
    def gen_new_apple(self, snake: Snake):
        x = randint(0, self.map.width//self.map.tile_size - 1)
        y = randint(0, self.map.height//self.map.tile_size - 1)
        self.pos = (x, y)
        while self.pos in snake.tail:
            x = randint(0, self.map.width//self.map.tile_size - 1)
            y = randint(0, self.map.height//self.map.tile_size - 1)
            self.pos = (x, y)
        
        x, y = self.map.get_pos(x, y).topleft
        rect = pygame.Rect(x, y, self.size, self.size)
        self.rect = rect
    
    def draw(self, screen: pygame.Surface):
        apple = gui.get_apple_surface(self.size)
        pygame.Surface.blit(screen, apple, (self.rect.x, self.rect.y))
