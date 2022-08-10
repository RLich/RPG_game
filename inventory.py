import json
from common import sleep, file_items, file_weapons
import logging
from common import get_object_from_json_list_by_id


def add_weapon_to_inventory(weapon):
    weapon = vars(weapon)
    sleep(1)
    print("Adding a new item to the inventory:\nName: %s\nDamage: %s\n" % (weapon["name"],
                                                                           weapon["damage"]))
    file = open(file_weapons, "r")
    file_content = json.loads(file.read())
    dict_list = file_content
    file_content.append(weapon)

    file_content = json.dumps(dict_list, indent=4)
    file.close()

    with open(file_weapons, "w") as outfile:
        outfile.write(file_content)
    file.close()


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
    file.close()


def add_item_to_inventory(item):
    sleep(1)
    if item["name"] == "Gold" and item["quantity"] == 1:
        sleep(0.3)
        print("Adding one gold coin to the inventory. You rich bastard...")
    elif item["name"] == "Gold" and item["quantity"] > 1:
        sleep(0.3)
        print("Adding %s gold coins to the inventory" % str(item["quantity"]) + "s")
    elif item["name"] != "Gold" and item["quantity"] == 1:
        sleep(0.3)
        print("Adding %s %s to the inventory" % (item["quantity"], item["name"]))
    else:
        sleep(0.3)
        print("Adding %s %s to the inventory" % (item["quantity"], item["name"]))
    replace_item_quantity_in_inventory(item=item, action="adding")


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
    sleep(1)
    if item["name"] == "Gold" and item["quantity"] == 1:
        print("Removing one gold coin from the inventory. You will miss it one day...")
    elif item["name"] == "Gold" and item["quantity"] > 1:
        print("Removing %s gold coins from the inventory" % item["quantity"])
    elif item["name"] != "Gold" and item["quantity"] == 1:
        print("Removing %s %s from the inventory" % (item["quantity"], str(item["name"]) + "s"))
    else:
        print("Removing %s %s from the inventory" % (item["quantity"], item["name"]))
    replace_item_quantity_in_inventory(item=item, action="removing")


def replace_item_quantity_in_inventory(item, action):
    file = open(file_items, "r")
    file_content = json.loads(file.read())
    for object in file_content:
        if object["id"] == item["id"]:
            logging.debug("Replacing old item's quantity %s with new item's quantity %s" % (
                object["quantity"], item["quantity"]))
            if action == "adding":
                object["quantity"] = object["quantity"] + item["quantity"]
            else:
                object["quantity"] = object["quantity"] - item["quantity"]
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
    equipped_weapon = get_item_from_inventory(file=file_weapons, item_id=1)
    return equipped_weapon
