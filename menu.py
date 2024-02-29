from common import load_save_game, file_characters, player_input, clean_console_after_confirmation
from time import sleep
from characters import get_character_from_character_list
import magic  # leaving this import to stop import conflict


def main_menu():
    return main_menu_options()


def main_menu_options():
    while True:
        dialog = "Welcome to the game!\nSelect the number from the list to proceed:"
        options = [
                   "Start a new adventure",
                   "Continue from the save file",
                   "Exit"
        ]
        answer = player_input(dialog, options)
        if answer == 1:
            print("A new adventure begins")
            sleep(0.5)
            encounter_counter = 1
            game_loaded = False  # determines if game should start from the beginning or in
            # safe place
            return encounter_counter, game_loaded
        elif answer == 2:
            load_save_game()
            hero = get_character_from_character_list(file=file_characters,
                                                     character_id=0)
            encounter_counter = hero["encounter"]
            print(encounter_counter)
            game_loaded = True  # determines if game should start from the beginning or in
            # safe place
            return encounter_counter, game_loaded
        elif answer == 3:
            quit()
