from abc import abstractmethod
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
    
    @abstractmethod
    def anim(self) -> None:
        pass

class RotateAnim(Anim):

    def __init__(self, obj_ptr: List[Object], duration, angle, loop=False) -> None:
        super().__init__(obj_ptr, duration, loop=loop)
        self.angle = angle
        self.original_surface = obj_ptr[0]._surface.copy()
    
    def anim(self) -> None:
        # TODO: Handle zoom distortion
        if self.ended:
            return
        
        if self.frame_passed >= self.duration and not self.loop:
            self.ended = True
        
        angle = (self.angle / self.duration) * self.frame_passed

        width = self.obj_ptr[0]._surface.get_width()
        height = self.obj_ptr[0]._surface.get_height()

        rotated_surf = pygame.transform.rotate(self.original_surface, angle)
        self.obj_ptr[0]._surface = pygame.transform.scale(rotated_surf, (width, height))

        self.frame_passed += 1
