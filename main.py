import pygame
from pygame.locals import *

# Inport logic from utils
from utils import play

if __name__ == "__main__" :
    pygame.init()
    pygame.display.set_caption('2048')
    # Call play function to start
    play()
    pygame.quit()
    
