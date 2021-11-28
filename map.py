from types import NoneType
from typing import List, Tuple, Union

import pygame
from pygame import Rect, Surface

from animation import Anim, RotateAnim, ZoomAnim
from gui import ScreenObj
from object import Object

_IntVec2D = Tuple[int, int]

class Map:

    def __init__(self, size, tile_size, pos = (0, 0)) -> None:
        w = size[0] * tile_size
        h = size[1] * tile_size
        self.rect: Rect         = Rect(*pos, w, h)
        self.size: _IntVec2D    = size
        self.tile_size: int     = tile_size
        
        self.obj_list:  List[ScreenObj] = []
        self.anim_list: List[Anim]      = []
    
    def get_pos(self, x, y) -> Rect:
        x =  x * self.tile_size + self.rect.x
        y =  y * self.tile_size + self.rect.y
        return Rect(x, y, self.tile_size, self.tile_size)

    def add_object(self, obj: Object) -> None:
        x =  obj.pos[0] * self.tile_size + self.rect.x
        x += round((self.tile_size - obj._surface.get_width()) / 2)
        y =  obj.pos[1] * self.tile_size + self.rect.y
        y += round((self.tile_size - obj._surface.get_height()) / 2)
        screen_obj = ScreenObj(obj._surface.copy(), (x, y), [obj])
        self.obj_list.append(screen_obj)
    
    def remove_object(self, obj: Object) -> ScreenObj:
        for i, screen_obj in enumerate(self.obj_list):
            if screen_obj.obj_ptr[0] is obj:
                return self.obj_list.pop(i)
    
    def get_screen_obj(self, obj: Object) -> Union[ScreenObj, NoneType]:
        for screen_obj in self.obj_list:
            if screen_obj.obj_ptr[0] is obj:
                return screen_obj

        print("There is no ScreenObj associated to this Object")
    
    def draw(self, screen: Surface):
        for screen_obj in self.obj_list:
            screen.blit(screen_obj.surface, screen_obj.screen_pos)

    def handle_anim(self):
        self.anim_list = list(filter(lambda anim: not anim.ended,
                                     self.anim_list))
        for anim in self.anim_list:
            anim.anim()

            obj = anim.ptr[0]
            x, y = self.get_pos(*obj.obj_ptr[0].pos).topleft
            x += round((self.tile_size - obj.surface.get_width()) / 2)
            y += round((self.tile_size - obj.surface.get_height()) / 2)
            obj.screen_pos = (x, y)

    def obj_rotate(self, obj, duration, angle, loop = False):
        screen_obj = self.get_screen_obj(obj)
        for anim in self.anim_list:
            if screen_obj is anim.ptr[0] and isinstance(anim, RotateAnim):
                return
        
        self.anim_list.append(RotateAnim([screen_obj], duration, angle, loop))

    def obj_zoom(self, obj, duration, zoom, loop = False):
        screen_obj = self.get_screen_obj(obj)
        for anim in self.anim_list:
            if screen_obj is anim.ptr[0] and isinstance(anim, ZoomAnim):
                return
        
        self.anim_list.append(ZoomAnim([screen_obj], duration, zoom, loop))
