import common
import inventory
import magic
import logging


def shop_encounter():
    answer_1 = shop_welcome()
    if answer_1 == 1:
        shop_buy()
    elif answer_1 == 2:
        shop_sell()
    elif answer_1 == 3:
        common.sleep(0.5)
        print("\nLeaving the store\n")
        common.sleep(0.5)
        # leave
    else:
        common.print_error_out_of_options_scope()
        shop_encounter()


def shop_welcome():
    print(
        "Welcome to my store, stranger. Would you like to buy or sell?\n1) Buy\n2) Sell\n3) Leave")
    answer_1 = int(input(">"))
    if answer_1 > 3:
        common.print_error_out_of_options_scope()
        shop_encounter()
    return answer_1


def shop_buy():
    print("What can I interest you with?")
    print("1) Supplies\n2) Weapons\n3) Spells\n4) Back")
    answer = int(input(">"))
    if answer == 1:
        shop_supplies()
    elif answer == 2:
        shop_weapons()
    elif answer == 3:
        shop_spells()
    elif answer == 4:
        shop_encounter()
    else:
        common.print_error_out_of_options_scope()
        shop_buy()


def shop_sell():
    print("What would you like to sell?"
          "\n1) Supplies\n2) Weapons\n3) Back")
    answer = int(input(">"))
    if answer == 1:
        what_to_sell(type_of_item="supply")
    elif answer == 2:
        what_to_sell(type_of_item="weapon")
    elif answer == 3:
        shop_encounter()
    else:
        common.print_error_out_of_options_scope()
        shop_sell()


def what_to_sell(type_of_item):
    print("What kind of %s do you have?" % type_of_item)
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
            print("%s) %s (%s damage, price: %s gold" % (item_counter, item["name"],
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
        # we subtract one from the user's input because of python's indexing. User's choice of "1"
        # is python's index of "0"
        chosen_item_id = available_items_id_list[answer - 1]
        equipped_weapon = inventory.get_equipped_weapon()
        if type_of_item == "weapon" and chosen_item_id == equipped_weapon["id"]:
            print("You cannot sell an equipped weapon")
            what_to_sell(type_of_item=type_of_item)
        if type_of_item == "supply":
            chosen_item = inventory.get_item_from_inventory(file=common.file_items,
                                                            item_id=chosen_item_id)
        else:
            chosen_item = inventory.get_item_from_inventory(file=common.file_weapons,
                                                            item_id=chosen_item_id)
        if type_of_item == "weapon":
            quantity = 1
        else:
            quantity = how_many_items(item=chosen_item, action="selling", type_of_item=type_of_item)
        sell_something(
            item=chosen_item,
            how_many=quantity,
            type_of_item=type_of_item
        )
    elif answer == back_index:
        shop_sell()
    else:
        common.print_error_out_of_options_scope()
        what_to_sell(type_of_item=type_of_item)


def shop_supplies():
    print("Here are my wares:"
          "\n1) Health potion (10g)"
          "\n2) Mana potion (10g)"
          "\n3) Back")
    answer = int(input(">"))
    if answer == 1 or answer == 2:
        buy_something(item_id=answer, type_of_item="item")
    elif answer == 3:
        shop_buy()
    else:
        common.print_error_out_of_options_scope()
        shop_supplies()


def shop_spells():
    spellbook = magic.get_spellbook()
    print("Here are my wares:")
    print_counter = 1
    for spell in spellbook:
        print("%s) %s (%s damage, price: %s gold)" % (print_counter, spell["name"],
                                                      spell["damage"], spell["value"]))
        print_counter += 1
    print("%s) Back" % print_counter)
    answer = int(input(">"))
    if answer < print_counter:
        spell = magic.get_spell_from_spellbook(spell_id=answer)
        if spell["quantity"] == 1:
            print("You already have this spell")
            shop_spells()
        buy_something(item_id=answer, type_of_item="spell")
    elif answer == print_counter:
        shop_buy()
    else:
        common.print_error_out_of_options_scope()
        shop_spells()


def shop_weapons():
    # create a temp list of weapons to choose from
    pass


def how_many_items(item, action, type_of_item):
    print("How many of those?")
    answer = int(input(">"))
    if answer <= 0:
        print("Very funny. Anything else?")
        shop_encounter()
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


def buy_something(item_id, type_of_item):
    if type_of_item == "item":
        item = inventory.get_item_from_inventory(file=inventory.file_items, item_id=item_id)
    elif type_of_item == "weapon":
        item = inventory.get_item_from_inventory(file=inventory.file_weapons, item_id=item_id)
    else:
        item = magic.get_spell_from_spellbook(spell_id=item_id)
    gold = inventory.get_item_from_inventory(file=inventory.file_items, item_id=0)
    if type_of_item == "spell":
        quantity = 1
        item["quantity"] = quantity
    else:
        quantity = how_many_items(item=item, action="buying", type_of_item=type_of_item)
        item["quantity"] = quantity
    gold_check = check_if_player_has_enough_gold(gold["quantity"], price=item["value"],
                                                 quantity=quantity)
    gold["quantity"] = item["value"]
    if gold_check is True and type_of_item == "spell":
        inventory.remove_item_from_inventory(item=gold)
        magic.add_spell_to_spellbook(item)
        shop_buy()
    elif gold_check is True and type_of_item == "weapon":
        inventory.remove_item_from_inventory(item=gold)
        inventory.add_weapon_to_inventory(weapon=item)
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
