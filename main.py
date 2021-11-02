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
            self.board.update()
    
    def snake(self) -> Snake:
        return self.board.snake



lauched = True
game = Game()

while lauched:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: lauched = False

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]: game.start()
        if keys[K_UP] and not game.snake().dir == [0, 1]: game.snake().up()
        if keys[K_DOWN] and not game.snake().dir == [0, -1]: game.snake().down()
        if keys[K_RIGHT] and not game.snake().dir == [-1, 0]: game.snake().right()
        if keys[K_LEFT] and not game.snake().dir == [1, 0]: game.snake().left()
    
    screen.fill((0, 0, 0))
    game.update()
    pygame.display.flip()
    clock.tick(60)
