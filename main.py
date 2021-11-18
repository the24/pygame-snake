import pygame
from pygame.locals import *

import gui
from game import Apple, Snake
from gui import Board

pygame.init()

size = width, height = 720, 480

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

class Game:

    def __init__(self) -> None:
        gui.init_font("Roboto", 32)

        self.board = Board()
        self.board.center(screen)
        self.started = False

        self.snake = Snake(self.board.map)
        self.apple = Apple(self.board.map)
        self.board.map._objects.append(self.snake)
        self.board.map._objects.append(self.apple)
        

    def start(self):
        self.started = True
    
    def stop(self):
        self.started = False

    def update(self):
        if self.started:
            self.board.draw(screen, self.snake.tail_lenght)
        
        if self.snake.rect.collidepoint(self.apple.rect.center):
            self.snake.eat()
            self.apple.gen_new_apple(self.snake)
        
        self.snake.update()



lauched = True
game = Game()

while lauched:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: lauched = False

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]: game.start()
        if keys[K_UP] and not game.snake.dir == [0, 1]: game.snake.up()
        if keys[K_DOWN] and not game.snake.dir == [0, -1]: game.snake.down()
        if keys[K_RIGHT] and not game.snake.dir == [-1, 0]: game.snake.right()
        if keys[K_LEFT] and not game.snake.dir == [1, 0]: game.snake.left()
    
    screen.fill((0, 0, 0))
    game.update()
    pygame.display.flip()
    clock.tick(60)
