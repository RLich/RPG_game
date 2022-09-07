import common
import inventory
import magic
import logging
from items import populate_weapons_shop_list, clear_weapons_shop_list_json, assign_free_id
from time import sleep


def shop_encounter():
    while True:
        try:
            shop_counter = 0
            print(
                "\n- Welcome to my store, stranger. Would you like to buy or sell?"
                "\n1) Buy"
                "\n2) Sell"
                "\n3) Leave")
            answer = int(input(">"))
            if answer == 1:
                shop_buy()
                break
            elif answer == 2:
                shop_sell()
                break
            elif answer == 3:
                # leave by not doing anything
                sleep(0.5)
                if shop_counter > 0:
                    # TODO implement bumping shop counter
                    print("\nAfter concluding your business, you return on the road\n")
                else:
                    print("\nNot feeling in a mood for trading, you merely glance at the stacks of "
                          "weapons and potions before returning to the world outside")
                sleep(0.5)
                break
            else:
                common.print_error_out_of_options_scope()
        except ValueError:
            common.print_error_wrong_value()


def shop_welcome():
    print("\nYou enter a local store. Being covered in dried out blood and road dust, "
          "the shopkeeper glances at you with rather defensive look on his face. He then sees your "
          "gold pouch and summons a restrained smile to his face. Felling the weight of gold at the"
          " waist, you come closer to the counter")
    print(common.style_text("Available gold: %s" % inventory.get_item_from_inventory(
        file=common.file_items, item_id=0)["quantity"], style="bright"))
    shop_encounter()


def shop_buy():
    while True:
        try:
            print("- What can I interest you with?")
            print("1) Supplies\n2) Weapons\n3) Spells\n4) Back")
            answer = int(input(">"))
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
            else:
                common.print_error_out_of_options_scope()
        except ValueError:
            common.print_error_wrong_value()


def shop_sell():
    while True:
        try:
            print("- What would you like to sell?"
                  "\n1) Supplies\n2) Weapons\n3) Back")
            answer = int(input(">"))
            if answer == 1:
                what_to_sell(type_of_item="supply")
                break
            elif answer == 2:
                what_to_sell(type_of_item="weapon")
                break
            elif answer == 3:
                shop_encounter()
                break
            else:
                common.print_error_out_of_options_scope()
        except ValueError:
            common.print_error_out_of_options_scope()


def what_to_sell(type_of_item):
    while True:
        try:
            print("- What kind of %ss do you have?" % type_of_item)
            if type_of_item == "supply":
                items_list = inventory.get_inventory(file=common.file_items)
                # removing gold from the list
                items_list.pop(0)
            else:
                items_list = inventory.get_inventory(file=common.file_weapons)
            item_counter = 1
            available_items_id_list = []
            used_counters = []
            for item in items_list:
                if type_of_item == "supply" and item["quantity"] > 0:
                    print("%s) %s (%s gold)" % (item_counter, item["name"], item["value"]))
                elif type_of_item == "weapon":
                    print("%s) %s (%s damage, price: %s gold)" % (item_counter, item["name"],
                                                                  item["damage"], item["value"]))
                else:
                    print("%s) %s (%s gold)" % (item_counter, item["name"], item["value"]))
                available_items_id_list.append(item["id"])
                used_counters.append(item_counter)
                item_counter += 1
            back_index = int(len(items_list) + 1)
            print("%s) Back" % back_index)
            answer = int(input(">"))
            if answer in used_counters:
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
                    print("You cannot sell an equipped weapon")
                    what_to_sell(type_of_item=type_of_item)
                    break
                else:
                    sell_something(
                        item=chosen_item,
                        how_many=quantity,
                        type_of_item=type_of_item
                    )
                    break
            elif answer == back_index:
                shop_sell()
                break
            else:
                common.print_error_out_of_options_scope()
                what_to_sell(type_of_item=type_of_item)
                break
        except ValueError:
            common.print_error_out_of_options_scope()


def shop_supplies():
    while True:
        try:
            print("- Here are my wares:"
                  "\n1) Health potion (10g)"
                  "\n2) Mana potion (10g)"
                  "\n3) Back")
            answer = int(input(">"))
            if answer in [1, 2]:
                item = inventory.get_item_from_inventory(file=common.file_items, item_id=answer)
                buy_something(item=item, type_of_item="item")
                break
            elif answer == 3:
                shop_buy()
                break
            else:
                common.print_error_out_of_options_scope()
        except ValueError:
            common.print_error_wrong_value()


def shop_spells():
    while True:
        try:
            spellbook = magic.get_spellbook()
            print("- Here are my wares:")
            spell_counter = 1
            available_spells_id_list = []
            used_counters = []
            for spell in spellbook:
                if spell["quantity"] == 0:
                    print("%s) %s (%s power, price: %s gold)" % (spell_counter, spell["name"],
                                                                 spell["power"], spell["value"]))
                    available_spells_id_list.append(spell["id"])
                    used_counters.append(spell_counter)
                    spell_counter += 1
            if spell_counter == 1:
                print("\nShopkeeper is looking around nervously, but eventually sighs:\n- I don't "
                      "have any new spells for you, traveller\n")
                sleep(1)
                shop_buy()
                break
            else:
                print("%s) Back" % spell_counter)
                answer = int(input(">"))
                if answer < spell_counter:
                    spell_id = available_spells_id_list[answer - 1]
                    spell = magic.get_spell_from_spellbook(spell_id=spell_id)
                    if spell["quantity"] == 1:
                        print("You already have this spell")
                        shop_spells()
                        break
                    else:
                        buy_something(item=spell, type_of_item="spell")
                        break
                elif answer == spell_counter:
                    shop_buy()
                    break
                else:
                    common.print_error_out_of_options_scope()
        except ValueError:
            common.print_error_wrong_value()


def shop_weapons():
    while True:
        try:
            populate_weapons_shop_list()
            weapons_for_sale = inventory.get_inventory(file=common.file_shop_weapons)
            print("- This is what I've got:")
            for weapon in weapons_for_sale:
                print("%s) %s (damage: %s, price: %s)" % (weapon["id"], weapon["name"],
                                                          weapon["damage"],weapon["value"]))
            print("%s) Back" % (len(weapons_for_sale) + 1))
            answer = int(input())
            if answer in range(1, 6):  # shopkeeper sells 5 weapons per visit -> need implementing
                chosen_weapon = weapons_for_sale[answer - 1]  # deducting one because indexing
                # starts from 0
                free_id = assign_free_id()
                chosen_weapon["id"] = free_id
                logging.debug("Assigning a new ID to the chosen weapon. New ID: %s" % free_id)
                clear_weapons_shop_list_json()
                buy_something(item=chosen_weapon, type_of_item="weapon")
                break
            elif answer == 6:
                clear_weapons_shop_list_json()
                shop_buy()
                break
            else:
                common.print_error_out_of_options_scope()
        except ValueError:
            common.print_error_wrong_value()


def how_many_items(item, action, type_of_item):
    while True:
        try:
            print("- How many of those?")
            answer = int(input(">"))
            if answer <= 0:
                print("- Very funny. Anything else?")
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
        except ValueError:
            common.print_error_wrong_value()


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
    elif gold_check is False:
        print("Not enough gold. Want to buy something else?")
        shop_buy()
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
