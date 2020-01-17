import random
import json
import basic_utils

CARD_HELP = """
Card Codes:

   COLOR            GEM              QUANTITY
r  -  red        d  -  diamond       1  -  solitaire
g  -  green      p  -  pearl         2  -  pair
b  -  blue       o  -  opal          3  -  cluster
y  -  yellow

Code must always be in [color][gem][quantity] order.

Valid card code:   rp3 = Red Pearl Cluster

Invalid card codes:  pr3, 3rp, r3p, p3r, etc.

"""

COLORS = {'r': "Red", 'g': "Green", 'b': "Blue", 'y': "Yellow"}
GEMS = {'d': "Diamond", 'p': "Pearl", 'o': "Opal"}
QUANTITIES = {'1': "Solitaire", '2': "Pair", '3': "Cluster"}


def get_hands():
    unavailable_cards = []
    hands = {}

    for player_i in range(basic_utils.ask_int("How many human players?\n")):

        hand = request_cards(str(player_i + 1))
        hands["p" + str(player_i)] = hand
        unavailable_cards += hand

    missing_card = select_card(excluded=unavailable_cards)
    hands["missing"] = missing_card
    unavailable_cards.append(missing_card)

    comp_card_amount = basic_utils.ask_int("How many cards for the computer?\n")
    hands["comp"] = select_cards(comp_card_amount, unavailable_cards)

    hands["extra"] = []
    for _ in range(36 - len(unavailable_cards)):
        card = select_card(excluded=unavailable_cards)
        hands["extra"].append(card)
        unavailable_cards.append(card)

    save_cards(hands)

    basic_utils.clear_screen()
    return hands


def save_cards(hands):
    with open("cards.json", "w") as jsonfile:
        json.dump(hands, jsonfile, indent=4, sort_keys=True)


def select_cards(amount, excluded=()):
    cards = []
    for _ in range(amount):
        card = select_card(excluded=excluded)
        cards.append(card)
        excluded.append(card)
    return cards


def select_card(excluded=()):
    color = random.choice(list(COLORS))
    gem = random.choice(list(GEMS))
    quantity = random.choice(list(QUANTITIES))
    
    card = color + gem + quantity
    if card not in excluded:
        return card
    return select_card(excluded=excluded)


def request_cards(player):
    cards = []
    basic_utils.clear_screen()
    print("Player " + player + " - Pick your cards:\n\n")

    while True:
        print(CARD_HELP)
        print("You have entered " + str(len(cards)) + " cards.")
        card = input("Enter a card - enter 'done' when finished:\n")
        if is_valid_card(card):
            cards.append(card)
        elif card.lower() == "done":
            break
        else:
            print("An invalid card was entered!")

    print("\n\n\nYou have entered the following cards:")
    print("\n".join(list_of_codes_to_names(cards)))
    answer = input("\nAre you sure these are your cards? If so, enter 'done'\n")
    if answer.lower() == "done":
        return cards
    else:
        return request_cards(player)


def list_of_codes_to_names(list_codes):
    return [code_to_name(card_code) for card_code in list_codes]


def code_to_name(card_code):
    color = card_code[0]
    gem = card_code[1]
    quantity = card_code[2]
    return " ".join([COLORS[color], GEMS[gem], QUANTITIES[quantity]])


def element_to_name(element):
    if element in COLORS:
        return COLORS[element]
    elif element in GEMS:
        return GEMS[element]
    elif element in QUANTITIES:
        return QUANTITIES[element]


def is_valid_card(card):  # Done
    if card[0] in COLORS and card[1] in GEMS and card[2] in QUANTITIES:
        return True
    return False
