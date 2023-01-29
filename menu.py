import common
from time import sleep
from characters import get_character_from_character_list
import magic  # leaving this import to stop import conflict


def main_menu():
    welcome_message()
    return main_menu_options()


def welcome_message():
    print("Welcome to the game!\n"
          "Select the number from the list to proceed:\n"
          "1) Start a new adventure\n"
          "2) Continue from the save file\n"
          "3) Exit")


def main_menu_options():
    while True:
        try:
            answer = int(input(">"))
            if answer == 1:
                print("A new adventure begins")
                sleep(0.5)
                game = 1
                save_game_skip = 0  # determines if game should start from the beginning or in
                # safe place
                return game, save_game_skip
            elif answer == 2:
                common.load_save_game()
                hero = get_character_from_character_list(file=common.file_characters,
                                                         character_id=0)
                game = hero["game"]
                print(game)
                save_game_skip = 1  # determines if game should start from the beginning or in
                # safe place
                return game, save_game_skip
            elif answer == 3:
                quit()
            else:
                common.print_error_out_of_options_scope()
                main_menu_options()
        except ValueError:
            common.print_error_wrong_value()
