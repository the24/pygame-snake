from typing import List, Tuple

import pygame
from game_colors import Color
from map import Map, Tile
from object import Movable


class Snake(Movable):

    def __init__(self, map: Map, x: int = 3, y: int = 4, color: Tuple[int] = (30, 50, 170)) -> None:
        x, y = map.get_pos(x, y)
        super().__init__(x, y, 36, 36, color=color)
        self.map = map

        self.dir = [0, 0]
        self.speed = 10

        x, y = map.get_case(x, y)
        self.tail: List[Tuple[int, int]] = []
        for i in range(1, 4):
            self.tail.append((x - i, y))
        self.tail_lenght = len(self.tail)
    
    def update(self):
        if self.dir == [0, 0]:
            return

        if not hasattr(self, "x") or not hasattr(self, "y"):
            self.prev_x, self.prev_y = self.x, self.y = self.rect.center
        
        if self.rect.center == (self.x, self.y):
            self.prev_x, self.prev_y = self.x, self.y

            self.x += self.dir[0] * Tile.TILE_WIDTH
            self.y += self.dir[1] * Tile.TILE_HEIGHT

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
            # Because it's not totally symmetrical
            snake_surface = pygame.transform.flip(snake_surface, True, False)
        elif self.dir == [-1, 0]:
            snake_surface = pygame.transform.rotate(snake_surface, 180)
            # Because it's not totally symmetrical
            snake_surface = pygame.transform.flip(snake_surface, False, True)
        elif self.dir == [0, -1]:
            snake_surface = pygame.transform.rotate(snake_surface, 90)
        
        pygame.Surface.blit(screen, snake_surface, (x, y))

    def _draw_neck(self, screen: pygame.Surface, x, y, w, h, head_x, head_y):
        # TODO: Handle when the neck is a corner
        lenght_x = abs(x - head_x)
        lenght_y = abs(y - head_y)

        if self.dir == [1, 0]:
            pygame.draw.rect(screen, self.color, (x, y + 0.1*h, lenght_x, 0.8*h))
        elif self.dir == [-1, 0]:
            pygame.draw.rect(screen, self.color, (self.rect.topright[0], y + 0.1*h, lenght_x, 0.8*h))
        elif self.dir == [0, 1]:
            pygame.draw.rect(screen, self.color, (x + 0.1*w, y, 0.8*w, lenght_y))
        elif self.dir == [0, -1]:
            pygame.draw.rect(screen, self.color, (x + 0.1*w, self.rect.bottomleft[1], 0.8*w, lenght_y))

    def _draw_corner(self, screen: pygame.Surface, x: int, y: int, w: int, h: int, t_before: Tuple[int, int], t_after: Tuple[int, int]):
        o = self.get_corner_orientation(t_before, self.map.get_case(x, y), t_after)
        draw_surface = pygame.Surface((w, h)).convert_alpha()
        transparent = (0, 0, 0, 0)
        draw_surface.fill(transparent)

        if o == (1, 1):
            pygame.draw.circle(draw_surface, self.color, (w, h), 0.8*w)
            pygame.draw.circle(draw_surface, transparent, (w, h), 0.1*w)
        if o == (1, -1):
            pygame.draw.circle(draw_surface, self.color, (w, 0), 0.8*w)
            pygame.draw.circle(draw_surface, transparent, (w, 0), 0.1*w)
        elif o == (-1, -1):
            pygame.draw.circle(draw_surface, self.color, (0, 0), 0.8*w)
            pygame.draw.circle(draw_surface, transparent, (0, 0), 0.1*w)
        elif o == (-1, 1):
            pygame.draw.circle(draw_surface, self.color, (0, h), 0.8*w)
            pygame.draw.circle(draw_surface, transparent, (0, h), 0.1*w)
        
        pygame.Surface.blit(screen, draw_surface, (x, y))
    
    def _draw_end_tail(self, screen: pygame.Surface, x: int, y: int, w, h, t_before: Tuple[int, int]):
        draw_surface = pygame.Surface((w, h)).convert_alpha()
        draw_surface.fill((0, 0, 0, 0))

        r = round((w/2)*0.8)
        pygame.draw.circle(draw_surface, self.color, (w/2, h/2), r)
        pygame.draw.rect(draw_surface, self.color, (w/2, 0.1*h, w/2, 0.8*h))
        
        case_x, case_y = self.map.get_case(x, y)
        if case_x == t_before[0] and case_y == t_before[1] + 1:
            draw_surface = pygame.transform.rotate(draw_surface, 90)
        elif case_x == t_before[0] and case_y == t_before[1] - 1:
            draw_surface = pygame.transform.rotate(draw_surface, 270)
        elif case_x == t_before[0] + 1 and case_y == t_before[1]:
            draw_surface = pygame.transform.rotate(draw_surface, 180)

        pygame.Surface.blit(screen, draw_surface, (x, y))

    def draw(self, screen):
        head_x, head_y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        
        self._draw_head(screen, head_x, head_y, w, h)

        for i in range(self.tail_lenght):
            t = self.tail[i]
            x, y = self.map.get_pos(t[0], t[1])
            if i == 0:
                self._draw_end_tail(screen, x, y, w, h, self.tail[1])
            elif i == self.tail_lenght - 1:
                self._draw_neck(screen, x, y, w, h, head_x, head_y)
            else:
                t_before = self.tail[i-1]
                t_after = self.tail[i+1]
                
                if t_before[0] == t[0] == t_after[0]:
                    pygame.draw.rect(screen, self.color, (x + 0.1*w, y, 0.8*w, h))
                elif t_before[1] == t[1] == t_after[1]:
                    pygame.draw.rect(screen, self.color, (x, y + 0.1*h, w, 0.8*h))
                else:
                    self._draw_corner(screen, x, y, w, h, t_before, t_after)

    def down(self):
        self.dir = [0, 1]
    
    def up(self):
        self.dir = [0, -1]
    
    def right(self):
        self.dir = [1, 0]
    
    def left(self):
        self.dir = [-1, 0]
        
