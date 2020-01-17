import cards
import random
import basic_utils

COMMAND_HELP = """
Commands:
answer [elements]           Search the computer's cards using a
                            search card. [elements] refers to what
                            one or two elements are being searched.
                            Valid examples:
                            answer r2   --   search for red pair cards
                            answer y    --   search for yellow cards
                            answer bd1  --   search for blue diamond
                                             solitaire cards(only for
                                             the last turn)

ask                         Have the computer choose a search card to
                            play (either 1, 2, 3, or 4) at random and
                            choose a player to play it on at random.

guess                       Make a guess at the missing card.

exit                        Exit the game.


"""


def play_sleuth():
    hands = cards.get_hands()
    missing_card = hands["missing"]
    comp_cards = hands["comp"]

    print("The extra cards are:")
    print("\n".join([cards.code_to_name(card_code) for card_code in hands["extra"]]))
    print("COMPUTER PLAYER IS READY TO PLAY!\n\n")
    pause()

    while True:
        print(COMMAND_HELP)
        action = input("Enter a command: ").lower().split()

        if len(action) > 1 and action[0] == "answer":
            answer(action, comp_cards, missing_card)
        elif action[0] == "ask":
            ask(len(hands) - 3)  # Number of players (excluding comp, extra, and missing cards)
        elif action[0] == "guess":
            guess(missing_card)
            break
        elif action[0] == "exit":
            print("\nGAME OVER")
            break
        else:
            print("An invalid command was entered!!\n")


def ask(num_of_players):
    message = "The computer plays search card {} on player {}"
    message = message.format(random.randint(1, 4), random.randint(1, num_of_players))
    print("\n---------------------------")
    print(message)
    print("\n---------------------------")
    pause()


def answer(action, comp_cards, missing_card):
    search_code = action[1]
    if not is_valid_search_code(search_code):
        print("An invalid search code was entered!!")
        return
    
    if len(search_code) == 1:
        show_amount(search_code, comp_cards)
        pause()
    elif len(search_code) == 2:
        show_cards(search_code, comp_cards)
        basic_utils.clear_screen()
    elif len(search_code) == 3:
        show_three_elements(search_code, comp_cards)
        guess(missing_card)
        basic_utils.clear_screen()


def guess(missing_card):
    print("\n\n")
    while True:
        card_code = input("Enter your guess(in valid card code format):\n")
        if cards.is_valid_card(card_code):
            break
        else:
            print("The card code you entered was invalid")

    if card_code != missing_card:
        print("INCORRECT!!! You are out of the game!")
    else:
        print("\n---------------------------\n" * 5)
        print("\n" * 2)
        print("CORRECT!! YOU WIN!")
        print("\n" * 2)
        print("\n---------------------------\n" * 5)
        
        pause()
        exit()
    pause()


def show_three_elements(search_code, comp_cards):
    elmt1 = search_code[0]
    elmt2 = search_code[1]
    elmt3 = search_code[2]
    for card in comp_cards:
        if elmt1 in card and elmt2 in card and elmt3 in card:
            message = "The computer has the {}".format(cards.code_to_name(card))
    
            print("\n---------------------------")
            print(message)
            print("\n---------------------------")
            pause()
            return

    print("\n---------------------------")
    print("The computer does not have that card")
    print("\n---------------------------")
    pause()


def show_amount(search_code, comp_cards):
    count = count_cards_one_element(comp_cards, search_code)
    message = "The computer has {} {} cards"
    message = message.format(count, cards.element_to_name(search_code))
    print("\n---------------------------")
    print(message)
    print("\n---------------------------")


def show_cards(search_code, comp_cards):
    card_list = find_cards_two_elements(comp_cards, search_code)
    message = "The computer has {} {} {} cards"
    message = message.format(len(card_list), cards.element_to_name(search_code[0]),
                             cards.element_to_name(search_code[1]))
    print("\n---------------------------")
    print(message)
    print("\n---------------------------")
    input("Press enter to view cards\n")

    print("The computer has the following cards:")
    print("\n".join([cards.code_to_name(card_code) for card_code in card_list]))
    pause()


def find_cards_two_elements(comp_cards, search_code):
    card_list = []
    for card in comp_cards:
        if search_code[0] in card and search_code[1] in card:
            card_list.append(card)
    return card_list


def count_cards_one_element(comp_cards, element):
    count = 0
    for card in comp_cards:
        if element in card:
            count += 1
    return count


def is_valid_search_code(search_code):
    if len(search_code) == 1:
        if is_valid_element(search_code):
            return True
    elif len(search_code) == 2:
        if is_valid_element(search_code[0]):
            if is_valid_element(search_code[1]):
                return True
    else:
        return False


def is_valid_element(element):
    if element in cards.COLORS or element in cards.GEMS or element in cards.QUANTITIES:
        return True
    return False


def pause():
    input("\nPress enter to continue\n")


if __name__ == "__main__":
    play_sleuth()
