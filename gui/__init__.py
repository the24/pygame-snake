from math import ceil, floor
from typing import Tuple

import pygame
from pygame import Rect, Surface

import gui.colors

_ColorValue = gui.colors._ColorValue

_IntVec2D = Tuple[int, int]

class Menu:
    
    def __init__(self, pos: _IntVec2D, size: _IntVec2D) -> None:
        self.rect = Rect(pos[0], pos[1], size[0], size[1])

    def center(self, screen: pygame.Surface) -> None:
        self.move((screen.get_width() - self.rect.width) / 2,
                  (screen.get_height() - self.rect.height) / 2)
    
    def move(self, x: int, y: int) -> None:
        self.rect.x = x
        self.rect.y = y


def draw_ellipse_angle(surface: Surface, color: _ColorValue, rect, angle, width=0):
    target_rect = Rect(rect)
    shape_surf = Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))

def get_apple_surface(size) -> Surface:
    draw_surface = Surface((size, size), pygame.SRCALPHA)
    transparent = (0, 0, 0, 0)
    draw_surface.fill(transparent)

    half_size = size/2
    r = floor(half_size * 0.85)
    offset = ceil(half_size * 0.15)

    draw_ellipse_angle(draw_surface, (22, 165, 11), (half_size, 0, offset*4, offset*2), 20)

    pygame.draw.rect(draw_surface, (165, 42, 42), (half_size - 1, 0, 3, offset*2))

    pygame.draw.circle(draw_surface, (240, 0, 0), (half_size, half_size + offset), r)

    return draw_surface
