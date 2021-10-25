import pygame
from pygame.locals import *

from board import Board
from snake import Snake

pygame.init()

size = width, height = 720, 480

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

class Game:

    def __init__(self) -> None:
        self.board = Board()
        self.started = False
        self.board.center(screen)
        

    def start(self):
        self.started = True
    
    def stop(self):
        self.started = False

    def update(self):
        if self.started:
            self.board.draw(screen)
            self.snake().update()
    
    def snake(self) -> Snake:
        return self.board.map.snake



lauched = True
game = Game()

while lauched:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: lauched = False

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]: game.start()
        if keys[K_UP]: game.snake().up()
        if keys[K_DOWN]: game.snake().down()
        if keys[K_RIGHT]: game.snake().right()
        if keys[K_LEFT]: game.snake().left()
    
    screen.fill((0, 0, 0))
    game.update()
    pygame.display.flip()
    clock.tick(60)