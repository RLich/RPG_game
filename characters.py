from common import working_dir
import json
import logging
from random import randrange
from common import get_object_from_json_list_by_id, file_characters


def change_character_stat(character, stat, how_much, action):
    file = open(file_characters, "r")
    file_content = json.loads(file.read())
    for creature in file_content:
        if creature["id"] == character["id"]:
            logging.debug("Replacing old %s stat %s with new item's stat %s" % (
                character["name"], creature[stat], character[stat]))
            if action == "adding":
                creature[stat] = int(creature[stat] + how_much)
            else:
                creature[stat] = int(creature[stat] - how_much)
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
    # reminder: "randrange" second argument is stop, which means it stops on the given number
    # WITHOUT including it. So randrange(1, 4) will return 1, 2 or 3
    if stage == "early":
        encountered_enemy_id = randrange(1, 4)
    elif stage == "mid":
        encountered_enemy_id = randrange(4, 7)
    else:
        encountered_enemy_id = randrange(7, 10)
    enemy = get_character_from_character_list(file=file_characters,
                                              character_id=encountered_enemy_id)
    file.close()
    return enemy


def regenerate_after_combat(character):
    # Because we need an integer to calculate regeneration and we don't really care about
    # whatever is after number's dot, we dispose of it by converting hp_to_regen to a string,
    # cutting of the after-dot-tail and swapping back to integer before using
    regen_rate = 0.1
    hp_to_regen = str(character["max_hp"] * regen_rate)
    hp_to_regen = int(hp_to_regen.split(".", 2)[0])
    if hp_to_regen > character["max_hp"]:
        hp_to_regen = character["max_hp"] - character["hp"]
    elif character["hp"] == character["max_hp"]:
        hp_to_regen = 0

    mp_to_regen = str(character["max_mp"] * regen_rate)
    mp_to_regen = int(mp_to_regen.split(".", 2)[0])
    if mp_to_regen > character["max_mp"]:
        mp_to_regen = character["max_mp"] - character["mp"]
    elif character["mp"] == character["max_mp"]:
        mp_to_regen = 0

    if hp_to_regen > 0:
        print("\nRegenerating %s hp after combat" % hp_to_regen)
        change_character_stat(character=character, stat="hp", how_much=hp_to_regen, action="adding")
    if mp_to_regen > 0:
        print("Regenerating %s mp after combat" % mp_to_regen)
        change_character_stat(character=character, stat="mp", how_much=mp_to_regen, action="adding")
