import pygame
import pygame_menu
from gui import Gui

pygame.init()
surface = pygame.display.set_mode((600, 400))

def set_difficulty(value, difficulty):
    # Do the job here !
    
    pass

def start_the_game():
    # Do the job here !
    gui = Gui()
    gui.start()

menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

wid = menu.add.text_input('Depth:', default='4')
menu.add.selector('Mode :', [('AI-Monte Carlo', 1), ('AI-Alpha Beta', 2), ('User', 3)], onchange=set_difficulty)
menu.add.text_input('Simulations:', default= 1000)
menu.add.text_input('Time wait for result:', default=1)

menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)


menu.mainloop(surface)