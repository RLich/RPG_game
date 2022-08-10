from random import choice, randrange
from inventory import file_weapons
import json
import logging
import inventory


class Weapon:
    def __init__(self, id, name, dmg, value):
        self.id = id
        self.name = name
        self.damage = dmg
        self.value = value


def weapon_name_generator():
    adjectives = ["Old", "Rusty", "Used", "Short", "Long", "Sharp", "Balanced", "Mastercraft"]
    chosen_adjective = choice(adjectives)
    types = ["Knife", "Dagger", "Mace", "Axe", "Sword", "Greatsword"]
    chosen_type = choice(types)
    name = chosen_adjective + " " + chosen_type
    logging.debug("A new weapon has been created: %s" % name)
    return name, chosen_adjective, chosen_type


def weapon_damage_generator_adjective(adjective):
    weapon_mod_adjective = 0
    if adjective == "Old":
        weapon_mod_adjective -= 4
    elif adjective == "Rusty":
        weapon_mod_adjective -= 3
    elif adjective == "Used":
        weapon_mod_adjective -= 2
    elif adjective == "Short":
        weapon_mod_adjective -= 1
    elif adjective == "Long":
        weapon_mod_adjective += 1
    elif adjective == "Sharp":
        weapon_mod_adjective += 2
    elif adjective == "Balanced":
        weapon_mod_adjective += 3
    elif adjective == "Mastercraft":
        weapon_mod_adjective += 4
    logging.debug("Adjusting weapon's damage by %s, because it's %s" % (weapon_mod_adjective,
                                                                    adjective))
    return weapon_mod_adjective


def weapon_damage_generator_type(type):
    weapon_mod_type = 0
    if type == "Knife":
        weapon_mod_type += 1
    elif type == "Dagger":
        weapon_mod_type += 2
    elif type == "Mace" or "Axe" or "Sword":
        weapon_mod_type += 3
    elif type == "Greatsword":
        weapon_mod_type += 4
    logging.debug("Adjusting weapon's damage by %s, because it's %s" % (weapon_mod_type, type))
    return weapon_mod_type


def weapon_damage_generator(weapon_mod_adjective, weapon_mod_type):
    weapon_dmg_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    weapon_base_damage = choice(weapon_dmg_range)
    weapon_final_dmg = weapon_base_damage + weapon_mod_adjective + weapon_mod_type
    if weapon_final_dmg <= 0:
        weapon_final_dmg = 1
    logging.debug("Weapon's final damage is: %s" % weapon_final_dmg)
    return weapon_final_dmg


def get_weapon_id_list():
    weapon_ids = []
    inventory_json = open(file_weapons, "r")
    inventory_list = json.loads(inventory_json.read())
    for item in inventory_list:
        weapon_ids.append(item["id"])
        logging.debug("Append a new id %s to weapons_id list: %s" % (item["id"], weapon_ids))
    inventory_json.close()
    return weapon_ids


def assign_free_id(weapon_ids):
    id_candidate = 1
    logging.debug("id_candidate: %s" % id_candidate)
    length_of_weapon_ids = len(weapon_ids)
    logging.debug("length of weapons_id: %s" % length_of_weapon_ids)
    while id_candidate in weapon_ids:
        logging.debug("id_candidate %s taken. Weapons_id: %s" % (id_candidate, weapon_ids))
        id_candidate += 1
    logging.debug("Free id found. A new id_candidate created. New weapon will be assigned as id: %s"
          % id_candidate)
    return id_candidate


def generate_weapon_value(damage):
    counter = 1
    value = 1
    while counter < damage:
        value += randrange(1, 6)
        counter += 1
    return value


def create_weapon():
    weapon_ids = get_weapon_id_list()
    free_id = assign_free_id(weapon_ids)
    name = weapon_name_generator()
    weapon_adj_mod = weapon_damage_generator_adjective(name[1])
    weapon_type_mod = weapon_damage_generator_type(name[2])
    damage = weapon_damage_generator(
            weapon_mod_adjective=weapon_adj_mod,
            weapon_mod_type=weapon_type_mod)
    weapon = Weapon(
        id=free_id,
        name=name[0],
        dmg=damage,
        value=generate_weapon_value(damage=damage)
    )
    weapon_ids.append(weapon.id)
    return weapon


def test_weapon_generation():
    x = 0
    while x < 2:
        create_weapon()
        print("")
        x += 1