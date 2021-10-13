from typing import Tuple
from object import Mouvable


class Snake(Mouvable):

    def __init__(self, x: int = 3, y: int = 4, color: Tuple[int] = (30, 50, 170)) -> None:
        super().__init__(x, y, 24, 24, color=color)
        self.speed = [0, 0]
    
    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
    
    def down(self):
        self.speed = [0, 1]
    
    def up(self):
        self.speed = [0, -1]
    
    def right(self):
        self.speed = [1, 0]
    
    def left(self):
        self.speed = [-1, 0]
        
