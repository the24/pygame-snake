from math import ceil, floor
from typing import List, Tuple

import pygame

from game_colors import Color
from map import Map
from object import Movable


class Snake(Movable):

    def __init__(self, map: Map, x: int = 3, y: int = 4, color: Tuple[int] = (30, 50, 170)) -> None:
        x, y = map.get_pos(x, y).topleft
        super().__init__(x, y, 36, 36, color=color)
        self.map = map

        self.dir = [0, 0]
        self.speed = 1

        x, y = map.get_case(x, y)
        self.tail: List[Tuple[int, int]] = []
        for i in range(3, 0, -1):
            self.tail.append((x - i, y))
        self.tail_lenght = len(self.tail)
    
    def update(self):
        if self.dir == [0, 0]:
            return

        if not hasattr(self, "x") or not hasattr(self, "y"):
            self.prev_x, self.prev_y = self.x, self.y = self.rect.center
        
        if self.rect.center == (self.x, self.y):
            self.prev_x, self.prev_y = self.x, self.y

            self.x += self.dir[0] * self.map.tile_size
            self.y += self.dir[1] * self.map.tile_size

            for i in range(len(self.tail) - 1):
                self.tail[i] = self.tail[i + 1]
            
            self.tail[self.tail_lenght - 1] = self.map.get_case(self.rect.x, self.rect.y)
        else:
            delta_x = self.x - self.prev_x
            delta_y = self.y - self.prev_y
            
            mx = round(delta_x / 60 * self.speed)
            my = round(delta_y / 60 * self.speed)
            self.rect.x += mx
            self.rect.y += my
    
    def get_corner_orientation(self, p0: Tuple[int, int], p1: Tuple[int, int], p2:Tuple[int, int]) -> Tuple[int, int] | int:
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
            return -1

    def _draw_head(self, screen: pygame.Surface, x, y, size):
        snake_surface = pygame.Surface((size, size)).convert_alpha()
        snake_surface.fill((0, 0, 0, 0))
        
        snake_width = ceil(0.8*size)
        margin = floor(0.1*size)
        one_third = round(1/3*size)

        # Nose
        pygame.draw.ellipse(snake_surface, self.color, (one_third, margin, 2*one_third, snake_width))

        # Body
        pygame.draw.rect(snake_surface, self.color, (0, margin, 2*one_third, snake_width))

        # Eye
        r = round(1/4*size)
        pygame.draw.circle(snake_surface, self.color, (one_third, r), r)
        pygame.draw.circle(snake_surface, self.color, (one_third, size - r), r)

        r = round(1/7*size)
        pygame.draw.circle(snake_surface, Color.EYES, (one_third, r), r)
        pygame.draw.circle(snake_surface, Color.EYES, (one_third, size - r), r)
        
        pygame.draw.circle(snake_surface, self.color, (7/18*size, r), 2/3*r)
        pygame.draw.circle(snake_surface, self.color, (7/18*size, size - r), 2/3*r)

        if self.dir == [0, 1]:
            snake_surface = pygame.transform.rotate(snake_surface, 270)
            # Because it's not totally symmetrical
            snake_surface = pygame.transform.flip(snake_surface, True, False)
        elif self.dir == [-1, 0]:
            snake_surface = pygame.transform.rotate(snake_surface, 180)
            # Because it's not totally symmetrical
            snake_surface = pygame.transform.flip(snake_surface, False, True)
        elif self.dir == [0, -1]:
            snake_surface = pygame.transform.rotate(snake_surface, 90)
        
        pygame.Surface.blit(screen, snake_surface, (x, y))

    def _draw_neck(self, screen: pygame.Surface, x: int, y: int, size: int, head_x: int, head_y: int):
        # TODO: Handle when the neck is a corner

        lenght_x = abs(x - head_x)
        lenght_y = abs(y - head_y)

        snake_width = ceil(0.8*size)
        margin = floor(0.1*size)

        if self.dir == [1, 0]:
            pygame.draw.rect(screen, self.color, (x, y + margin, lenght_x, snake_width))
        elif self.dir == [-1, 0]:
            pygame.draw.rect(screen, self.color, (self.rect.topright[0], y + margin, lenght_x, snake_width))
        elif self.dir == [0, 1]:
            pygame.draw.rect(screen, self.color, (x + margin, y, snake_width, lenght_y))
        elif self.dir == [0, -1]:
            pygame.draw.rect(screen, self.color, (x + margin, self.rect.bottomleft[1], snake_width, lenght_y))

    def _draw_corner(self, screen: pygame.Surface, x: int, y: int, size: int, t_before: Tuple[int, int], t_after: Tuple[int, int]):
        o = self.get_corner_orientation(t_before, self.map.get_case(x, y), t_after)
        draw_surface = pygame.Surface((size, size)).convert_alpha()
        transparent = (0, 0, 0, 0)
        draw_surface.fill(transparent)

        snake_width = ceil(0.8*size)
        margin = floor(0.1*size)

        if o == (1, 1):
            pygame.draw.circle(draw_surface, self.color, (size, size), snake_width + margin)
            pygame.draw.circle(draw_surface, transparent, (size, size), margin)
        if o == (1, -1):
            pygame.draw.circle(draw_surface, self.color, (size, 0), snake_width + margin)
            pygame.draw.circle(draw_surface, transparent, (size, 0), margin)
        elif o == (-1, -1):
            pygame.draw.circle(draw_surface, self.color, (0, 0), snake_width + margin)
            pygame.draw.circle(draw_surface, transparent, (0, 0), margin)
        elif o == (-1, 1):
            pygame.draw.circle(draw_surface, self.color, (0, size), snake_width + margin)
            pygame.draw.circle(draw_surface, transparent, (0, size), margin)
        
        pygame.Surface.blit(screen, draw_surface, (x, y))
    
    def _draw_end_tail(self, screen: pygame.Surface, x: int, y: int, size: int, t_before: Tuple[int, int]):
        if hasattr(self, "prev_x") and hasattr(self, "prev_y"):
            delta = max(abs(self.prev_x - self.rect.centerx), abs(self.prev_y - self.rect.centery))
        else:
            delta = 0

        draw_surface = pygame.Surface((size - delta, size)).convert_alpha()
        draw_surface.fill((0, 0, 0, 0))

        snake_width = ceil(0.8*size)
        margin = floor(0.1*size)
        r = round(snake_width/2)
        center = round(size/2)

        pygame.draw.circle(draw_surface, self.color, (center, center), r)
        pygame.draw.rect(draw_surface, self.color, (center, margin, center, snake_width))
        
        case_x, case_y = self.map.get_case(x, y)
        if case_x == t_before[0] - 1 and case_y == t_before[1]:
            pygame.Surface.blit(screen, draw_surface, (x + delta, y))
        elif case_x == t_before[0] and case_y == t_before[1] + 1:
            draw_surface = pygame.transform.rotate(draw_surface, 90)

            pygame.Surface.blit(screen, draw_surface, (x, y))
        elif case_x == t_before[0] and case_y == t_before[1] - 1:
            draw_surface = pygame.transform.rotate(draw_surface, 270)
            # Because it's not totally symmetrical on small screens
            draw_surface = pygame.transform.flip(draw_surface, True, False)

            pygame.Surface.blit(screen, draw_surface, (x, y + delta))
        elif case_x == t_before[0] + 1 and case_y == t_before[1]:
            draw_surface = pygame.transform.rotate(draw_surface, 180)
            # Because it's not totally symmetrical on small screens
            draw_surface = pygame.transform.flip(draw_surface, False, True)

            pygame.Surface.blit(screen, draw_surface, (x, y))

    def draw(self, screen):
        head_x, head_y = self.rect.x, self.rect.y
        size = self.rect.width
        
        self._draw_head(screen, head_x, head_y, size)

        for i in range(self.tail_lenght):
            t = self.tail[i]
            x, y = self.map.get_pos(t[0], t[1]).topleft
            if i == 0:
                self._draw_end_tail(screen, x, y, size, self.tail[1])
            elif i == self.tail_lenght - 1:
                self._draw_neck(screen, x, y, size, head_x, head_y)
            else:
                t_before = self.tail[i-1]
                t_after = self.tail[i+1]
                
                snake_width = ceil(0.8*size)
                margin = floor(0.1*size)

                if t_before[0] == t[0] == t_after[0]:
                    pygame.draw.rect(screen, self.color, (x + margin, y, snake_width, size))
                elif t_before[1] == t[1] == t_after[1]:
                    pygame.draw.rect(screen, self.color, (x, y + margin, size, snake_width))
                else:
                    self._draw_corner(screen, x, y, size, t_before, t_after)

    def down(self):
        self.dir = [0, 1]
    
    def up(self):
        self.dir = [0, -1]
    
    def right(self):
        self.dir = [1, 0]
    
    def left(self):
        self.dir = [-1, 0]
        
