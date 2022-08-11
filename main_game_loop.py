import menu
from characters import choose_enemy_to_encounter, get_character_from_character_list, \
    file_characters, regenerate_after_combat
from combat import fight
from shop import shop_encounter
from common import sleep, reset_all_jsons


def main_loop():
    reset_all_jsons()
    menu.main_menu()
    game_length = 15
    game = 1
    while game <= game_length:
        enemy_encounter(counter=game)
        regenerate_after_combat(character=get_character_from_character_list(file=file_characters,
                                                                            character_id=0))
        if game == 3 or game == 6 or game == 9 or game == 12:
            shop_encounter()
        game += 1
    print("Congratulations, you have won the game. Feedback is welcomed :)")


def enemy_encounter(counter):
    stage = determine_stage_of_the_game(counter)
    enemy = choose_enemy_to_encounter(stage=stage)
    print("You encounter %s on your path" % enemy["name"])
    sleep(0.5)
    fight(hero=get_character_from_character_list(file=file_characters, character_id=0),
          enemy=enemy)


def determine_stage_of_the_game(counter):
    if counter in [1, 2, 3]:
        stage = "early"
    elif counter in [4, 5, 6]:
        stage = "mid"
    else:
        stage = "late"
    return stage


main_loop()
