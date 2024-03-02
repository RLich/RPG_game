import json
import logging
from random import randrange
from time import sleep
from common import get_object_from_json_list_by_id, file_characters, file_current_enemy, \
    print_error_out_of_options_scope, style_text, print_error_wrong_value, player_input


def change_character_stat(character, stat, by_how_much, action):
    if character["name"] == "Hero":
        file = open(file_characters, "r")
    else:
        file = open(file_current_enemy, "r")
    file_content = json.loads(file.read())
    for creature in file_content:
        if creature["id"] == character["id"]:
            if action == "adding":
                logging.debug("Replacing old %s stat %s - %s with new stat - %s" % (
                    character["name"], stat, creature[stat], int(creature[stat] + by_how_much)))
                creature[stat] = int(creature[stat] + by_how_much)
            else:
                logging.debug("Replacing old %s stat %s - %s with new stat - %s" % (
                    character["name"], stat, creature[stat], int(creature[stat] - by_how_much)))
                creature[stat] = int(creature[stat] - by_how_much)
                if creature[stat] <= 0 and stat != "hp" and stat != "xp":
                    logging.debug("Rising %s to 1, because it cannot be lower than 1" % stat)
                    creature[stat] = 1
    dict_list = file_content
    file_content = json.dumps(dict_list, indent=4)
    file.close()

    if character["name"] == "Hero":
        with open(file_characters, "w") as outfile:
            outfile.write(file_content)
        file.close()
    else:
        with open(file_current_enemy, "w") as outfile:
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
    elif stage == "late":
        encountered_enemy_id = randrange(7, 10)
    else:
        encountered_enemy_id = 10
    enemy = get_character_from_character_list(file=file_characters,
                                              character_id=encountered_enemy_id)
    file.close()
    return enemy


def regenerate_after_combat(character):
    # Because we need an integer to calculate regeneration, and we don't really care about
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
        print("\nRegenerating %s health after combat (%s/%s)" %
              (hp_to_regen, character["hp"] + hp_to_regen, character["max_hp"]))
        change_character_stat(character=character, stat="hp", by_how_much=hp_to_regen, action="adding")
    if mp_to_regen > 0:
        print("Regenerating %s mana after combat (%s/%s)" %
              (mp_to_regen, character["mp"] + mp_to_regen, character["max_mp"]))
        change_character_stat(character=character, stat="mp", by_how_much=mp_to_regen, action="adding")


def copy_enemy_to_current_enemy_json(enemy):
    file = open(file_characters, "r")
    file_content = json.loads(file.read())
    for creature in file_content:
        if creature["id"] == enemy["id"]:
            logging.debug("Copying creature %s to the current_enemy.json file" % enemy["name"])
            file_content = json.dumps([creature], indent=4)
            file.close()
            break

    with open(file_current_enemy, "w") as outfile:
        outfile.write(file_content)
    file.close()


def check_if_level_up_ready():
    character = get_character_from_character_list(file=file_characters, character_id=0)
    xp_to_lvl_up = 10 * character["level"]
    if character["xp"] >= xp_to_lvl_up:
        print(style_text(text="\nYou feel more experienced. You are now on a whole new level",
                         style="bright"))
        sleep(0.5)
        change_character_stat(
            character=character, stat="level", action="adding", by_how_much=1)
        # returning xp to 0 at the end
        change_character_stat(
            character=character, stat="xp", action="removing", by_how_much=character["xp"])
        level_up(character=character)


def level_up(character):
    while True:
        try:
            stats_to_lvl_up = ["max_hp", "max_mp", "str", "int", "speed"]
            sleep(0.5)
            dialog = "All this killing is finally paying off. What would you like to improve about yourself?"
            options = ["10 Health(currently: %s)" % character[stats_to_lvl_up[0]],
                       "10 Mana (currently: %s)" % character[stats_to_lvl_up[1]],
                       "5 Strength (currently: %s)" % character[stats_to_lvl_up[2]],
                       "5 Intelligence (currently: %s)" % character[stats_to_lvl_up[3]],
                       "5 Speed (currently: %s)" % character[stats_to_lvl_up[4]]]
            answer = player_input(dialog, options)
            if answer in range(1, 3):
                change_character_stat(character=character, stat=(stats_to_lvl_up[answer - 1]),
                                      by_how_much=10, action="adding")
                # adding 10 hp/mana so the leveled up stats are not "empty"
                if answer == 1:
                    change_character_stat(character=character, stat="hp",
                                          by_how_much=10, action="adding")
                else:
                    change_character_stat(character=character, stat="mp",
                                          by_how_much=10, action="adding")
                break
            elif answer in range(3, 6):
                change_character_stat(character=character, stat=(stats_to_lvl_up[answer - 1]),
                                      by_how_much=5, action="adding")
                break
            else:
                print_error_out_of_options_scope()
        except ValueError:
            print_error_wrong_value()
