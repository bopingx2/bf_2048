import pygame
from pygame.locals import *

from utils import play

if __name__ == "__main__" :
    pygame.init()
    pygame.display.set_caption('2048')
    play()
    pygame.quit()
    