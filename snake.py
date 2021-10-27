from typing import List, Tuple

import pygame
from pygame.rect import Rect
from map import Map
from object import Movable


class Snake(Movable):

    def __init__(self, map: Map, x: int = 3, y: int = 4, color: Tuple[int] = (30, 50, 170)) -> None:
        x, y = map.get_pos(x, y)
        super().__init__(x, y, 36, 36, color=color)
        self.map = map
        self.dir = [0, 0]
        self.speed = 10
        self.tail: List[Rect] = []
        self.tail_lenght = 0
    
    def update(self):
        if self.dir == [0, 0]:
            return

        if not hasattr(self, "x") or not hasattr(self, "y"):
            self.x, self.y = self.rect.x, self.rect.y
        
        if self.x == self.rect.x and self.y == self.rect.y:
            self.prev_x, self.prev_y = self.x, self.y

            self.x += self.dir[0] * 36
            self.y += self.dir[1] * 36

            for i in range(len(self.tail) - 1):
                self.tail[i] = self.tail[i + 1]
            
            self.tail[self.tail_lenght - 1] = pygame.Rect(self.prev_x, self.prev_y, 36, 36)
        else:
            delta_x = self.x - self.prev_x
            delta_y = self.y - self.prev_y
            
            self.rect.x += round(delta_x / 60 * self.speed)
            self.rect.y += round(delta_y / 60 * self.speed)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        for t in self.tail:
            pygame.draw.rect(screen, self.color, t)

    def down(self):
        self.dir = [0, 1]
    
    def up(self):
        self.dir = [0, -1]
    
    def right(self):
        self.dir = [1, 0]
    
    def left(self):
        self.dir = [-1, 0]
        
