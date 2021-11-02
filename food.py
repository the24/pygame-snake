from random import randint

from pygame import Rect

from map import Map
from object import Object
from snake import Snake


class Apple(Object):

    def __init__(self, map: Map) -> None:
        self.pos = (7, 4)
        self.map = map
        self.size = map.tile_size
        x, y = map.get_pos(self.pos[0], self.pos[1]).topleft
        super().__init__(x, y, self.size, self.size, color=(255, 0, 0))
    
    def gen_new_apple(self, snake: Snake):
        x = randint(0, self.map.width//self.map.tile_size - 1)
        y = randint(0, self.map.height//self.map.tile_size - 1)
        self.pos = (x, y)
        while self.pos in snake.tail:
            x = randint(0, self.map.width//self.map.tile_size - 1)
            y = randint(0, self.map.height//self.map.tile_size - 1)
            self.pos = (x, y)
        
        x, y = self.map.get_pos(x, y).topleft
        rect = Rect(x, y, self.size, self.size)
        self.rect = rect
