from characters import change_character_stat, get_character_from_character_list, \
    copy_enemy_to_current_enemy_json
from random import choice, randrange
from common import print_error_out_of_options_scope, color_text, style_text, file_characters, \
    file_current_enemy, print_error_wrong_value, delete_save_data, player_input
import inventory
import loot
import logging
import magic
from time import sleep


def fight(hero, enemy):
    sleep(1)
    print(style_text(hero["name"], style="bright") + " vs " + style_text(enemy["name"],
                                                                         style="bright"))
    copy_enemy_to_current_enemy_json(enemy=enemy)
    if turn(hero, enemy) is False:
        return False  # returning False if player escaped combat


def turn(hero, enemy):
    counter = 1
    while hero["hp"] >= 1 and enemy["hp"] >= 1:
        hero = get_character_from_character_list(file=file_characters, character_id=0)
        enemy = get_character_from_character_list(file=file_current_enemy, character_id=enemy["id"])
        print("\nTurn " + style_text(counter, style="bright") + " begins")
        print("%s HP: %s" % (style_text(hero["name"], style="bright"), hero["hp"]))
        print("%s HP: %s" % (style_text(enemy["name"], style="bright"), enemy["hp"]))
        if decide_if_hero_goes_first(hero=hero, enemy=enemy) is True:
            print("\nInitiative is on your side")
            if choose_action(hero, enemy) is False:
                return False  # returning False if player escaped combat
            if is_enemy_dead(enemy) is True:
                loot.loot_handling_after_combat(enemy)
                break
            enemy_action = enemy_choose_action()
            counter += 1
            if enemy_action == 1:
                do_basic_attack(attacker=enemy, defender=hero)
            if is_hero_dead() is True:
                restart_if_desired()
                break

        else:
            print("\nYour enemy moves first")
            enemy_action = enemy_choose_action()
            counter += 1
            if enemy_action == 1:
                do_basic_attack(attacker=enemy, defender=hero)
                print("You have %s health left" % get_character_from_character_list(
                    file=file_characters, character_id=0)["hp"])
            if is_hero_dead() is True:
                restart_if_desired()
                break
            if choose_action(hero, enemy) is False:
                return False  # returning False if player escaped combat
            if is_enemy_dead(enemy) is True:
                loot.loot_handling_after_combat(enemy)
                break


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


def choose_action(hero, enemy):
    while True:
        try:
            sleep(1)
            dialog = "Choose an action to perform:"
            options = [
                  "Attack with your weapon",
                  "Cast a spell",
                  "Use an item",
                  "Try to retreat(50%)"
            ]
            action = player_input(dialog, options)
            if action == 1:
                do_basic_attack(attacker=hero, defender=enemy)
                break
            elif action == 2:
                action = magic.cast_spell(attacker=hero, defender=enemy, camp=False)
                if action is not False:
                    break
            elif action == 3:
                action = inventory.use_item(character=hero)
                if action is not False:
                    break
            elif action == 4:
                retreat_roll = choice([1, 2])
                if retreat_roll == 1:
                    sleep(1)
                    print("Retreat successful")
                    return False  # returning False if player escaped combat
                else:
                    sleep(1)
                    print("Retreat failed")
                    break
            else:
                print_error_out_of_options_scope()
        except ValueError:
            print_error_wrong_value()


def enemy_choose_action():
    sleep(1)
    print("Enemy performs an attack")
    return 1


def calculate_spell_power(attacker, spell):
    standard_roll = choice([1, 2, 3, 4, 5, 6])
    if isinstance(spell["power"], int) is True:
        damage = attacker["int"] + spell["power"] + standard_roll
    else:
        damage_string_split = spell["power"].split("d")
        power = int(damage_string_split[1]) + 1
        damage_from_dices_list = []
        number_of_dices = int(damage_string_split[0]) + 1
        for dice in range(1, number_of_dices):
            roll = randrange(1, power)
            damage_from_dices_list.append(roll)
        sum_of_damage_from_dices = sum(damage_from_dices_list)
        damage = attacker["int"] + standard_roll + sum_of_damage_from_dices
    return damage


def do_basic_attack(attacker, defender):
    damage = calculate_damage(attacker=attacker)
    sleep(1)
    print("\n%s dealt %s to %s" % (style_text(attacker["name"], style="bright"),
                                   color_text("%s physical damage" % damage, color="red"),
                                   style_text(defender["name"], style="bright")))
    change_character_stat(character=defender, stat="hp", by_how_much=damage, action="removing")


def calculate_damage(attacker):
    if attacker["name"] == "Hero":
        equipped_weapon = inventory.get_equipped_weapon()
        weapon_damage = equipped_weapon["damage"]
        print("You are attacking with %s" % equipped_weapon["name"])
    else:
        weapon_damage = attacker["weapon_dmg"]
    armor = 0
    roll = choice([1, 2, 3, 4, 5, 6])
    damage = (roll + attacker["str"] + weapon_damage) - armor
    logging.debug("Calculating damage:\n   roll(d6): %s\n   strength: %s\n   weapon's damage: "
                  "%s\n   armor: %s\nTotal damage: %s" % (roll, attacker["str"], weapon_damage,
                                                          armor, damage))
    if damage <= 0:
        damage = 1
        logging.debug("Damage cannot be lower than 1. Adjusting")
    return damage


def decide_if_hero_goes_first(hero, enemy):
    roll_hero = randrange(1, 7)
    roll_enemy = randrange(1, 7)
    logging.debug("Initiative roll:\nHero: %s\nEnemy: %s" % (roll_hero, roll_enemy))
    if roll_hero + hero["speed"] >= roll_enemy + enemy["speed"]:  # greater or equal :wink:
        return True


def is_hero_dead():
    hero = get_character_from_character_list(file=file_characters, character_id=0)
    if hero["hp"] <= 0:
        print("You are dead. Your journey has ended")
        return True


def is_enemy_dead(enemy):
    enemy = get_character_from_character_list(file=file_current_enemy, character_id=enemy["id"])
    if enemy["hp"] <= 0:
        print("\nYour foe is vanquished!\n")
        return True
