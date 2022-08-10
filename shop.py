import common
import inventory
import magic


def shop_encounter():
    answer_1 = shop_welcome()
    if answer_1 == 1:
        shop_buy()
    elif answer_1 == 2:
        shop_sell()
    elif answer_1 == 3:
        pass
        # leave
    else:
        common.print_error_out_of_options_scope()
        shop_encounter()


def shop_welcome():
    print("Welcome to my store, stranger. Would you like to buy or sell?\n1) Buy\n2) Sell\n3) Leave")
    answer_1 = int(input())
    if answer_1 > 3:
        common.print_error_out_of_options_scope()
        shop_encounter()
    return answer_1


def shop_buy():
    print("What can I interest you with?")
    print("1) Supplies\n2) Weapons\n3) Spells\n4) Back")
    answer = int(input())
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
    pass


def shop_supplies():
    print("Here are my wares:"
          "\n1) Health potion (10g)"
          "\n2) Back")
    answer = int(input())
    if answer == 1:
        # since gold has ID of "1", I did a dirty fix here to not change the whole ID assigning system in the loot :(
        buy_something(item_id=answer+1, type_of_item="item")
    elif answer == 2:
        shop_buy()
    else:
        common.print_error_out_of_options_scope()
        shop_supplies()


def shop_spells():
    print("Here are my wares:"
          "\n1) Firebolt (10g)"
          "\n2) Fireball (20g)"
          "\n3) Elemental Missiles (30g)"
          "\n4) Back")
    answer = int(input())
    if answer in [1, 2, 3]:
        buy_something(item_id=answer, type_of_item="spell")
    elif answer == 4:
        shop_buy()
    else:
        common.print_error_out_of_options_scope()
        shop_spells()


def shop_weapons():
    # create a temp list of weapons to choose from
    pass


def how_many_items():
    print("How many of those?")
    answer = int(input())
    if answer <= 0:
        print("Very funny. Anything else?")
        shop_encounter()
    else:
        return answer


def buy_something(item_id, type_of_item):
    if type_of_item == "item":
        item = inventory.get_item_from_inventory(file=inventory.file_items, item_id=item_id)
    elif type_of_item == "weapon":
        item = inventory.get_item_from_inventory(file=inventory.file_weapons, item_id=item_id)
    else:
        item = magic.get_spell_from_spellbook(spell_id=item_id)
    gold = inventory.get_item_from_inventory(file=inventory.file_items, item_id=1)
    if type_of_item == "spell":
        quantity = 1
        item["quantity"] = quantity
    else:
        quantity = how_many_items()
        item["quantity"] = quantity
    gold_check = check_if_player_has_enough_gold(gold["quantity"], price=item["value"], quantity=quantity)
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
        shop_supplies()
    else:
        inventory.remove_item_from_inventory(item=gold)
        inventory.add_item_to_inventory(item)
        shop_buy()


def sell_something(item, type_of_item):
    gold = inventory.get_item_from_inventory(file=inventory.file_items, item_id=1)
    inventory.add_item_to_inventory(item["value"])
    if type_of_item == "weapon":
        inventory.remove_weapon_from_inventory(weapon=item)
    elif type_of_item == "spell":
        magic.remove_spell_from_spellbook(spell=item)


def check_if_player_has_enough_gold(available_gold, price, quantity):
    check = available_gold - (quantity * price)
    if check >= 0:
        return True
    else:
        return False
