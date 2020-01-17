#!/usr/bin/env python3.6
""" Cards module that gathers info on the hands of each player"""

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
import random


class Cards:
    def __init__(self):
        self.colors = {'r': "Red", 'g': "Green", 'b': "Blue", 'y': "Yellow"}
        self.gems = {'d': "Diamond", 'p': "Pearl", 'o': "Opal"}
        self.quantities = {'1': "Solitaire", '2': "Pair", '3': "Cluster"}

    def get_hands(self):
        return {}

    def get_list_of_random_cards(self, amount, excluded=()):
        cards_chosen = []
        for _ in range(amount):
            excluded_cards = list(excluded) + cards_chosen
            card = self.select_card_at_random(excluded=excluded_cards)
            cards_chosen.append(card)
        return cards_chosen

    def select_card_at_random(self, excluded=()):
        while True:
            color = random.choice(list(self.colors))
            gem = random.choice(list(self.gems))
            quantity = random.choice(list(self.quantities))

            card = "{color}{gem}{quantity}".format(color=color, gem=gem, quantity=quantity)
            if card not in excluded:
                return card

    def list_of_codes_to_names(self, list_of_codes):
        return [self.code_to_name(card_code) for card_code in list_of_codes]

    def code_to_name(self, card_code):
        if not self.is_valid_card(card_code):
            raise RuntimeError("The card code {} is not valid".format(card_code))
        color = card_code[0]
        gem = card_code[1]
        quantity = card_code[2]
        return " ".join([self.colors[color], self.gems[gem], self.quantities[quantity]])

    def element_to_name(self, element):
        if element in self.colors:
            return self.colors[element]
        elif element in self.gems:
            return self.gems[element]
        elif element in self.quantities:
            return self.quantities[element]
        else:
            raise RuntimeError("The element {} is not a valid element".format(element))

    def is_valid_card(self, card_code):
        if len(card_code) == 3:
            codes = list(card_code)
            if (codes[0] in self.colors) and (codes[1] in self.gems) and (codes[2] in self.quantities):
                return True
        return False
