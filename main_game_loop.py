import menu
from characters import choose_enemy_to_encounter, get_character_from_character_list, \
    file_characters, regenerate_after_combat
from combat import fight
from shop import shop_welcome
from common import reset_all_jsons, print_error_out_of_options_scope, style_text
from inventory import use_item, change_equipped_weapon
from time import sleep


def main_loop():
    reset_all_jsons()
    menu.main_menu()
    game_length = 15
    game = 1
    while game <= game_length:
        enemy_encounter(counter=game)
        regenerate_after_combat(character=get_character_from_character_list(file=file_characters,
                                                                            character_id=0))
        after_combat_break()
        if game == 3 or game == 6 or game == 9 or game == 12:
            shop_welcome()
        game += 1
    print("Congratulations, you have won the game. Feedback is welcomed :)")


def enemy_encounter(counter):
    stage = determine_game_stage(counter)
    enemy = choose_enemy_to_encounter(stage=stage)
    print("You encounter " + style_text(enemy["name"], style="bright") + " on your path")
    sleep(0.5)
    fight(hero=get_character_from_character_list(file=file_characters, character_id=0),
          enemy=enemy)


def determine_game_stage(counter):
    if counter in [1, 2, 3]:
        stage = "early"
    elif counter in [4, 5, 6]:
        stage = "mid"
    else:
        stage = "late"
    return stage


def after_combat_break():
    while True:
        print("\nYou are resting in a quiet place. What would you like to do?"
              "\n1) Continue with your journey"
              "\n2) Use an item"
              "\n3) Change equipped weapon"
              "\n4) Cast a spell (not implemented yet)")
        answer = int(input(">"))
        if answer == 1:
            break
        elif answer == 2:
            use_item(character=get_character_from_character_list(file=file_characters,
                                                                 character_id=0))
        elif answer == 3:
            change_equipped_weapon()
        elif answer == 4:
            print("I've told you it's not implemented yet :) You will fight a monster instead")
            break
        else:
            print_error_out_of_options_scope()
            after_combat_break()


main_loop()
