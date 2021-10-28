from typing import List, Tuple

import pygame
from pygame.rect import Rect
from game_colors import Color
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
        self.tail_lenght = len(self.tail)
    
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
            
            #self.tail[self.tail_lenght - 1] = pygame.Rect(self.prev_x, self.prev_y, 36, 36)
        else:
            delta_x = self.x - self.prev_x
            delta_y = self.y - self.prev_y
            
            self.rect.x += round(delta_x / 60 * self.speed)
            self.rect.y += round(delta_y / 60 * self.speed)
    
    def _draw_head(self, screen: pygame.Surface, x, y, w, h):
        snake_surface = pygame.Surface((w, h)).convert_alpha()
        snake_surface.fill((0, 0, 0, 0))
        
        # Nose
        r = 1/3*w
        pygame.draw.ellipse(snake_surface, self.color, (1/3*w, 0.1*h, 2/3*w, 0.8*h))

        # Body
        pygame.draw.rect(snake_surface, self.color, (0, 0.1*h, 2/3*w, 0.8*h))

        # Eye
        r = 1/4*w
        pygame.draw.circle(snake_surface, self.color, (1/3*w, r), r)
        pygame.draw.circle(snake_surface, self.color, (1/3*w, h - r), r)

        r = 1/7*w
        pygame.draw.circle(snake_surface, Color.EYES, (1/3*w, r), r)
        pygame.draw.circle(snake_surface, Color.EYES, (1/3*w, h - r), r)
        
        pygame.draw.circle(snake_surface, self.color, (7/18*w, r), 2/3*r)
        pygame.draw.circle(snake_surface, self.color, (7/18*w, h - r), 2/3*r)

        if self.dir == [0, 1]:
            snake_surface = pygame.transform.rotate(snake_surface, 270)
        elif self.dir == [-1, 0]:
            snake_surface = pygame.transform.rotate(snake_surface, 180)
        elif self.dir == [0, -1]:
            snake_surface = pygame.transform.rotate(snake_surface, 90)
        
        pygame.Surface.blit(screen, snake_surface, (x, y))

    def draw(self, screen):
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        
        self._draw_head(screen, x, y, w, h)

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
        
