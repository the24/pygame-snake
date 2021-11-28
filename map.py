from typing import List, Tuple

import pygame
from pygame import Rect, Surface

from animation import Anim, RotateAnim, ZoomAnim
from object import Object

_IntVec2D = Tuple[int, int]

class Tile:
    
    def __init__(self) -> None:
        pass

class Map:

    def __init__(self, size, tile_size, pos = (0, 0)) -> None:
        w = size[0] * tile_size
        h = size[1] * tile_size
        self.rect = Rect(*pos, w, h)
        self.size = size
        self.tile_size = tile_size
        
        self.anim_list: List[Anim] = []
    
    def get_ui_obj(self, obj: Object) -> Tuple[_IntVec2D, Surface]:
        x =  obj.pos[0] * self.tile_size + self.rect.x
        x += round((self.tile_size - obj._surface.get_width()) / 2)
        y =  obj.pos[1] * self.tile_size + self.rect.y
        y += round((self.tile_size - obj._surface.get_height()) / 2)

        return ((x, y), obj._surface)

    def handle_anim(self):
        self.anim_list = list(filter(lambda anim: not anim.ended,
                                     self.anim_list))
        for anim in self.anim_list:
            anim.anim()

    def obj_rotate(self, obj, duration, angle, loop = False):
        for anim in self.anim_list:
            if obj is anim.obj_ptr[0] and isinstance(anim, RotateAnim):
                return
        
        self.anim_list.append(RotateAnim([obj], duration, angle, loop))

    def obj_zoom(self, obj, duration, zoom, loop = False):
        for anim in self.anim_list:
            if obj is anim.obj_ptr[0] and isinstance(anim, ZoomAnim):
                return
        
        self.anim_list.append(ZoomAnim([obj], duration, zoom, loop))
