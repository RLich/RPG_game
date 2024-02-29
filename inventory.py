import json
import logging
from common import get_object_from_json_list_by_id, print_error_out_of_options_scope, \
    file_items, file_weapons, file_characters, print_error_wrong_value, style_text, player_input
from characters import change_character_stat, get_character_from_character_list
from time import sleep


def add_weapon_to_inventory(weapon, is_from_shop):
    if is_from_shop is True:
        pass
    else:
        weapon = vars(weapon)
    sleep(0.5)
    print("Adding a new weapon to the inventory: %s (damage: %s)" % (weapon["name"],
                                                                     weapon["damage"]))
    file = open(file_weapons, "r")
    file_content = json.loads(file.read())
    dict_list = file_content
    file_content.append(weapon)

    file_content = json.dumps(dict_list, indent=4)
    file.close()

    with open(file_weapons, "w") as outfile:
        outfile.write(file_content)


def remove_weapon_from_inventory(weapon):
    sleep(1)
    print("Removing %s from the inventory" % weapon["name"])
    file = open(file_weapons, "r")
    file_content = json.loads(file.read())
    dict_list = file_content
    file_content.remove(weapon)

    file_content = json.dumps(dict_list, indent=4)
    file.close()

    with open(file_weapons, "w") as outfile:
        outfile.write(file_content)


def add_item_to_inventory(item):
    sleep(1)
    if item["name"] == "Gold" and item["quantity"] == 1:
        sleep(0.3)
        print("Adding one gold coin to the inventory. You rich bastard...")
    elif item["name"] == "Gold" and item["quantity"] > 1:
        sleep(0.3)
        print("Adding %s gold coins to the inventory" % str(item["quantity"]))
    elif item["name"] != "Gold" and item["quantity"] == 1:
        sleep(0.3)
        print("Adding %s %s to the inventory" % (item["quantity"], item["name"]))
    else:
        sleep(0.3)
        print("Adding %s %s to the inventory" % (item["quantity"], item["name"]))
    replace_item_key_value_in_inventory(item=item, key="quantity", action="adding")


def get_item_from_inventory(file, item_id):
    inventory = open(file, "r")
    inventory_json = json.loads(inventory.read())
    chosen_item = get_object_from_json_list_by_id(data=inventory_json, object_id=item_id)
    inventory.close()
    return chosen_item


def get_inventory(file):
    inventory = open(file, "r")
    inventory_json = json.loads(inventory.read())
    return inventory_json


def remove_item_from_inventory(item):
    # quantity of the item will be removed by the item["quantity"] value. Not intuitive,
    # needs refactoring in the future
    sleep(1)
    if item["name"] == "Gold" and item["quantity"] == 1:
        print("Removing one gold coin from the inventory. You will miss it one day...")
    elif item["name"] == "Gold" and item["quantity"] > 1:
        print("Removing %s gold coins from the inventory" % item["quantity"])
    elif item["name"] != "Gold" and item["quantity"] == 1:
        print("Removing %s %s from the inventory" % (item["quantity"], str(item["name"])))
    else:
        print("Removing %s %s from the inventory" % (item["quantity"], item["name"] + "s"))
    replace_item_key_value_in_inventory(item=item, key="quantity", action="removing")


def replace_item_key_value_in_inventory(item, key, action):
    file = open(file_items, "r")
    file_content = json.loads(file.read())
    for object in file_content:
        if object["id"] == item["id"]:
            logging.debug("Replacing old item's %s %s %s with new item's quantity %s" % (
                object["name"], object[key], key, item[key]))
            if action == "adding":
                object[key] = object[key] + item[key]
            elif action == "replacing":
                # edit object's key before calling this function
                object[key] = item["key"]
            else:
                object[key] = object[key] - item[key]
    dict_list = file_content
    file_content = json.dumps(dict_list, indent=4)
    file.close()

    with open(file_items, "w") as outfile:
        outfile.write(file_content)
    file.close()
    file_content = json.dumps(dict_list, indent=4)
    file.close()

    with open(file_items, "w") as outfile:
        outfile.write(file_content)
    file.close()


def get_equipped_weapon():
    # Equipped weapon should have ID of "0"
    equipped_weapon = get_item_from_inventory(file=file_weapons, item_id=0)
    return equipped_weapon


def change_equipped_weapon():
    # To change weapon into equipped weapon, swap its ID with the current equipped weapon
    equipped_weapon = get_equipped_weapon()
    while True:
        print("Currently you use: %s (%s damage)" %
              (style_text(equipped_weapon["name"], style="bright"), equipped_weapon["damage"]))
        print("Available weapons to equip:")
        weapons_list = get_inventory(file=file_weapons)
        del weapons_list[0]
        weapon_counter = 1
        available_weapons_id_list = []
        used_counters = []

        for weapon in weapons_list:
            print("%s) %s (%s dmg)" % (weapon_counter, weapon["name"], weapon["damage"]))
            available_weapons_id_list.append(weapon["id"])
            used_counters.append(weapon_counter)
            weapon_counter += 1
        print("%s) Back" % weapon_counter)
        print("What weapon would you like to equip?")
        try:
            answer = int(input(">"))
            if answer in used_counters:
                # we subtract one from the user's input because of python's indexing. User's
                # choice of "1" is python's index of "0"
                chosen_weapon_id = available_weapons_id_list[answer - 1]
                chosen_weapon = get_item_from_inventory(file=file_weapons, item_id=chosen_weapon_id)
                swap_weapons_id(item_1=chosen_weapon, item_2=equipped_weapon)
                print("You now use %s (%s damage)" % (chosen_weapon["name"],
                                                      chosen_weapon["damage"]))
                break
            elif answer == len(used_counters) + 1:
                break
            else:
                print_error_out_of_options_scope()
        except ValueError:
            print_error_wrong_value()


def swap_weapons_id(item_1, item_2, key="id"):
    file = open(file_weapons, "r")
    file_content = json.loads(file.read())
    for object in file_content:
        if object["id"] == item_2["id"]:
            object[key] = item_1[key]
        elif object["id"] == item_1["id"]:
            object[key] = item_2["id"]
    dict_list = file_content
    file_content = json.dumps(dict_list, indent=4)
    file.close()

    file = open(file_weapons, "w")
    file.write(file_content)
    file.close()


def use_item(character):
    while True:
        item = choose_item_to_use()
        if item is False:
            return False
        else:
            if item["id"] == 1 and character["hp"] == character["max_hp"]:
                print("Your health is already full")
            elif item["id"] == 1:
                drink_potion(character=character, item=item)
                break
            elif item["id"] == 2 and character["mp"] == character["max_mp"]:
                print("Your mana is already full")
            else:
                drink_potion(character=character, item=item)
                break


def choose_item_to_use():
    while True:
        items_list = get_inventory(file=file_items)
        dialog = "Pick an item to use:"
        options = []
        for item in items_list:
            if item["id"] != 0 and item["quantity"] > 0:
                options.append(item["name"])
        options.append("Back")
        answer = player_input(dialog, options)
        back_index = int(len(items_list) + 1)
        if answer == back_index:
            return False
        else:
            item_to_return = get_item_from_inventory(file=file_items, item_id=answer)
            return item_to_return


def drink_potion(character, item):
    if item["id"] == 1:
        if item["restore"] + character["hp"] > character["max_hp"]:
            logging.debug("health would be greater than max health, adjusting")
            item["restore"] = character["max_hp"] - character["hp"]
        print("Restoring %s health" % item["restore"])
        change_character_stat(
            character=character, stat="hp", by_how_much=item["restore"], action="adding")
        character = get_character_from_character_list(file=file_characters,
                                                      character_id=0)
        print("Current health: %s/%s" % (character["hp"], character["max_hp"]))
    else:
        if item["restore"] + character["mp"] > character["max_mp"]:
            logging.debug("mana would be greater than max mana, adjusting")
            item["restore"] = character["max_mp"] - character["mp"]
        print("Restoring %s mana" % item["restore"])
        change_character_stat(
            character=character, stat="mp", by_how_much=item["restore"], action="adding")
        character = get_character_from_character_list(file=file_characters,
                                                      character_id=0)
        print("Current mana: %s/%s" % (character["mp"], character["max_mp"]))
    # need to edit item's "quantity" -> that will determine how much of it needs to be removed
    # I don't like it, note to self: refactor this remove_item_from_inventory function to
    # have "how_much" parameter handled in it, not outside
    item["quantity"] = 1
    remove_item_from_inventory(item=item)
