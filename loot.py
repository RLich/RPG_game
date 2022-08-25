import random
import items
import inventory
from time import sleep
import logging


def generate_loot(enemy):
    # loot list: gold, weapon, health_potions, mana_potions
    loot = []
    loot_gold = generate_gold_loot(enemy=enemy)
    loot.append(loot_gold)
    if loot_gold == 1:
        logging.debug("You have found:\n   %s gold coin" % loot_gold)
    else:
        logging.debug("You have found:\n   %s gold coins" % loot_gold)
    if do_item_drop_as_loot(item="weapon") is True:
        sleep(0.5)
        weapon = items.create_weapon()
        loot.append(weapon)
        logging.debug("   %s" % weapon.name)
        does_loot_contain_weapon = True
    else:
        does_loot_contain_weapon = False
    if do_item_drop_as_loot(item="health_potion") is True:
        sleep(0.5)
        health_potions_quantity = random.choice([1, 2, 3])
        if health_potions_quantity == 1:
            logging.debug("   %s %s" % (health_potions_quantity, "health potion"))
        elif health_potions_quantity > 1:
            logging.debug("   %s %s" % (health_potions_quantity, "health potions"))
    else:
        health_potions_quantity = 0
    if do_item_drop_as_loot(item="mana_potion") is True:
        sleep(0.5)
        mana_potions_quantity = random.choice([1, 2, 3])
        if mana_potions_quantity == 1:
            logging.debug("   %s %s" % (mana_potions_quantity, "mana potion"))
        elif mana_potions_quantity > 1:
            logging.debug("   %s %s" % (mana_potions_quantity, "mana potions"))
    else:
        mana_potions_quantity = 0
    return loot, does_loot_contain_weapon, health_potions_quantity, mana_potions_quantity


def generate_gold_loot(enemy):
    weight = enemy["max_hp"] + enemy["str"]
    logging.debug("Calculating based on enemy's max_hp (%s) + str (%s) = %s" % (
        enemy["max_hp"], enemy["str"], weight))
    gold = random.randrange(0, 10) + weight
    event = random.randrange(0, 100)
    if event in range(0, 80):
        logging.debug("Leaving the loot gold as it is")
    elif event in range(81, 90):
        logging.debug("Doubling the gold - lucky find")
        gold = gold * 2
    else:
        logging.debug("Making the gold be 1")
        gold = 1
    return gold





def do_item_drop_as_loot(item):
    # determine if an item ("weapon" / "health_potion" / "mana_potion") dropped as a loot
    item_drop_roll = random.randrange(1, 10)
    if item == "weapon":
        if item_drop_roll >= 6:
            return True
    elif item == "health_potion":
        if item_drop_roll >= 4:
            return True
    elif item == "mana_potion":
        if item_drop_roll >= 4:
            return True


def collect_loot(looted_gold_quantity, is_weapon, weapon, health_potions_quantity,
                 mana_potions_quantity):
    gold = inventory.get_item_from_inventory(file=inventory.file_items, item_id=0)
    gold["quantity"] = looted_gold_quantity
    if is_weapon is True:
        inventory.add_weapon_to_inventory(weapon, is_from_shop=False)
    inventory.add_item_to_inventory(gold)
    if health_potions_quantity > 0:
        health_potions = inventory.get_item_from_inventory(file=inventory.file_items, item_id=1)
        health_potions["quantity"] = health_potions_quantity
        inventory.add_item_to_inventory(health_potions)
    if mana_potions_quantity > 0:
        mana_potions = inventory.get_item_from_inventory(file=inventory.file_items, item_id=2)
        mana_potions["quantity"] = mana_potions_quantity
        inventory.add_item_to_inventory(mana_potions)


def loot_handling_after_combat(enemy):
    sleep(1)
    print("%s dropped some loot:" % enemy["name"])
    loot = generate_loot(enemy=enemy)
    gold = loot[0][0]
    health_potions_quantity = loot[2]
    mana_potions_quantity = loot[3]
    does_loot_contain_weapon = loot[1]
    if does_loot_contain_weapon is True:
        weapon = loot[0][1]
    else:
        weapon = False
    collect_loot(looted_gold_quantity=gold, is_weapon=does_loot_contain_weapon, weapon=weapon,
                 health_potions_quantity=health_potions_quantity,
                 mana_potions_quantity=mana_potions_quantity)