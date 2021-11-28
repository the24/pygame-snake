from abc import abstractmethod
from math import ceil
from typing import List

import pygame

from object import Object


class Anim:
    
    def __init__(self, obj_ptr, duration, loop = False) -> None:
        self.obj_ptr: List[Object] = obj_ptr
        self.duration = duration
        self.frame_passed = 0
        self.loop = loop
        self.ended = False
    
    def anim(self) -> None:
        if self.ended:
            return
        
        self.frame_passed += 1

        if self.frame_passed == self.duration:
            if self.loop:
                self.frame_passed = 0
            else:
                self.ended = True

class RotateAnim(Anim):

    def __init__(self,
                 obj_ptr:   List[Object],
                 duration:  int,
                 angle:     int,
                 loop:      bool = False) -> None:
        
        super().__init__(obj_ptr, duration, loop=loop)
        self.angle = angle
        self.original_surface = obj_ptr[0]._surface.copy()
    
    def anim(self) -> None:
        super().anim()
        obj = self.obj_ptr[0]
        
        angle = (self.angle / self.duration) * self.frame_passed

        rotated_surf = pygame.transform.rotate(self.original_surface, angle)
        obj._surface = rotated_surf

class ZoomAnim(Anim):

    def __init__(self,
                 obj_ptr:   List[Object],
                 duration:  int,
                 zoom:      float,
                 loop:      bool = False) -> None:
        
        super().__init__(obj_ptr, duration, loop=loop)
        self.zoom = zoom
        self.original_surface = obj_ptr[0]._surface.copy()
    
    def anim(self) -> None:
        super().anim()
        obj = self.obj_ptr[0]

        zoom = ((self.zoom - 1) / self.duration) * self.frame_passed + 1

        new_width  = self.original_surface.get_width() * zoom
        new_height = self.original_surface.get_height() * zoom
        obj._surface = pygame.transform.scale(self.original_surface, (new_width, new_height))


