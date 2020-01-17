#!/usr/bin/env python3.6
""" Tests the cards module"""
import unittest
import pcutils
pcutils.add_to_python_path(__file__, '..')
import cards


class TestCards(unittest.TestCase):
    """ Tests the cards module"""
    def setUp(self):
        self.cards_obj = cards.Cards()
        self.all_cards = [
            "rd1", "rd2", "rd3", "ro1", "ro2", "ro3", "rp1", "rp2", "rp3",
            "yd1", "yd2", "yd3", "yo1", "yo2", "yo3", "yp1", "yp2", "yp3",
            "gd1", "gd2", "gd3", "go1", "go2", "go3", "gp1", "gp2", "gp3",
            "bd1", "bd2", "bd3", "bo1", "bo2", "bo3", "bp1", "bp2", "bp3"
        ]
        self.all_cards.sort()

    def test_get_hands(self):
        """ Tests that get_hands returns the correct cards"""
        expected = {}
        self.assertEqual(expected, self.cards_obj.get_hands())

    def test_get_list_of_random_cards(self):
        """ Tests that get_list_of_random_cards returns the right cards"""
        expected = self.all_cards
        cards_chosen = self.cards_obj.get_list_of_random_cards(36)
        cards_chosen.sort()
        self.assertEqual(expected, cards_chosen)

    def test_select_card(self):
        """ Tests that select_card returns the right card"""
        expected = "rd1"
        excluded_cards = self.all_cards
        excluded_cards.remove("rd1")
        self.assertEqual(expected, self.cards_obj.select_card_at_random(excluded_cards))

    def test_element_to_name_with_valid_element(self):
        """ Tests that the element to name method returns the correct name"""
        expected = "Diamond"
        self.assertEqual(expected, self.cards_obj.element_to_name("d"))

    def test_element_to_name_with_invalid_element(self):
        """ Tests that the element to name method raises an error when an invalid
        element is passed"""
        with self.assertRaises(RuntimeError):
            self.cards_obj.element_to_name("invalid element")

    def test_code_to_name_with_valid_code(self):
        """ Tests that code_to_name returns the right name"""
        expected = "Red Diamond Solitaire"
        self.assertEqual(expected, self.cards_obj.code_to_name("rd1"))

    def test_code_to_name_with_invalid_code(self):
        """ Tests that code_to_name raises error when an invalid code is
        passed in"""
        with self.assertRaises(RuntimeError):
            self.cards_obj.code_to_name("invalid code")

    def test_list_of_codes_to_names(self):
        """ Tests that a list of codes is translated into names properly"""
        expected = ["Red Diamond Solitaire", "Blue Opal Pair"]
        starting_list = ["rd1", "bo2"]
        self.assertEqual(expected, self.cards_obj.list_of_codes_to_names(starting_list))

    def test_is_valid_card_with_valid_card(self):
        """ Tests the is_valid_card method with a valid card"""
        self.assertTrue(self.cards_obj.is_valid_card("rd1"))

    def test_is_valid_card_with_invalid_card(self):
        """ Tests the is_valid_card method with am invalid card"""
        self.assertFalse(self.cards_obj.is_valid_card("r1d"))


if __name__ == '__main__':
    unittest.main()
