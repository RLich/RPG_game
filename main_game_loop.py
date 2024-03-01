import menu
import logging
from characters import choose_enemy_to_encounter, get_character_from_character_list, \
    file_characters, regenerate_after_combat, check_if_level_up_ready, change_character_stat
from combat import fight
from shop import shop_welcome
from common import reset_all_jsons, style_text, file_items, \
    file_weapons, create_save_data, player_input, delete_save_data
from inventory import use_item, change_equipped_weapon, get_inventory
from time import sleep
from magic import cast_spell, get_spellbook
from items import populate_weapons_shop_list, clear_weapons_shop_list_json
from settings import game_length


def main_loop(restarted):
    reset_all_jsons()
    if restarted is True:
        encounter_counter = 1
        is_game_loaded_from_save = False
    else:
        answer_main_menu = menu.main_menu_options()
        encounter_counter = answer_main_menu[0]
        is_game_loaded_from_save = answer_main_menu[1]
    while encounter_counter <= game_length:
        if is_game_loaded_from_save is True:
            pass  # when loading a game, skips the enemy encounter so that player starts from the
            # safe place instead of combat
        else:
            if enemy_encounter(counter=encounter_counter, hero=get_character_from_character_list(
                    file=file_characters, character_id=0)) is False:  # it's false if player escaped
                encounter_counter -= 1
            check_if_level_up_ready()
            sleep(1)
        after_combat_break()
        if encounter_counter == 3 or encounter_counter == 6 or encounter_counter == 9 or encounter_counter == 12:
            populate_weapons_shop_list()
            shop_welcome()
            clear_weapons_shop_list_json()
        encounter_counter += 1
        is_game_loaded_from_save = 0  # sets this value to 0 to not skip the enemy encounter
    print("Congratulations, you have won the game. Feedback is welcomed :)")


def enemy_encounter(counter, hero):
    while True:
        logging.debug("!!!Game counter: %s" % counter)
        stage = determine_game_stage(counter)
        enemy = choose_enemy_to_encounter(stage=stage)
        print("You encounter " + style_text(enemy["name"], style="bright") + " on your path")
        sleep(0.5)
        if fight(hero=hero, enemy=enemy) is False:
            return False
        regenerate_after_combat(character=get_character_from_character_list(
            file=file_characters, character_id=0))
        change_character_stat(character=hero, stat="xp", by_how_much=enemy["xp"], action="adding")
        print("You have gained %s experience points (%s/%s)"
              % (enemy["xp"], hero["xp"] + enemy["xp"], hero["level"] * 10))
        break


def determine_game_stage(counter):
    if counter in [1, 2, 3]:
        stage = "early"
    elif counter in [4, 5, 6]:
        stage = "mid"
    else:
        stage = "late"
    return stage


def after_combat_break():
    while True:
        hero = get_character_from_character_list(file=file_characters, character_id=0)
        dialog = "You are resting in a quiet place. What would you like to do?"
        options = [
            "Continue with your journey",
            "Use an item",
            "Change equipped weapon",
            "Cast a spell",
            "Examine your character",
            "Browse your inventory",
            "Browse your spellbook",
            "Save your progress"]
        answer = player_input(dialog, options)
        if answer == 1:
            break
        elif answer == 2:
            use_item(character=hero)
        elif answer == 3:
            change_equipped_weapon()
        elif answer == 4:
            cast_spell(attacker=hero, defender=hero, camp=True)
        elif answer == 5:
            print("\nYou take a closer look at yourself:"
                  "\nHealth: %s/%s"
                  "\nMana: %s/%s"
                  "\nStrength: %s"
                  "\nIntelligence: %s"
                  "\nSpeed: %s"
                  "\nLevel: %s"
                  "\nExperience: %s/%s\n"
                  % (hero["hp"], hero["max_hp"], hero["mp"], hero["max_mp"], hero["str"],
                     hero["int"], hero["speed"], hero["level"], hero["xp"], hero["level"] * 10))
            input("--Press any button to continue--")
        elif answer == 6:
            weapons = get_inventory(file=file_weapons)
            items = get_inventory(file=file_items)
            print("\nGold: %s"
                  "\nHealth potions: %s"
                  "\nMana potions: %s" % (items[0]["quantity"], items[1]["quantity"],
                                          items[2]["quantity"]))
            for weapon in weapons:
                print("%s: %s damage (worth: %sg)" % (weapon["name"], weapon["damage"],
                                                      weapon["value"]))
            input("--Press any button to continue--")
        elif answer == 7:
            spellbook = get_spellbook()
            print("You open up your spellbook:")
            for spell in spellbook:
                if spell["quantity"] == 1 and spell["healing"] is True:
                    print("%s: %s healing power (mana cost: %s)" % (spell["name"],
                                                                    spell["power"],
                                                                    spell["mana_cost"]))
                elif spell["quantity"] == 1 and spell["healing"] is False:
                    print("%s: %s damaging power (mana cost: %s)" % (spell["name"],
                                                                     spell["power"],
                                                                     spell["mana_cost"]))
            input("--Press any button to continue--")
        elif answer == 8:
            create_save_data()


def restart_if_desired():
    delete_save_data()
    sleep(1)
    dialog = "Restart the game?"
    options = ["Yes", "No"]
    answer = player_input(dialog, options)
    if answer == 1:
        from main_game_loop import main_loop
        main_loop(restarted=True)
    else:
        quit()


main_loop(restarted=False)
