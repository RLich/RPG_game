import common
from time import sleep
import magic


def main_menu():
    welcome_message()
    main_menu_options()


def welcome_message():
    print("Welcome to the game!\n"
          "Select the number from the list to proceed:\n"
          "1) Start a new adventure\n"
          "2) Continue from the save file (not implemented yet)\n"
          "3) Exit")


def main_menu_options():
    while True:
        try:
            answer = int(input(">"))
            if answer == 1:
                print("A new adventure begins")
                sleep(0.5)
                break

            elif answer == 2:
                print("Not implemented yet")
                sleep(1)
            elif answer == 3:
                quit()
            else:
                common.print_error_out_of_options_scope()
                main_menu_options()
        except ValueError:
            common.print_error_wrong_value()
