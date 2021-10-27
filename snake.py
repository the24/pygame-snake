from typing import Tuple
from map import Map
from object import Movable


class Snake(Movable):

    def __init__(self, map: Map, x: int = 3, y: int = 4, color: Tuple[int] = (30, 50, 170)) -> None:
        x, y = map.get_pos(x, y)
        super().__init__(x, y, 24, 24, color=color)
        self.map = map
        self.dir = [0, 0]
        self.speed = 2
    
    def update(self):
        self.rect.x += self.dir[0] * self.speed
        self.rect.y += self.dir[1] * self.speed
    
    def down(self):
        self.dir = [0, 1]
    
    def up(self):
        self.dir = [0, -1]
    
    def right(self):
        self.dir = [1, 0]
    
    def left(self):
        self.dir = [-1, 0]
        
