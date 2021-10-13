import pygame
from board import Board

from map import Map
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



lauched = True
game = Game()

while lauched:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: lauched = False
        if event.type == pygame.KEYDOWN: game.start()
    
    game.update()
    pygame.display.flip()
    clock.tick(60)