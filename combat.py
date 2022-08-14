from characters import change_character_stat
from random import choice
from common import print_error_out_of_options_scope, sleep, file_characters
import inventory
import loot
import logging
import magic


def fight(hero, enemy):
    sleep(1)
    print("%s(%shp) vs %s(%shp)" % (hero["name"], hero["hp"], enemy["name"], enemy["hp"]))
    sleep(1)
    hero_hp = hero["hp"]
    enemy_hp = enemy["hp"]
    turn(hero, enemy, hero_hp, enemy_hp)


def turn(hero, enemy, hero_hp, enemy_hp, counter=1):
    while hero_hp >= 1 and enemy_hp >= 1:
        sleep(1)
        print("\nTurn %s begins\n\n"
              "Your HP: %s\n"
              "%s HP: %s\n" % (counter, hero_hp, enemy["name"], enemy_hp))
        sleep(0.5)
        action = choose_action()
        if action == 1:
            enemy_hp = do_basic_attack(attacker=hero, defender=enemy, defender_hp=enemy_hp)
        elif action == 2:
            enemy_hp = cast_spell(
                attacker=hero, defender=enemy, defender_hp=enemy_hp, counter=counter)
        elif action == 3:
            was_item_used = inventory.use_item(character=hero)
            while was_item_used is False:
                choose_action()
        elif action == 4:
            retreat_roll = choice([1, 2])
            if retreat_roll == 1:
                sleep(1)
                print("Retreat successful")
                quit()
            else:
                sleep(1)
                print("Retreat failed")
        else:
            enemy_action = enemy_choose_action()
            if enemy_action == 1:
                hp_before_enemy_attack = hero_hp
                hero_hp = do_basic_attack(attacker=enemy, defender=hero, defender_hp=hero_hp)
                hp_to_be_removed = hp_before_enemy_attack - hero_hp
                change_character_stat(
                    character=hero, stat="hp", how_much=hp_to_be_removed,
                    action="removing")
            else:
                counter += 1
    if is_enemy_dead(enemy_hp) is True:
        loot.loot_handling_after_combat(enemy)
    elif is_hero_dead(hero_hp) is True:
        quit()


def choose_action():
    while True:
        sleep(0.5)
        print("Choose an action to perform:\n"
              "1) Attack with your weapon\n"
              "2) Cast a spell\n"
              "3) Use an item\n"
              "4) Try to retreat(50%)")
        answer = int(input())
        if answer in [1, 2, 3, 4]:
            return answer
        else:
            print_error_out_of_options_scope()


def enemy_choose_action():
    sleep(1)
    print("Enemy performs an attack")
    return 1


def cast_spell(attacker, defender, defender_hp, counter):
    spell = magic.choose_spell_to_cast(spellbook=magic.get_spellbook())
    spend_mana = magic.spend_mana_to_cast_spell(caster=attacker, spell=spell)
    if spend_mana is False and attacker["name"] == "Hero":
        defender_hp = choose_action()
        return defender_hp
    elif spend_mana is not False and attacker["name"] != "Hero":
        enemy_choose_action()
        # WONT WORK, NEED A TURN REFACTOR
    else:
        damage = calculate_spell_damage(attacker=attacker, spell=spell)
        defender_hp = defender_hp - damage
        sleep(1)
        print("%s dealt %s magic damage to %s" % (attacker["name"], damage, defender["name"]))
        return defender_hp


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


def do_basic_attack(attacker, defender, defender_hp):
    damage = calculate_damage(attacker=attacker)
    defender_hp = defender_hp - damage
    sleep(1)
    print("%s dealt %s damage to %s" % (attacker["name"], damage, defender["name"]))
    return defender_hp


def calculate_damage(attacker):
    if attacker["name"] == "Hero":
        equipped_weapon = inventory.get_equipped_weapon()
        weapon_damage = equipped_weapon["damage"]
        print("You are attacking with %s" % equipped_weapon["name"])
        sleep(1)
        print("Weapon's damage: %s" % weapon_damage)
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


def is_hero_dead(hero_hp):
    if hero_hp <= 0:
        print("You are dead. Your journey has ended")
        return True


def is_enemy_dead(enemy_hp):
    if enemy_hp <= 0:
        print("Your foe is vanquished!")
        return True
    else:
        print("Enemy not dead yet - debugggggg")
