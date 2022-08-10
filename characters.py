from common import working_dir
import json
import logging
from random import randrange
from common import get_object_from_json_list_by_id, file_characters


class Enemy:
    def __init__(self, id, name, hp, str, int, mp, weapon_dmg):
        self.id = id
        self.name = name
        self.health = hp
        self.strength = str
        self.intelligence = int
        self.mana = mp
        self.weapon_damage = weapon_dmg


class Hero:
    def __init__(self, id, name, hp, str, int, mp):
        self.id = id
        self.name = name
        self.health = hp
        self.strength = str
        self.intelligence = int
        self.mana = mp


def change_character_stat(character, stat, how_much, action):
    file = open(file_characters, "r")
    file_content = json.loads(file.read())
    for creature in file_content:
        if creature["id"] == character["id"]:
            logging.debug("Replacing old %s stat %s with new item's stat %s" % (
                character["name"], creature[stat], character[stat]))
            if action == "adding":
                creature[stat] = creature[stat] + how_much
            else:
                creature[stat] = creature[stat] - how_much
                if creature[stat] <= 0:
                    logging.debug("Rising %s to 1, because it cannot be lower than 1" % stat)
                    creature[stat] = 1
    dict_list = file_content
    file_content = json.dumps(dict_list, indent=4)
    file.close()

    with open(file_characters, "w") as outfile:
        outfile.write(file_content)
    file.close()


def get_character_from_character_list(file, character_id):
    characters_list = open(file, "r")
    characters_list_json = json.loads(characters_list.read())
    chosen_character = get_object_from_json_list_by_id(data=characters_list_json,
                                                       object_id=character_id)
    characters_list.close()
    return chosen_character


def choose_enemy_to_encounter(stage):
    file = open(file_characters, "r")
    if stage == "early":
        encountered_enemy_id = randrange(1, 3)
    elif stage == "mid":
        encountered_enemy_id = randrange(4, 6)
    else:
        encountered_enemy_id = randrange(7, 9)
    enemy = get_character_from_character_list(file=file_characters,
                                              character_id=encountered_enemy_id)
    file.close()
    return enemy
