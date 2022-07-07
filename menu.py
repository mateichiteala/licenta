import pygame
import pygame_menu
from gui import Gui

pygame.init()
surface = pygame.display.set_mode((512, 512))

def set_difficulty_white(value, index):
    if index==0:
        white_depth.hide()
        white_sim.hide()
        white_time.hide()

    if index==1:
        white_depth.show()
        white_sim.show()
        white_time.show()
    if index==2:
        white_depth.show()
        white_sim.hide()
        white_time.show()


def set_difficulty_black(value, index):
    if index==0:
        black_depth.hide()
        black_sim.hide()
        black_time.hide()

    if index==1:
        black_depth.show()
        black_sim.show()
        black_time.show()
    if index==2:
        black_depth.show()
        black_sim.hide()
        black_time.show()


def start_the_game():
    _white_time = int(white_time.get_value())
    _black_time = int(black_time.get_value()) 


    playerOne_dict = {"player": 0}
    playerOne = white.get_value()[1]
    if playerOne == 1:
        playerOne_dict["player"] = 1
        playerOne_dict["ai"]={
            "depth": int(white_depth.get_value()),
            "simulations": int(white_sim.get_value()),
            "time": _white_time
        }
    if playerOne == 2:
        playerOne_dict["player"] = 2
        playerOne_dict["ai"]={
            "depth":  int(white_depth.get_value()),
            "time": _white_time
        }

    playerTwo_dict = {"player": 0}
    playerTwo = black.get_value()[1]
    if playerTwo == 1:
        playerTwo_dict["player"] = 1
        playerTwo_dict["ai"]={
            "depth":  int(black_depth.get_value()),
            "simulations": int(black_sim.get_value()),
            "time": _black_time
        }
    if playerTwo == 2:
        playerTwo_dict["player"] = 2
        playerTwo_dict["ai"]={
            "depth":  int(black_depth.get_value()),
            "time": _black_time
        }

    # board_type = board.get_value()[1]
    gui = Gui(playerOne_dict, playerTwo_dict, 0)
    gui.start()

menu = pygame_menu.Menu('Welcome', 512, 512,
                       theme=pygame_menu.themes.THEME_BLUE)

valid_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
white = menu.add.selector('White:', [('User', 0), ('AI-Monte Carlo', 1), ('AI-Alpha Beta', 2)], onchange=set_difficulty_white)
white_depth = menu.add.text_input('Depth White:', default=4, valid_chars=valid_chars).hide()
white_sim = menu.add.text_input('Simulations white:', default=1000, valid_chars=valid_chars).hide()
white_time = menu.add.text_input('Time wait for result white:', default=0, valid_chars=valid_chars).hide()

black = menu.add.selector('Black :', [('User', 0), ('AI-Monte Carlo', 1), ('AI-Alpha Beta', 2)], onchange=set_difficulty_black)
black_depth = menu.add.text_input('Depth Black:', default=4, valid_chars=valid_chars).hide()
black_sim = menu.add.text_input('Simulations black:', default=1000, valid_chars=valid_chars).hide()
black_time = menu.add.text_input('Time wait for result black:', default=0, valid_chars=valid_chars).hide()

board = menu.add.selector('Board:', [('Standard', 0), ('endGame1', 1), ('endGame', 2)])



menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)


menu.mainloop(surface)