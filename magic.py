import json
from common import file_spells, get_object_from_json_list_by_id, \
    print_error_out_of_options_scope
import logging
from characters import change_character_stat


class Spell:
    def __init__(self, id, name, dmg):
        self.id = id,
        self.name = name,
        self.damage = dmg


def get_spell_from_spellbook(spell_id):
    spellbook = open(file_spells, "r")
    spellbook_json = json.loads(spellbook.read())
    chosen_spell = get_object_from_json_list_by_id(data=spellbook_json, object_id=spell_id)
    spellbook.close()
    return chosen_spell


def get_spellbook():
    spellbook = open(file_spells, "r")
    spellbook_json = json.loads(spellbook.read())
    return spellbook_json


def generate_spells_id_list(spellbook):
    spells_id_list = []
    logging.debug("Creating a spells_id_list")
    for spell in spellbook:
        logging.debug("Appending spell's ID: %s to the spells_id_list" % spell["id"])
        spells_id_list.append(spell["id"])
    return spells_id_list


def print_spells_in_spellbook(spellbook):
    spell_counter = 1
    for spell in spellbook:
        if spell["quantity"] == 1:
            print(("%s) %s (%s damage, %s mana cost)" % (
                spell_counter, spell["name"], spell["damage"], spell["mana_cost"])))
            spell_counter += 1


def choose_spell_to_cast(spellbook):
    while True:
        print("Choose a spell to cast")
        spell_counter = 1
        available_spells_id_list = []
        used_counters = []
        for spell in spellbook:
            if spell["quantity"] == 1:
                print(("%s) %s (%s damage, %s mana cost)" % (
                    spell_counter, spell["name"], spell["damage"], spell["mana_cost"])))
                available_spells_id_list.append(spell["id"])
                used_counters.append(spell_counter)
                spell_counter += 1
        print("%s) Back" % (spell_counter))
        chosen_spell = int(input())
        if chosen_spell in used_counters:
            # we subtract one from the user's input because of python's indexing. User's choice of "1"
            # is python index of "0"
            chosen_spell = available_spells_id_list[chosen_spell - 1]
            chosen_spell = get_spell_from_spellbook(spell_id=chosen_spell)
            return chosen_spell
        elif chosen_spell == spell_counter:
            return False
        else:
            print_error_out_of_options_scope()


# returns False if not enough mana to cast spell, otherwise returns mana remaining after
# spellcasting
def spend_mana_to_cast_spell(caster, spell):
    caster_mana = caster["mp"]
    spell_cost = spell["mana_cost"]
    if caster_mana >= spell_cost:
        logging.debug("Spent %s mana to cast %s" % (spell_cost, spell["name"]))
    else:
        print("Not enough mana to cast %s" % spell["name"])
        return False
    caster_mana_after_casting = caster_mana - spell_cost
    change_character_stat(character=caster, stat="mp", how_much=spell_cost, action="removing")
    print("Mana remaining: %s" % caster_mana_after_casting)
    return caster_mana_after_casting


def remove_spell_from_spellbook(spell):
    print("Removing %s from the Spellbook" % spell["name"])
    replace_spell_quantity_in_spellbook(spell=spell, action="removing")


def add_spell_to_spellbook(spell):
    print("Adding %s to the Spellbook" % spell["name"])
    replace_spell_quantity_in_spellbook(spell=spell, action="adding")


def replace_spell_quantity_in_spellbook(spell, action):
    file = open(file_spells, "r")
    file_content = json.loads(file.read())
    for object in file_content:
        if object["id"] == spell["id"]:
            logging.debug("Replacing old item's quantity %s with new item's quantity %s" % (
                object["quantity"], spell["quantity"]))
            if action == "adding":
                object["quantity"] = object["quantity"] + spell["quantity"]
            else:
                object["quantity"] = object["quantity"] - spell["quantity"]
    dict_list = file_content
    file_content = json.dumps(dict_list, indent=4)
    file.close()

    with open(file_spells, "w") as outfile:
        outfile.write(file_content)
    file.close()
    file_content = json.dumps(dict_list, indent=4)
    file.close()

    with open(file_spells, "w") as outfile:
        outfile.write(file_content)
    file.close()