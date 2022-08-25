from characters import change_character_stat, get_character_from_character_list, \
    copy_enemy_to_current_enemy_json
from random import choice
from common import print_error_out_of_options_scope, color_text, style_text, file_characters, \
    file_current_enemy
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
    turn(hero, enemy)


def turn(hero, enemy):
    counter = 1
    while hero["hp"] >= 1 and enemy["hp"] >= 1:
        hero = get_character_from_character_list(file=file_characters, character_id=0)
        enemy = get_character_from_character_list(file=file_current_enemy, character_id=enemy["id"])
        print("\nTurn " + style_text(counter, style="bright") + " begins")
        print("%s HP: %s" % (style_text(hero["name"], style="bright"), hero["hp"]))
        print("%s HP: %s" % (style_text(enemy["name"], style="bright"), enemy["hp"]))
        choose_action(hero, enemy)
        if is_enemy_dead(enemy) is True:
            loot.loot_handling_after_combat(enemy)
            break
        enemy_action = enemy_choose_action()
        counter += 1
        if enemy_action == 1:
            do_basic_attack(attacker=enemy, defender=hero)
        if is_hero_dead() is True:
            quit()


def choose_action(hero, enemy):
    while True:
        sleep(1)
        print("\nChoose an action to perform:\n"
              "1) Attack with your weapon\n"
              "2) Cast a spell\n"
              "3) Use an item\n"
              "4) Try to retreat(50%) - not fully supported at the moment")
        action = int(input(">"))
        if action == 1:
            do_basic_attack(attacker=hero, defender=enemy)
            break
        elif action == 2:
            action = cast_spell(attacker=hero, defender=enemy)
            if action is not False:
                break
        elif action == 3:
            action = inventory.use_item(character=hero)
            if action is not False:
                break
        elif action == 4:
            retreat_roll = choice([2]) # changed for debugging purposes
            if retreat_roll == 1:
                sleep(1)
                print("Retreat successful")
                # add a skip fight mechanic
                quit()
            else:
                sleep(1)
                print("Retreat failed")
                break
        else:
            print_error_out_of_options_scope()


def enemy_choose_action():
    sleep(1)
    print("Enemy performs an attack")
    return 1


def cast_spell(attacker, defender):
    while True:
        spell = magic.choose_spell_to_cast(spellbook=magic.get_spellbook())
        # spell is False when player decided to go back from spell selection
        if spell is False:
            return False
        was_enough_mana = magic.spend_mana_to_cast_spell(caster=attacker, spell=spell)
        # no mana to cast -> no casting -> do another iteration
        if was_enough_mana is False and attacker["name"] == "Hero":
            pass
        # no mana to cast + caster is not hero -> make AI decide what to do next
        elif was_enough_mana is False and attacker["name"] != "Hero":
            pass
            # WONT WORK, NEED IMPLEMENTING ENEMY MAGIC USAGE
        else:
            damage = calculate_spell_damage(attacker=attacker, spell=spell)
            sleep(0.5)
            print("\n%s dealt %s to %s" % (style_text(attacker["name"], style="bright"),
                                         color_text("%s magic damage" % damage, color="blue"),
                                         defender["name"]))
            change_character_stat(character=defender, stat="hp", how_much=damage, action="removing")
            break


def calculate_spell_damage(attacker, spell):
    roll = choice([1, 2, 3, 4, 5, 6])
    if isinstance(spell["damage"], int) is True:
        damage = attacker["int"] + spell["damage"] + roll
    else:
        damage_string_split = spell["damage"].split("d")
        damage_range_list = []
        counter = 1
        while counter <= int(damage_string_split[1]):
            damage_range_list.append(counter)
            counter += 1
        additional_roll = choice(damage_range_list)
        spell_damage_roll = int(damage_string_split[0]) * int(additional_roll + roll)
        damage = attacker["int"] + spell_damage_roll
    return damage


def do_basic_attack(attacker, defender):
    damage = calculate_damage(attacker=attacker)
    sleep(1)
    print("\n%s dealt %s to %s" % (style_text(attacker["name"], style="bright"),
                                 color_text("%s physical damage" % damage, color="red"),
                                 style_text(defender["name"], style="bright")))
    change_character_stat(character=defender, stat="hp", how_much=damage, action="removing")


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
                  "%s\n   armor: %s" % (roll, attacker["str"], weapon_damage, armor))
    if damage <= 0:
        damage = 1
        logging.debug("Damage cannot be lower than 1. Adjusting")
    return damage


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
