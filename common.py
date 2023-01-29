import os
from json import dumps
import logging
from colorama import Fore, Style, init
from time import sleep
import shutil
#import logging_on  # enables debug logs, requires file that is in git ignore
init()  # without init, colorama doesnt seem to work in windows cmd

working_dir = os.getcwd() + "\\"


def print_error_out_of_options_scope():
    print(color_text("Please choose a number within given options\n", color="red"))
    sleep(0.5)


def print_error_wrong_value():
    print(color_text("Please use a number\n", color="red"))
    sleep(0.5)


def get_object_from_json_list_by_id(data, object_id):
    for object in data:
        if object["id"] == object_id:
            return object
    else:
        print("Object with ID: %s not found in %s" % (object_id, data))


def color_text(text, color):
    # returns text in a color chosen from the dict
    colors = {"red": Fore.RED, "green": Fore.GREEN, "blue": Fore.BLUE, "white": Fore.WHITE,
              "yellow": Fore.YELLOW, "magenta": Fore.MAGENTA, "cyan": Fore.CYAN}
    if color in colors.keys():
        chosen_color = colors[color]
    else:
        chosen_color = Fore.BLACK
    return chosen_color + str(text) + Style.RESET_ALL


def style_text(text, style):
    # returns text in style chosen from the dict
    styles = {"dim": Style.DIM, "bright": Style.BRIGHT}
    if style in styles.keys():
        chosen_style = styles[style]
    else:
        chosen_style = Style.NORMAL
    return chosen_style + str(text) + Style.RESET_ALL


items_list = [
    {
        "id": 0,
        "name": "Gold",
        "value": 1,
        "quantity": 10
    },
    {
        "id": 1,
        "name": "Health potion",
        "value": 10,
        "restore": 10,
        "quantity": 3
    },
{
        "id": 2,
        "name": "Mana potion",
        "value": 10,
        "restore": 10,
        "quantity": 3
    }
]

spells_list = [
    {
        "id": 1,
        "name": "Firebolt",
        "power": 6,
        "mana_cost": 2,
        "value": 10,
        "quantity": 1,
        "combat": True,
        "camp": False,
        "healing": False
    },
    {
        "id": 2,
        "name": "Fireball",
        "power": 12,
        "mana_cost": 4,
        "value": 20,
        "quantity": 0,
        "combat": True,
        "camp": False,
        "healing": False
    },
    {
        "id": 3,
        "name": "Elemental Missiles",
        "power": "6d6",
        "mana_cost": 5,
        "value": 30,
        "quantity": 0,
        "combat": True,
        "camp": False,
        "healing": False
    },
{
        "id": 4,
        "name": "Healing Light",
        "power": 5,
        "mana_cost": 2,
        "value": 20,
        "quantity": 0,
        "combat": True,
        "camp": True,
        "healing": True
    }
]

weapons_list = [
    {
        "id": 0,
        "name": "Trusty knife",
        "damage": 3,
        "value": 5
    }
]

characters_list = [
    {
        "id": 0,
        "game": 1,
        "name": "Hero",
        "hp": 20,
        "max_hp": 20,
        "str": 5,
        "int": 5,
        "mp": 10,
        "speed": 5,
        "xp": 0,
        "level": 1,
        "max_mp": 10
    },
    {
        "id": 1,
        "name": "Goblin",
        "hp": 5,
        "str": 5,
        "int": 3,
        "mp": 3,
        "speed": 7,
        "weapon_dmg": 3,
        "xp": 5,
        "max_hp": 5
    },
    {
        "id": 2,
        "name": "Zombie",
        "hp": 12,
        "str": 10,
        "int": 1,
        "mp": 1,
        "speed": 2,
        "weapon_dmg": 0,
        "xp": 5,
        "max_hp": 12
    },
    {
        "id": 3,
        "name": "Bandit",
        "hp": 10,
        "str": 7,
        "int": 5,
        "mp": 5,
        "speed": 5,
        "weapon_dmg": 3,
        "xp": 5,
        "max_hp": 10
    },
    {
        "id": 4,
        "name": "Marauder",
        "hp": 15,
        "str": 10,
        "int": 8,
        "mp": 8,
        "speed": 5,
        "weapon_dmg": 5,
        "xp": 10,
        "max_hp": 15
    },
    {
        "id": 5,
        "name": "Young Orc",
        "hp": 18,
        "str": 10,
        "int": 10,
        "mp": 10,
        "speed": 6,
        "weapon_dmg": 5,
        "xp": 10,
        "max_hp": 10
    },
    {
        "id": 6,
        "name": "Skeleton Warrior",
        "hp": 12,
        "str": 8,
        "int": 5,
        "mp": 5,
        "speed": 4,
        "weapon_dmg": 8,
        "xp": 10,
        "max_hp": 12
    },
    {
        "id": 7,
        "name": "Hobgoblin",
        "hp": 10,
        "str": 7,
        "int": 5,
        "mp": 5,
        "speed": 6,
        "weapon_dmg": 10,
        "xp": 15,
        "max_hp": 10
    },
    {
        "id": 8,
        "name": "Orc",
        "hp": 22,
        "str": 12,
        "int": 5,
        "mp": 5,
        "speed": 5,
        "weapon_dmg": 7,
        "xp": 15,
        "max_hp": 22
    },
    {
        "id": 9,
        "name": "Meat Golem",
        "hp": 30,
        "str": 20,
        "int": 5,
        "mp": 5,
        "speed": 1,
        "weapon_dmg": 0,
        "xp": 15,
        "max_hp": 30
    }
]

current_enemy_list = "Place to do stuff to enemy in combat"
files_list = ["characters_list.json",
              "spells_list.json",
              "weapons_list.json",
              "items_list.json",
              "weapons_shop_list.json",
              "current_enemy.json"]
file_characters = working_dir + files_list[0]
file_spells = working_dir + files_list[1]
file_weapons = working_dir + files_list[2]
file_items = working_dir + files_list[3]
file_shop_weapons = working_dir + files_list[4]
file_current_enemy = working_dir + files_list[5]
savegame = working_dir + "savegames\\"


def reset_all_jsons():
    original_files_list = [
        spells_list, items_list, weapons_list, characters_list, current_enemy_list]
    counter = 0
    for file in [file_spells, file_items, file_weapons, file_characters, file_current_enemy]:
        logging.debug("Restoring original values in file: %s" % file)
        replace_file_content(file=file, content=original_files_list[counter])
        counter += 1


def replace_file_content(file, content):
    with open(file, "w") as outfile:
        file_content = dumps(content, indent=4)
        outfile.write(file_content)


def create_save_data():
    print("Saving game...")
    for file in files_list:
        logging.debug("Copying json file %s to a savegame location" % file)
        shutil.copy(working_dir + file, savegame)
    sleep(1)
    print("Game saved")


def delete_save_data():
    if os.path.exists(savegame + "\\weapons_list.json"):
        for file in files_list:
            logging.debug("Deleting json file %s from a savegame location" % file)
            os.remove(savegame + file)


def load_save_game():
    if os.path.exists(savegame + "\\weapons_list.json"):
        print("Loading game...")
        for file in files_list:
            logging.debug("Copying json file %s to a game location" % file)
            shutil.copy(savegame + file, working_dir)
        sleep(1)
        print("Game loaded")
