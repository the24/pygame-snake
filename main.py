import pygame
from pygame.locals import *

import gui
from gui.board import Board
from map import Map
from object import Object


class Game:

    def __init__(self) -> None:
        self.playing = False
        tile_size = 36

        self.obj = Object((2, 0), gui.get_apple_surface(36))
        self.board = Board()
        self.board.center(screen)

        self.game_map = Map((10, 9), tile_size, self.board.map_pos)

    def start(self):
        self.playing = True
    
    def stop(self):
        self.playing = False

    def update(self):
        if not self.playing:
            return
        
        screen.fill((0, 0, 0))

        self.board.draw(screen)
        self.game_map.handle_anim()
        pos, surf = self.game_map.get_ui_obj(self.obj)
        screen.blit(surf, pos)

        pygame.display.flip()
    
    def handle_keys(self, keys):
        if keys[K_SPACE]: game.start()
        if keys[K_a]: self.game_map.obj_rotate(self.obj, 360, 2*60)
        # if keys[K_UP] and not game.snake.dir == [0, 1]: game.snake.up()
        # if keys[K_DOWN] and not game.snake.dir == [0, -1]: game.snake.down()
        # if keys[K_RIGHT] and not game.snake.dir == [-1, 0]: game.snake.right()
        # if keys[K_LEFT] and not game.snake.dir == [1, 0]: game.snake.left()


if __name__ == "__main__":
    pygame.init()

    size = width, height = 720, 480

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    
    lauched = True
    game = Game()

    while lauched:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: lauched = False

            keys = pygame.key.get_pressed()
            game.handle_keys(keys)
        
        clock.tick(60)
        game.update()
