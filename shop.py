import common
import inventory
import magic
import logging
from items import remove_weapon_from_shop_list, assign_free_id, add_weapon_to_shop_list
from time import sleep


def shop_encounter():
    while True:
        dialog = '"Welcome to my store, stranger. Would you like to buy or got something to sell?"'
        options = [
            "Buy",
            "Sell",
            "Leave"
        ]
        answer = common.player_input(dialog, options)
        if answer == 1:
            shop_buy()
            break
        elif answer == 2:
            shop_sell()
            break
        elif answer == 3:
            # leave by not doing anything
            sleep(0.5)
            print("\nAfter concluding your business, you return on the road\n")
            sleep(0.5)
            break


def shop_welcome():
    print("\nYou enter a local store. Being covered in dried out blood and road dust, "
          "the shopkeeper glances at you with rather defensive look on his face. He then sees your "
          "gold pouch and summons a restrained smile to his face. Felling the weight of precious metal at the"
          " waist, you come closer to the counter")
    print(common.style_text("Available gold: %s" % inventory.get_item_from_inventory(
        file=common.file_items, item_id=0)["quantity"], style="bright"))
    shop_encounter()


def shop_buy():
    while True:
        dialog = '"What can I interest you with?'
        options = [
            "Supplies",
            "Weapons",
            "Spells",
            "Back"
        ]
        answer = common.player_input(dialog, options)
        if answer == 1:
            shop_supplies()
            break
        elif answer == 2:
            shop_weapons()
            break
        elif answer == 3:
            shop_spells()
            break
        elif answer == 4:
            shop_encounter()
            break


def shop_sell():
    while True:
        dialog = '"What would you like to sell?'
        options = [
            "Supplies",
            "Weapons",
            "Back"
        ]
        answer = common.player_input(dialog, options)
        if answer == 1:
            what_to_sell(type_of_item="supply")
            break
        elif answer == 2:
            what_to_sell(type_of_item="weapon")
            break
        elif answer == 3:
            shop_encounter()
            break


def what_to_sell(type_of_item):
    while True:
        dialog = '"What kind of %ss do you have?"' % type_of_item
        options = []
        if type_of_item == "supply":
            items_list = inventory.get_inventory(file=common.file_items)
            items_list.pop(0)  # removing gold from the list, as it cannot be sold
        else:
            items_list = inventory.get_inventory(file=common.file_weapons)
        available_items_id_list = []
        for item in items_list:
            if type_of_item == "supply" and item["quantity"] > 0:
                options.append("%s (%s gold)" % (item["name"], item["value"]))
            elif type_of_item == "weapon":
                options.append("%s (%s damage, price: %s gold)" % (item["name"], item["damage"], item["value"]))
            else:
                options.append("%s (%s gold)" % (item["name"], item["value"]))
            available_items_id_list.append(item["id"])
        options.append("Back")
        answer = common.player_input(dialog, options)
        if answer == len(options):
            shop_sell()
            break
        else:
            # we subtract one from the user's input because of python's indexing. User's choice
            # of "1" is python's index of "0"
            chosen_item_id = available_items_id_list[answer - 1]
            equipped_weapon = inventory.get_equipped_weapon()
            if type_of_item == "supply":
                chosen_item = inventory.get_item_from_inventory(file=common.file_items,
                                                                item_id=chosen_item_id)
            else:
                chosen_item = inventory.get_item_from_inventory(file=common.file_weapons,
                                                                item_id=chosen_item_id)
            if type_of_item == "weapon":
                quantity = 1
            else:
                quantity = how_many_items(
                    item=chosen_item, action="selling", type_of_item=type_of_item)
            if type_of_item == "weapon" and chosen_item_id == equipped_weapon["id"]:
                print("You cannot sell an equipped weapon. You can equip something else during camping and "
                      "sell this one on the next shop encounter")
                what_to_sell(type_of_item=type_of_item)
                break
            else:
                sell_something(
                    item=chosen_item,
                    how_many=quantity,
                    type_of_item=type_of_item
                )
                break


def shop_supplies():
    while True:
        dialog = '"Here are my wares:"'
        options = [
            "Health potion (10g)",
            "Mana potion (10g)",
            "Back"
        ]
        answer = common.player_input(dialog, options)
        if answer in [1, 2]:
            item = inventory.get_item_from_inventory(file=common.file_items, item_id=answer)
            buy_something(item=item, type_of_item="item")
            break
        elif answer == 3:
            shop_buy()
            break


def shop_spells():
    while True:
        dialog = '"Here are my wares:"'
        options = []
        spellbook = magic.get_spellbook()
        spell_counter = 1
        available_spells_id_list = []
        for spell in spellbook:
            if spell["quantity"] == 0:
                options.append("%s (%s power, price: %s gold)" % (spell["name"], spell["power"], spell["value"]))
                available_spells_id_list.append(spell["id"])
                spell_counter += 1
        if spell_counter == 1:
            print('Shopkeeper is looking around nervously, but eventually sighs:\n "I do not '
                  'have any new spells for you, traveller"\n')
            sleep(1)
            shop_buy()
            break
        else:
            options.append("Back")
            answer = common.player_input(dialog, options)
            if answer < spell_counter:
                spell_id = available_spells_id_list[answer - 1]
                spell = magic.get_spell_from_spellbook(spell_id=spell_id)
                if spell["quantity"] == 1:
                    print("You already have this spell")
                else:
                    buy_something(item=spell, type_of_item="spell")
                    break
            elif answer == spell_counter:
                shop_buy()
                break


def shop_weapons():
    while True:
        dialog = '"This is what I have for sell:"'
        options = []
        weapons_for_sale = inventory.get_inventory(file=common.file_shop_weapons)
        for weapon in weapons_for_sale:
            options.append("%s (damage: %s, price: %s)" % (weapon["name"], weapon["damage"], weapon["value"]))
        options.append("Back")
        answer = common.player_input(dialog, options)
        if answer in range(len(weapons_for_sale) + 1):  # adding one because of indexing
            chosen_weapon = weapons_for_sale[answer - 1]  # deducting one because of indexing
            logging.debug("Removing chosen weapon from shop's weapons list")
            remove_weapon_from_shop_list(weapon=chosen_weapon)
            initial_id = chosen_weapon["id"]
            free_id = assign_free_id()
            chosen_weapon["id"] = free_id
            logging.debug("Assigning a new ID to the chosen weapon. New ID: %s" % free_id)
            if buy_something(item=chosen_weapon, type_of_item="weapon") is False:
                logging.debug("Bringing deleted weapon back to the shop list as player "
                              "didn't have enough gold for it")
                chosen_weapon["id"] = initial_id
                add_weapon_to_shop_list(weapon=chosen_weapon)
                shop_buy()
            break
        elif answer == 6:
            shop_buy()
            break


def how_many_items(item, action, type_of_item):
    while True:
        dialog = '"How many of those?"'
        options = []
        answer = common.player_input(dialog, options)
        if answer <= 0:
            print('"Very funny. Anything else?"')
            sleep(1)
            shop_encounter()
            break
        else:
            if action == "buying":
                return answer
            else:
                enough_items_in_inventory = check_if_player_has_enough_items(
                    item=item, how_many=answer, type_of_item=type_of_item)
                if enough_items_in_inventory is True:
                    return answer
                else:
                    print("Not enough items in the inventory")
                    shop_sell()
                    break


def check_if_player_has_enough_items(item, how_many, type_of_item):
    if type_of_item == "weapons":
        return True
    else:
        file = common.file_items
    items_in_inventory = inventory.get_item_from_inventory(file=file, item_id=item["id"])[
        "quantity"]
    if items_in_inventory >= how_many:
        return True
    else:
        return False


def buy_something(item, type_of_item):
    gold = inventory.get_item_from_inventory(file=inventory.file_items, item_id=0)
    if type_of_item == "spell" or type_of_item == "weapon":
        quantity = 1
        item["quantity"] = quantity
    else:
        quantity = how_many_items(item=item, action="buying", type_of_item=type_of_item)
        item["quantity"] = quantity
    gold_check = check_if_player_has_enough_gold(gold["quantity"], price=item["value"],
                                                 quantity=quantity)
    gold["quantity"] = (item["value"] * quantity)
    if gold_check is True and type_of_item == "spell":
        inventory.remove_item_from_inventory(item=gold)
        magic.add_spell_to_spellbook(item)
        shop_buy()
    elif gold_check is True and type_of_item == "weapon":
        inventory.remove_item_from_inventory(item=gold)
        inventory.add_weapon_to_inventory(weapon=item, is_from_shop=True)
        shop_buy()
    elif gold_check is False and type_of_item != "weapon":
        print("It seems that you cannot afford it... That's fine")
        shop_buy()
    elif gold_check is False and type_of_item == "weapon":
        print("It seems that you cannot afford it... That's fine")
        return False
    else:
        inventory.remove_item_from_inventory(item=gold)
        inventory.add_item_to_inventory(item)
        shop_buy()


def sell_something(item, how_many, type_of_item):
    logging.debug("How many: %s" % how_many)
    gold = inventory.get_item_from_inventory(file=inventory.file_items, item_id=0)
    gold["quantity"] = int(item["value"] * how_many)
    logging.debug("Value:%s" % item["value"])
    logging.debug("How many items: %s" % how_many)
    logging.debug("How much gold to add: %s" % gold["quantity"])
    inventory.add_item_to_inventory(item=gold)
    if type_of_item == "weapon":
        inventory.remove_weapon_from_inventory(weapon=item)
        shop_sell()
    elif type_of_item == "supply":
        item["quantity"] = how_many
        inventory.remove_item_from_inventory(item=item)
        shop_sell()


def check_if_player_has_enough_gold(available_gold, price, quantity):
    check = available_gold - (quantity * price)
    if check >= 0:
        return True
    else:
        return False
