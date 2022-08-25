import json
from common import file_spells, get_object_from_json_list_by_id, \
    print_error_out_of_options_scope, style_text, color_text, file_characters
import logging
from characters import change_character_stat, get_character_from_character_list
from time import sleep
from combat import calculate_spell_power


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


def print_spells_in_spellbook():
    spellbook = get_spellbook()
    spell_counter = 1
    for spell in spellbook:
        if spell["quantity"] == 1:
            print(("%s) %s (%s power, %s mana cost)" % (
                spell_counter, spell["name"], spell["power"], spell["mana_cost"])))
            spell_counter += 1


def cast_spell(attacker, defender):
    while True:
        spell = choose_spell_to_cast(spellbook=get_spellbook())
        # spell is False when player decided to go back from spell selection
        if spell is False:
            return False
        was_enough_mana = check_if_enough_mana(caster=attacker, spell=spell)
        # no mana to cast -> no casting -> do another iteration
        if was_enough_mana is False and attacker["name"] == "Hero":
            pass
        # no mana to cast + caster is not hero -> make AI decide what to do next
        elif was_enough_mana is False and attacker["name"] != "Hero":
            pass  # NEED IMPLEMENTING ENEMY MAGIC USAGE
        elif spell["healing"] is False:
            damage = calculate_spell_power(attacker=attacker, spell=spell)
            sleep(0.5)
            print("\n%s dealt %s to %s" % (style_text(attacker["name"], style="bright"),
                                           color_text("%s magic damage" % damage, color="blue"),
                                           style_text(defender["name"], style="bright")))
            change_character_stat(character=defender, stat="hp", how_much=damage, action="removing")
            spend_mana_to_cast_spell(
                caster=attacker, spell=spell, caster_mana_after_casting=was_enough_mana)
            break
        else:
            healing = calculate_spell_power(attacker=attacker, spell=spell)
            sleep(0.5)
            if attacker["hp"] == attacker["max_hp"]:
                print("Your health is already full")
                return False
            elif healing + attacker["hp"] > attacker["max_hp"]:
                logging.debug("Health would be greater than max health, adjusting")
                healing = attacker["max_hp"] - attacker["hp"]
                print("\n%s restored %s to %s" % (style_text(attacker["name"], style="bright"),
                                                  color_text("%s health" % healing,
                                                             color="blue"),
                                                  style_text(attacker["name"], style="bright")))
                change_character_stat(character=attacker, stat="hp", how_much=healing,
                                      action="adding")
                spend_mana_to_cast_spell(
                    caster=attacker, spell=spell, caster_mana_after_casting=was_enough_mana)
                character = get_character_from_character_list(file=file_characters,
                                                              character_id=0)
                print("Current health: %s/%s" % (character["hp"], character["max_hp"]))
            else:
                print("\n%s restored %s to %s" % (style_text(attacker["name"], style="bright"),
                                                  color_text("%s health" % healing,
                                                             color="blue"),
                                                  style_text(attacker["name"], style="bright")))
                change_character_stat(character=attacker, stat="hp", how_much=healing,
                                      action="adding")
                spend_mana_to_cast_spell(
                    caster=attacker, spell=spell, caster_mana_after_casting=was_enough_mana)
                character = get_character_from_character_list(file=file_characters,
                                                              character_id=0)
                print("Current health: %s/%s" % (character["hp"], character["max_hp"]))
                break


def choose_spell_to_cast(spellbook):
    while True:
        print("Choose a spell to cast")
        spell_counter = 1
        available_spells_id_list = []
        used_counters = []
        for spell in spellbook:
            if spell["quantity"] == 1 and spell["combat"] is True:
                print(("%s) %s (%s power, %s mana cost)" % (
                    spell_counter, spell["name"], spell["power"], spell["mana_cost"])))
                available_spells_id_list.append(spell["id"])
                used_counters.append(spell_counter)
                spell_counter += 1
        print("%s) Back" % spell_counter)
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
def check_if_enough_mana(caster, spell):
    caster_mana = caster["mp"]
    spell_cost = spell["mana_cost"]
    if caster_mana >= spell_cost:
        logging.debug("Spent %s mana to cast %s" % (spell_cost, spell["name"]))
    else:
        print("Not enough mana to cast %s" % spell["name"])
        return False
    caster_mana_after_casting = caster_mana - spell_cost
    return caster_mana_after_casting


def spend_mana_to_cast_spell(caster, spell, caster_mana_after_casting):
    sleep(0.5)
    change_character_stat(character=caster, stat="mp", how_much=spell["mana_cost"],
                          action="removing")
    print("Mana remaining: %s" % caster_mana_after_casting)


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
